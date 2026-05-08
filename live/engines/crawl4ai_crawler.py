"""Crawl4AI-backed web crawler.

Mirrors the interface of ``browserless_crawler`` but fetches pages through the
Crawl4AI REST API (``POST /crawl``) instead of Browserless.

Configuration keys (YAML / merged dict):
  crawl4ai_base_url       – Crawl4AI server root, e.g. https://…railway.app
                            Falls back to env CRAWL4AI_BASE_URL.
  crawl4ai_api_token      – Bearer token. Falls back to env CRAWL4AI_API_TOKEN.
  crawl4ai_timeout_sec    – Per-request HTTP timeout (default 90).
  crawl4ai_js_enabled     – Pass java_script_enabled to browser_config (default true).
  crawl4ai_word_threshold – word_count_threshold for crawler_config (default 0).
  crawl4ai_scrape_pdfs    – When true, PDF URLs are added to the crawl frontier and
                            scraped via Crawl4AI (default true).

Media extraction (always on):
  Every page record includes a ``media`` field:
    images – absolute URLs of <img> / markdown image refs
    videos – YouTube/Vimeo/mp4 embed/link URLs
    pdfs   – absolute URLs of linked PDF files

Entry points:
  run_crawl4ai_crawl(cfg) – in-process crawl, returns exit code 0/1/2.
  main()                   – CLI: python -m live.engines.crawl4ai_crawler [config.yaml]
"""

from __future__ import annotations

import json
import os
import re
import sys
import threading
import time
from datetime import UTC, datetime
from fnmatch import fnmatch
from hashlib import md5
from queue import Empty, Queue
from urllib.parse import urljoin

import requests
import yaml

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None  # type: ignore[assignment]

# Re-use URL utilities from the browserless crawler (pure functions, no side-effects).
from live.engines.browserless_crawler import (
    atomic_write_json,
    canonicalize_url,
    make_prefix,
    slug,
    url_output_filename,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_ENGINE = "crawl4ai"
_ENGINE_LABEL = "Crawl4AI /crawl REST API"


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------


def merge_crawl4ai_defaults(raw: dict | None) -> dict:
    cfg: dict = {
        "output_dir": "output",
        "max_pages": 500,
        "delay": 0.5,
        "respect_allowed_prefixes": False,
        "parallel_workers": 4,
        "retry_limit": 2,
        "page_output_subdir": "pages",
        "global_status_filename": "crawl_status.json",
        "resume": False,
        "url_whitelist_patterns": ["*"],
        "url_blacklist_patterns": [
            "mailto:*",
            "tel:*",
            "javascript:*",
            "*.css*",
            "*.js*",
            "*.svg*",
            "*.png*",
            "*.jpg*",
            "*.jpeg*",
            "*.gif*",
            "*.webp*",
            "*.ico*",
            "*.pdf*",
            "*.zip*",
            "*.woff*",
            "*.woff2*",
            "*.ttf*",
            "*.eot*",
        ],
        "page_fetcher": "crawl4ai",
        "max_depth": None,
        # Crawl4AI-specific
        "crawl4ai_base_url": None,
        "crawl4ai_api_token": None,
        "crawl4ai_timeout_sec": 90,
        "crawl4ai_js_enabled": True,
        "crawl4ai_word_threshold": 0,
        "crawl4ai_scrape_pdfs": True,
        **(raw or {}),
    }
    # When PDF scraping is enabled, remove the *.pdf* blacklist entry so PDF
    # URLs flow through the frontier and get scraped like regular pages.
    if cfg.get("crawl4ai_scrape_pdfs"):
        cfg["url_blacklist_patterns"] = [
            p for p in cfg.get("url_blacklist_patterns", []) if "pdf" not in p.lower()
        ]
    # Back-compat: accept base_urls in place of seed_urls / allowed_prefixes.
    legacy_base_urls = cfg.get("base_urls", [])
    if not cfg.get("seed_urls"):
        cfg["seed_urls"] = legacy_base_urls
    if not cfg.get("allowed_prefixes"):
        cfg["allowed_prefixes"] = legacy_base_urls

    cfg["seed_urls"] = [u for u in cfg.get("seed_urls", []) if isinstance(u, str) and u.strip()]
    cfg["allowed_prefixes"] = [u for u in cfg.get("allowed_prefixes", []) if isinstance(u, str) and u.strip()]
    return cfg


def load_config(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return merge_crawl4ai_defaults(raw)


def resolve_crawl4ai_config(cfg: dict) -> tuple[str, str]:
    """Return (base_url, api_token) or raise ValueError."""
    base_url = (cfg.get("crawl4ai_base_url") or "").strip() or (os.environ.get("CRAWL4AI_BASE_URL") or "").strip()
    if not base_url:
        raise ValueError(
            "Missing Crawl4AI base URL. Set env CRAWL4AI_BASE_URL or config crawl4ai_base_url."
        )
    api_token = (cfg.get("crawl4ai_api_token") or "").strip() or (os.environ.get("CRAWL4AI_API_TOKEN") or "").strip()
    if not api_token:
        raise ValueError(
            "Missing Crawl4AI API token. Set env CRAWL4AI_API_TOKEN or config crawl4ai_api_token."
        )
    return base_url.rstrip("/"), api_token


# ---------------------------------------------------------------------------
# Media extraction helpers
# ---------------------------------------------------------------------------

_VIDEO_DOMAINS = re.compile(
    r"(youtube\.com/watch|youtu\.be/|youtube\.com/embed|vimeo\.com/|\.mp4|\.webm|\.ogv)",
    re.I,
)
_IMAGE_MD_RE = re.compile(r"!\[[^\]]*\]\(([^\s)\"]+)\)", re.I)
_PDF_URL_RE = re.compile(r"https?://[^\s)\"]+\.pdf(?:[?#][^\s)\"]*)?", re.I)
_VIDEO_URL_RE = re.compile(r"https?://[^\s)\"]+", re.I)
_IFRAME_SRC_RE = re.compile(r'<iframe[^>]+src=["\']([^"\']+)["\']', re.I)
_IMG_SRC_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.I)


def extract_media(
    markdown: str,
    links: list[str],
    api_media: dict,
    page_url: str = "",
    raw_html: str = "",
) -> dict[str, list[str]]:
    """Return {images, videos, pdfs} extracted from markdown, links, and the
    Crawl4AI ``media`` API field.  All URLs are absolute and deduplicated."""

    images: list[str] = []
    videos: list[str] = []
    pdfs: list[str] = []
    seen: set[str] = set()

    def _abs(url: str) -> str:
        url = url.strip().rstrip(")")
        if not url:
            return ""
        if url.startswith("data:"):
            return ""
        if page_url and not url.startswith(("http://", "https://")):
            url = urljoin(page_url, url)
        return url

    def _add(bucket: list[str], url: str) -> None:
        url = _abs(url)
        if url and url not in seen:
            seen.add(url)
            bucket.append(url)

    # 1. Crawl4AI media object (images / videos / audios).
    for img in (api_media.get("images") or []):
        src = img.get("src") or img.get("url") or (img if isinstance(img, str) else None)
        if src:
            _add(images, src)
    for vid in (api_media.get("videos") or []):
        src = vid.get("src") or vid.get("url") or (vid if isinstance(vid, str) else None)
        if src:
            _add(videos, src)

    # 2. Markdown image refs: ![alt](url) — may be relative.
    for url in _IMAGE_MD_RE.findall(markdown):
        _add(images, url)

    # 3. PDF links from the canonicalized link list + markdown.
    for url in links:
        if re.search(r"\.pdf(?:[?#]|$)", url, re.I):
            _add(pdfs, url)
    for url in _PDF_URL_RE.findall(markdown):
        _add(pdfs, url)

    # 4. Video links from canonicalized links + markdown.
    for url in links:
        if _VIDEO_DOMAINS.search(url):
            _add(videos, url)
    for url in _VIDEO_URL_RE.findall(markdown):
        if _VIDEO_DOMAINS.search(url):
            _add(videos, url)

    # 5. Raw HTML: iframe srcs (YouTube/Vimeo embeds) and img srcs.
    if raw_html:
        for src in _IFRAME_SRC_RE.findall(raw_html):
            if _VIDEO_DOMAINS.search(src):
                _add(videos, src)
        for src in _IMG_SRC_RE.findall(raw_html):
            if not re.search(r"\.(svg|gif|ico)$", src, re.I):
                _add(images, src)

    return {"images": images, "videos": videos, "pdfs": pdfs}


# ---------------------------------------------------------------------------
# Page fetching
# ---------------------------------------------------------------------------


def scrape_page_crawl4ai(
    url: str,
    *,
    base_url: str,
    api_token: str,
    timeout_sec: int,
    js_enabled: bool = True,
    word_threshold: int = 0,
) -> dict:
    """Fetch *url* via Crawl4AI and return normalised page data dict.

    Returns:
        {
          "markdown": str,
          "metadata": {title, description, og_title, og_image, language, status_code, content_type},
          "links": list[str],   # canonicalized absolute URLs
          "media": {images: list[str], videos: list[str], pdfs: list[str]},
          "final_url": str,
        }
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }
    payload = {
        "urls": [url],
        "browser_config": {
            "headless": True,
            "java_script_enabled": js_enabled,
            "ignore_https_errors": True,
            "text_mode": False,
        },
        "crawler_config": {
            "word_count_threshold": word_threshold,
            "cache_mode": "bypass",
            "wait_until": "domcontentloaded",
            "page_timeout": max(30_000, timeout_sec * 1_000),
            "exclude_social_media_links": False,
            "score_links": False,
            "remove_consent_popups": True,
        },
    }

    resp = requests.post(
        f"{base_url}/crawl",
        headers=headers,
        json=payload,
        timeout=timeout_sec,
    )
    resp.raise_for_status()
    data = resp.json()

    if not data.get("success"):
        raise ValueError(f"Crawl4AI API returned success=false: {data}")

    results = data.get("results") or []
    if not results:
        raise ValueError("Crawl4AI returned empty results list")

    result = results[0]
    if not result.get("success"):
        err = result.get("error_message") or "unknown error"
        raise ValueError(f"Crawl4AI page fetch failed: {err}")

    # ---- Markdown ----
    markdown_obj = result.get("markdown") or {}
    if isinstance(markdown_obj, dict):
        markdown = (
            markdown_obj.get("fit_markdown")
            or markdown_obj.get("raw_markdown")
            or ""
        )
    else:
        markdown = str(markdown_obj) if markdown_obj else ""

    # ---- Links ----
    final_url: str = result.get("redirected_url") or result.get("url") or url
    links_obj = result.get("links") or {}
    raw_hrefs: list[str] = []
    if isinstance(links_obj, dict):
        for bucket in ("internal", "external"):
            for entry in links_obj.get(bucket) or []:
                href = entry.get("href") if isinstance(entry, dict) else str(entry)
                if href and isinstance(href, str):
                    raw_hrefs.append(href)

    canonical_links: list[str] = []
    seen: set[str] = set()
    for href in raw_hrefs:
        c = canonicalize_url(urljoin(final_url, href))
        if c and c not in seen:
            seen.add(c)
            canonical_links.append(c)

    # ---- Metadata ----
    meta_obj = result.get("metadata") or {}
    resp_headers = result.get("response_headers") or {}
    metadata = {
        "title": meta_obj.get("title") if isinstance(meta_obj, dict) else None,
        "description": meta_obj.get("description") if isinstance(meta_obj, dict) else None,
        "og_title": None,
        "og_image": None,
        "language": None,
        "status_code": result.get("status_code"),
        "content_type": resp_headers.get("content-type") or resp_headers.get("Content-Type"),
    }

    stripped_markdown = markdown.strip()
    media = extract_media(
        markdown=stripped_markdown,
        links=canonical_links,
        api_media=result.get("media") or {},
        page_url=final_url,
        raw_html=result.get("html") or "",
    )

    return {
        "markdown": stripped_markdown,
        "metadata": metadata,
        "links": canonical_links,
        "media": media,
        "final_url": canonicalize_url(final_url) or final_url,
    }


# ---------------------------------------------------------------------------
# Crawl orchestration (mirrors run_browserless_crawl)
# ---------------------------------------------------------------------------


def run_crawl4ai_crawl(cfg: dict) -> int:
    """Run the Crawl4AI crawl from an in-memory config dict.

    Returns 0 on success, 1 for invalid/empty config, 2 when every visit errored.
    """
    if load_dotenv:
        load_dotenv()

    cfg = merge_crawl4ai_defaults(dict(cfg))
    if not cfg.get("seed_urls"):
        print("No seed_urls specified in config.")
        return 1
    if not cfg.get("allowed_prefixes"):
        print("No allowed_prefixes specified in config.")
        return 1

    base_url, api_token = resolve_crawl4ai_config(cfg)
    timeout_sec = int(cfg.get("crawl4ai_timeout_sec", 90))
    js_enabled = bool(cfg.get("crawl4ai_js_enabled", True))
    word_threshold = int(cfg.get("crawl4ai_word_threshold", 0))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    configured_workers = int(cfg.get("parallel_workers", 4))
    workers = max(1, configured_workers) if configured_workers > 0 else max(1, (os.cpu_count() or 2) - 1)

    allowed_prefixes = [make_prefix(url) for url in cfg["allowed_prefixes"]]
    respect_allowed_prefixes = bool(cfg.get("respect_allowed_prefixes", False))
    url_whitelist_patterns = cfg.get("url_whitelist_patterns", ["*"])
    url_blacklist_patterns = cfg.get("url_blacklist_patterns", [])
    output_dir = cfg["output_dir"]
    os.makedirs(output_dir, exist_ok=True)
    global_status_path = os.path.join(output_dir, cfg.get("global_status_filename", "crawl_status.json"))
    resume = bool(cfg.get("resume", False))
    seed_set = {make_prefix(s) for s in cfg["seed_urls"]}

    url_records: dict[str, dict] = {}
    run_id = timestamp
    pages_dir: str

    if resume and os.path.isfile(global_status_path):
        try:
            with open(global_status_path, encoding="utf-8") as sf:
                state = json.load(sf)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Could not read {global_status_path}: {e}; starting fresh.", file=sys.stderr)
            state = {}
        raw = state.get("urls")
        if isinstance(raw, dict):
            url_records = {k: dict(v) if isinstance(v, dict) else {} for k, v in raw.items()}
        run_id = state.get("run_id") or timestamp
        sub = state.get("pages_subdir")
        if isinstance(sub, str) and sub.strip():
            pages_dir = os.path.normpath(os.path.join(output_dir, sub))
        else:
            pages_dir = os.path.join(output_dir, cfg.get("page_output_subdir", "pages"), run_id)
    else:
        pages_dir = os.path.join(output_dir, cfg.get("page_output_subdir", "pages"), run_id)

    os.makedirs(pages_dir, exist_ok=True)

    frontier: Queue[str] = Queue()
    state_lock = threading.Lock()
    write_lock = threading.Lock()
    stop_event = threading.Event()

    to_crawl: dict[str, dict] = {}
    crawled: dict[str, dict] = {}

    if resume and url_records:
        for u, e in url_records.items():
            if u in seed_set:
                continue
            if e.get("status") == "ok":
                crawled[u] = {
                    "status": "ok",
                    "error": e.get("error"),
                    "retries": e.get("retries", 0),
                    "output_file": e.get("output_file"),
                    "scraped_at": e.get("scraped_at"),
                }

    max_pages = int(cfg["max_pages"])
    retry_limit = int(cfg.get("retry_limit", 2))
    _md = cfg.get("max_depth")
    max_depth: int | None = None if _md is None or _md is False else int(_md)

    def persist_state() -> None:
        with state_lock:
            payload = {
                "schema_version": 1,
                "run_id": run_id,
                "pages_subdir": os.path.relpath(pages_dir, output_dir),
                "urls": {k: dict(v) for k, v in url_records.items()},
                "urls_to_process": sorted(to_crawl.keys()),
            }
        with write_lock:
            atomic_write_json(global_status_path, payload)

    def wildcard_allowed(url: str) -> bool:
        if url_whitelist_patterns and not any(fnmatch(url, p) for p in url_whitelist_patterns):
            return False
        if url_blacklist_patterns and any(fnmatch(url, p) for p in url_blacklist_patterns):
            return False
        return True

    def terminal_ok_blocks_enqueue(candidate: str) -> bool:
        if candidate in seed_set:
            return False
        return url_records.get(candidate, {}).get("status") == "ok"

    def enqueue(url: str, discovered_from: str, retries: int = 0, *, depth: int = 0, force_seed: bool = False) -> None:
        if max_depth is not None and depth > max_depth:
            return
        c = canonicalize_url(url)
        if not c:
            return
        candidate = c
        if respect_allowed_prefixes and not any(candidate.startswith(p) for p in allowed_prefixes):
            return
        if not wildcard_allowed(candidate):
            return
        with state_lock:
            if stop_event.is_set():
                return
            if force_seed:
                crawled.pop(candidate, None)
                if candidate in to_crawl:
                    return
                url_records[candidate] = {
                    "status": "queued",
                    "source": discovered_from,
                    "retries": retries,
                    "depth": depth,
                    "error": None,
                    "output_file": None,
                    "scraped_at": None,
                }
            else:
                if candidate in to_crawl:
                    return
                if candidate in crawled:
                    return
                if terminal_ok_blocks_enqueue(candidate):
                    return
            if len(crawled) + len(to_crawl) >= max_pages:
                return
            to_crawl[candidate] = {"source": discovered_from, "retries": retries, "in_progress": False, "depth": depth}
            if candidate not in url_records or force_seed:
                url_records[candidate] = {
                    "status": "queued",
                    "source": discovered_from,
                    "retries": retries,
                    "depth": depth,
                    "error": None,
                    "output_file": None,
                    "scraped_at": None,
                }
            else:
                url_records[candidate]["status"] = "queued"
                url_records[candidate]["source"] = discovered_from
                url_records[candidate]["retries"] = retries
                url_records[candidate]["depth"] = depth
            frontier.put(candidate)
        persist_state()

    for seed_url in cfg["seed_urls"]:
        enqueue(make_prefix(seed_url), discovered_from="seed", depth=0, force_seed=True)

    if resume and url_records:
        for u, entry in url_records.items():
            if u in seed_set:
                continue
            if entry.get("status") == "ok":
                continue
            d = int(entry.get("depth", 0))
            if max_depth is not None and d > max_depth:
                continue
            crawled.pop(u, None)
            enqueue(u, entry.get("source") or "?", int(entry.get("retries", 0)), depth=d)

    if not to_crawl:
        print("No URLs eligible to crawl after applying prefix rules.")
        persist_state()
        return 0

    print("\nStarting parallel crawl")
    print(f"Engine: {_ENGINE} — {_ENGINE_LABEL}")
    print(f"Resume: {resume} | status file: {global_status_path}")
    print(f"Seeds: {', '.join(make_prefix(url) for url in cfg['seed_urls'])}")
    print(f"Allowed prefixes: {', '.join(allowed_prefixes)}")
    print(f"Respect allowed prefixes: {respect_allowed_prefixes}")
    print(f"Workers: {workers}")
    print(f"Retry limit: {retry_limit}")
    print(f"Max depth (BFS hops from seed): {max_depth if max_depth is not None else 'unlimited'}")
    print(f"Per-page output dir: {pages_dir}")
    print(f"Global status file: {global_status_path}")

    def worker(worker_id: int) -> None:
        while True:
            if stop_event.is_set() and frontier.empty():
                return
            try:
                url = frontier.get(timeout=0.5)
            except Empty:
                with state_lock:
                    if not to_crawl:
                        return
                continue

            with state_lock:
                pending = to_crawl.get(url)
                if pending is None:
                    frontier.task_done()
                    continue
                if pending.get("in_progress"):
                    frontier.task_done()
                    continue
                pending["in_progress"] = True
                parent = pending["source"]
                retries = int(pending.get("retries", 0))
                parent_depth = int(pending.get("depth", 0))
                if len(crawled) >= max_pages:
                    stop_event.set()
                    to_crawl.pop(url, None)
                    frontier.task_done()
                    continue
                index = len(crawled) + 1
                url_records[url] = {
                    **url_records.get(url, {}),
                    "status": "in_progress",
                    "source": parent,
                    "retries": retries,
                    "depth": parent_depth,
                }

            print(f"  worker {worker_id} | page {index}/{max_pages} | d={parent_depth} | {url}")

            status = "ok"
            error_message = None
            page_output_file = os.path.join(pages_dir, url_output_filename(url))
            rel_out = os.path.relpath(page_output_file, output_dir)
            try:
                data = scrape_page_crawl4ai(
                    url,
                    base_url=base_url,
                    api_token=api_token,
                    timeout_sec=timeout_sec,
                    js_enabled=js_enabled,
                    word_threshold=word_threshold,
                )
                for link in data["links"]:
                    enqueue(link, discovered_from=url, depth=parent_depth + 1)
                # Also enqueue PDF URLs found in media so they get scraped.
                for pdf_url in data["media"].get("pdfs", []):
                    enqueue(pdf_url, discovered_from=url, depth=parent_depth + 1)

                record = {
                    "url": data["final_url"],
                    "source": parent,
                    "engine": _ENGINE,
                    "engine_label": _ENGINE_LABEL,
                    "markdown": data["markdown"],
                    "metadata": data["metadata"],
                    "links": data["links"],
                    "media": data["media"],
                    "scraped_at": datetime.now(UTC).isoformat(),
                }
                with open(page_output_file, "w", encoding="utf-8") as page_fh:
                    page_fh.write(json.dumps(record, indent=2, ensure_ascii=False))
            except Exception as e:
                error_message = str(e)
                if retries < retry_limit:
                    status = "retrying"
                    print(f"  Error: {e} (retry {retries + 1}/{retry_limit})")
                else:
                    status = "error"
                    print(f"  Error: {e} (retry limit reached)")
                error_record = {
                    "url": url,
                    "source": parent,
                    "engine": _ENGINE,
                    "engine_label": _ENGINE_LABEL,
                    "retries": retries,
                    "error": error_message,
                    "scraped_at": datetime.now(UTC).isoformat(),
                }
                with open(page_output_file, "w", encoding="utf-8") as page_fh:
                    page_fh.write(json.dumps(error_record, indent=2, ensure_ascii=False))
            finally:
                now = datetime.now(UTC).isoformat()
                with state_lock:
                    if status == "retrying":
                        if url in to_crawl:
                            to_crawl[url]["retries"] = retries + 1
                            to_crawl[url]["in_progress"] = False
                            url_records[url] = {
                                "status": "retrying",
                                "source": parent,
                                "retries": retries,
                                "depth": parent_depth,
                                "error": error_message,
                                "output_file": rel_out,
                                "scraped_at": now,
                            }
                            frontier.put(url)
                    else:
                        to_crawl.pop(url, None)
                        crawled[url] = {
                            "status": status,
                            "error": error_message,
                            "retries": retries,
                            "output_file": page_output_file,
                            "scraped_at": now,
                        }
                        url_records[url] = {
                            "status": status,
                            "source": parent,
                            "retries": retries,
                            "depth": parent_depth,
                            "error": error_message,
                            "output_file": rel_out,
                            "scraped_at": now,
                        }
                        if len(crawled) >= max_pages:
                            stop_event.set()
                frontier.task_done()
                persist_state()
                time.sleep(cfg["delay"])

    threads = [threading.Thread(target=worker, args=(i + 1,), daemon=True) for i in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    success_count = sum(1 for item in crawled.values() if item["status"] == "ok")
    print(f"Done. {success_count} pages scraped ({len(crawled)} URLs visited, {len(to_crawl)} still queued).")
    if success_count == 0 and crawled:
        any_error = any(item.get("status") == "error" for item in crawled.values() if isinstance(item, dict))
        if any_error:
            return 2
    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        sys.exit(1)
    cfg = load_config(config_path)
    sys.exit(run_crawl4ai_crawl(cfg))


if __name__ == "__main__":
    main()
