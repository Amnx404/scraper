"""Crawl4AI-backed web crawler — batched mode.

Instead of local threads, sends batches of URLs directly to the Crawl4AI API
(``POST /crawl`` with ``urls: [url1, url2, ...]``) and lets the remote server
handle parallelism. BFS proceeds in rounds: seed batch → extract links →
next batch → … until max_pages or frontier is exhausted.

Configuration keys (YAML / merged dict):
  crawl4ai_base_url       – Crawl4AI server root, e.g. https://…railway.app
                            Falls back to env CRAWL4AI_BASE_URL.
  crawl4ai_api_token      – Bearer token. Falls back to env CRAWL4AI_API_TOKEN.
  crawl4ai_timeout_sec    – Per-request HTTP timeout (default 120).
  crawl4ai_js_enabled     – java_script_enabled in browser_config (default true).
  crawl4ai_word_threshold – word_count_threshold for crawler_config (default 0).
  crawl4ai_scrape_pdfs    – When true, PDF URLs flow through the frontier (default true).
  parallel_workers        – Batch size: how many URLs per single /crawl call (default 4).

Entry points:
  run_crawl4ai_crawl(cfg) – in-process crawl, returns exit code 0/1/2.
  main()                   – CLI: python -m live.engines.crawl4ai_crawler [config.yaml]
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import UTC, datetime
from fnmatch import fnmatch
from urllib.parse import urljoin

import requests
import yaml

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None  # type: ignore[assignment]

from live.engines.browserless_crawler import (
    atomic_write_json,
    canonicalize_url,
    make_prefix,
    slug,
    url_output_filename,
)

_ENGINE = "crawl4ai"
_ENGINE_LABEL = "Crawl4AI /crawl REST API (batched)"

# ---------------------------------------------------------------------------
# Config
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
            "mailto:*", "tel:*", "javascript:*",
            "*.css*", "*.js*", "*.svg*", "*.png*", "*.jpg*", "*.jpeg*",
            "*.gif*", "*.webp*", "*.ico*", "*.pdf*", "*.zip*",
            "*.woff*", "*.woff2*", "*.ttf*", "*.eot*",
        ],
        "page_fetcher": "crawl4ai",
        "max_depth": None,
        "crawl4ai_base_url": None,
        "crawl4ai_api_token": None,
        "crawl4ai_timeout_sec": 120,
        "crawl4ai_js_enabled": True,
        "crawl4ai_word_threshold": 0,
        "crawl4ai_scrape_pdfs": True,
        **(raw or {}),
    }
    if cfg.get("crawl4ai_scrape_pdfs"):
        cfg["url_blacklist_patterns"] = [
            p for p in cfg.get("url_blacklist_patterns", []) if "pdf" not in p.lower()
        ]
    legacy = cfg.get("base_urls", [])
    if not cfg.get("seed_urls"):
        cfg["seed_urls"] = legacy
    if not cfg.get("allowed_prefixes"):
        cfg["allowed_prefixes"] = legacy
    cfg["seed_urls"] = [u for u in cfg.get("seed_urls", []) if isinstance(u, str) and u.strip()]
    cfg["allowed_prefixes"] = [u for u in cfg.get("allowed_prefixes", []) if isinstance(u, str) and u.strip()]
    return cfg


def load_config(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return merge_crawl4ai_defaults(raw)


def resolve_crawl4ai_config(cfg: dict) -> tuple[str, str]:
    base_url = (cfg.get("crawl4ai_base_url") or "").strip() or (os.environ.get("CRAWL4AI_BASE_URL") or "").strip()
    if not base_url:
        raise ValueError("Missing Crawl4AI base URL. Set env CRAWL4AI_BASE_URL or config crawl4ai_base_url.")
    api_token = (cfg.get("crawl4ai_api_token") or "").strip() or (os.environ.get("CRAWL4AI_API_TOKEN") or "").strip()
    if not api_token:
        raise ValueError("Missing Crawl4AI API token. Set env CRAWL4AI_API_TOKEN or config crawl4ai_api_token.")
    return base_url.rstrip("/"), api_token


# ---------------------------------------------------------------------------
# Media extraction
# ---------------------------------------------------------------------------

_VIDEO_DOMAINS = re.compile(
    r"(youtube\.com/watch|youtu\.be/|youtube\.com/embed|vimeo\.com/|\.mp4|\.webm|\.ogv)", re.I
)
_IMAGE_MD_RE = re.compile(r"!\[[^\]]*\]\(([^\s)\"]+)\)", re.I)
_PDF_URL_RE = re.compile(r"https?://[^\s)\"]+\.pdf(?:[?#][^\s)\"]*)?", re.I)
_VIDEO_URL_RE = re.compile(r"https?://[^\s)\"]+", re.I)
_IFRAME_SRC_RE = re.compile(r'<iframe[^>]+src=["\']([^"\']+)["\']', re.I)
_IMG_SRC_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.I)


def extract_media(markdown: str, links: list[str], api_media: dict, page_url: str = "", raw_html: str = "") -> dict[str, list[str]]:
    images: list[str] = []
    videos: list[str] = []
    pdfs: list[str] = []
    seen: set[str] = set()

    def _abs(url: str) -> str:
        url = url.strip().rstrip(")")
        if not url or url.startswith("data:"):
            return ""
        if page_url and not url.startswith(("http://", "https://")):
            url = urljoin(page_url, url)
        return url

    def _add(bucket: list[str], url: str) -> None:
        url = _abs(url)
        if url and url not in seen:
            seen.add(url)
            bucket.append(url)

    for img in (api_media.get("images") or []):
        src = img.get("src") or img.get("url") or (img if isinstance(img, str) else None)
        if src:
            _add(images, src)
    for vid in (api_media.get("videos") or []):
        src = vid.get("src") or vid.get("url") or (vid if isinstance(vid, str) else None)
        if src:
            _add(videos, src)
    for url in _IMAGE_MD_RE.findall(markdown):
        _add(images, url)
    for url in links:
        if re.search(r"\.pdf(?:[?#]|$)", url, re.I):
            _add(pdfs, url)
    for url in _PDF_URL_RE.findall(markdown):
        _add(pdfs, url)
    for url in links:
        if _VIDEO_DOMAINS.search(url):
            _add(videos, url)
    for url in _VIDEO_URL_RE.findall(markdown):
        if _VIDEO_DOMAINS.search(url):
            _add(videos, url)
    if raw_html:
        for src in _IFRAME_SRC_RE.findall(raw_html):
            if _VIDEO_DOMAINS.search(src):
                _add(videos, src)
        for src in _IMG_SRC_RE.findall(raw_html):
            if not re.search(r"\.(svg|gif|ico)$", src, re.I):
                _add(images, src)
    return {"images": images, "videos": videos, "pdfs": pdfs}


# ---------------------------------------------------------------------------
# Page result parsing (shared between sync /crawl and async /crawl/job)
# ---------------------------------------------------------------------------

def _parse_page_result(result: dict) -> dict:
    """Normalise a single crawl4ai page result dict into our standard format."""
    url = result.get("redirected_url") or result.get("url") or ""
    final_url = canonicalize_url(url) or url

    if not result.get("success"):
        return {
            "url": final_url,
            "error": result.get("error_message") or "crawl4ai page error",
            "success": False,
        }

    markdown_obj = result.get("markdown") or {}
    if isinstance(markdown_obj, dict):
        markdown = markdown_obj.get("fit_markdown") or markdown_obj.get("raw_markdown") or ""
    else:
        markdown = str(markdown_obj) if markdown_obj else ""

    links_obj = result.get("links") or {}
    raw_hrefs: list[str] = []
    if isinstance(links_obj, dict):
        for bucket in ("internal", "external"):
            for entry in (links_obj.get(bucket) or []):
                href = entry.get("href") if isinstance(entry, dict) else str(entry)
                if href and isinstance(href, str):
                    raw_hrefs.append(href)

    canonical_links: list[str] = []
    seen_links: set[str] = set()
    for href in raw_hrefs:
        c = canonicalize_url(urljoin(final_url, href))
        if c and c not in seen_links:
            seen_links.add(c)
            canonical_links.append(c)

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
        "last_modified": resp_headers.get("last-modified"),
    }

    stripped = markdown.strip()
    media = extract_media(
        markdown=stripped,
        links=canonical_links,
        api_media=result.get("media") or {},
        page_url=final_url,
        raw_html=result.get("html") or "",
    )

    return {
        "url": final_url,
        "markdown": stripped,
        "metadata": metadata,
        "links": canonical_links,
        "media": media,
        "success": True,
    }


# ---------------------------------------------------------------------------
# Batch fetch — concurrent async jobs (/crawl/job) with /crawl fallback
# ---------------------------------------------------------------------------

def _build_crawl_payload(urls: list[str], *, js_enabled: bool, word_threshold: int, timeout_sec: int) -> dict:
    return {
        "urls": urls,
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


def _submit_job(url: str, *, base_url: str, headers: dict, js_enabled: bool, word_threshold: int, timeout_sec: int) -> str:
    """Submit one URL as an async /crawl/job and return its task_id."""
    payload = _build_crawl_payload([url], js_enabled=js_enabled, word_threshold=word_threshold, timeout_sec=timeout_sec)
    resp = requests.post(f"{base_url}/crawl/job", headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    task_id = resp.json().get("task_id")
    if not task_id:
        raise ValueError(f"No task_id in /crawl/job response: {resp.json()}")
    return task_id


def _poll_job(task_id: str, *, base_url: str, headers: dict, timeout_sec: int, poll_interval: float = 2.0) -> dict:
    """Poll GET /crawl/job/{task_id} until completed or failed, return page result dict."""
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        resp = requests.get(f"{base_url}/crawl/job/{task_id}", headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status", "")
        if status == "completed":
            result_wrap = data.get("result") or {}
            page_results = result_wrap.get("results") or []
            if not page_results:
                return {"url": "", "error": "job completed but no results", "success": False}
            return _parse_page_result(page_results[0])
        if status == "failed":
            return {"url": "", "error": data.get("error") or "job failed", "success": False}
        time.sleep(poll_interval)
    return {"url": "", "error": f"job {task_id} timed out after {timeout_sec}s", "success": False}


def fetch_batch(
    urls: list[str],
    *,
    base_url: str,
    api_token: str,
    timeout_sec: int,
    js_enabled: bool = True,
    word_threshold: int = 0,
) -> list[dict]:
    """Submit each URL as a concurrent /crawl/job, poll all in parallel, return normalised results.

    Falls back to synchronous POST /crawl if job submission fails for any URL.
    parallel_workers (the caller's batch size) controls how many jobs fly simultaneously.
    """
    import threading

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    # Submit all jobs concurrently
    task_ids: dict[str, str] = {}   # url → task_id
    fallback_urls: list[str] = []

    def _submit(url: str) -> None:
        try:
            tid = _submit_job(url, base_url=base_url, headers=headers, js_enabled=js_enabled,
                              word_threshold=word_threshold, timeout_sec=timeout_sec)
            task_ids[url] = tid
        except Exception as exc:
            print(f"  /crawl/job submit failed for {url}: {exc} — will use /crawl fallback", flush=True)
            fallback_urls.append(url)

    submit_threads = [threading.Thread(target=_submit, args=(u,), daemon=True) for u in urls]
    for t in submit_threads:
        t.start()
    for t in submit_threads:
        t.join()

    # Poll all submitted jobs concurrently
    results: dict[str, dict] = {}   # url → parsed result

    def _poll(url: str, task_id: str) -> None:
        results[url] = _poll_job(task_id, base_url=base_url, headers=headers,
                                 timeout_sec=timeout_sec)
        # Patch in the original url if result url is empty (timeout/error case)
        if not results[url].get("url"):
            results[url]["url"] = url

    poll_threads = [threading.Thread(target=_poll, args=(u, tid), daemon=True)
                    for u, tid in task_ids.items()]
    for t in poll_threads:
        t.start()
    for t in poll_threads:
        t.join()

    # Fallback: sync /crawl for any URLs that failed job submission
    if fallback_urls:
        payload = _build_crawl_payload(fallback_urls, js_enabled=js_enabled,
                                       word_threshold=word_threshold, timeout_sec=timeout_sec)
        try:
            resp = requests.post(f"{base_url}/crawl", headers=headers, json=payload, timeout=timeout_sec)
            resp.raise_for_status()
            data = resp.json()
            for r in (data.get("results") or []):
                parsed = _parse_page_result(r)
                results[parsed["url"]] = parsed
        except Exception as exc:
            for u in fallback_urls:
                results[u] = {"url": u, "error": str(exc), "success": False}

    # Return in the same order as input
    return [results.get(u, {"url": u, "error": "no result", "success": False}) for u in urls]


# ---------------------------------------------------------------------------
# Crawl orchestration — round-based BFS, no local threads
# ---------------------------------------------------------------------------

def run_crawl4ai_crawl(cfg: dict) -> int:
    """Batch-mode BFS crawl via Crawl4AI.

    parallel_workers controls how many URLs are sent per /crawl call.
    Returns 0 on success, 1 for bad config, 2 when all visits errored.
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
    timeout_sec = int(cfg.get("crawl4ai_timeout_sec", 120))
    js_enabled = bool(cfg.get("crawl4ai_js_enabled", True))
    word_threshold = int(cfg.get("crawl4ai_word_threshold", 0))
    batch_size = max(1, int(cfg.get("parallel_workers", 4)))
    max_pages = int(cfg["max_pages"])
    retry_limit = int(cfg.get("retry_limit", 2))
    delay = float(cfg.get("delay", 0.5))
    _md = cfg.get("max_depth")
    max_depth: int | None = None if _md is None or _md is False else int(_md)

    allowed_prefixes = [make_prefix(u) for u in cfg["allowed_prefixes"]]
    respect_allowed_prefixes = bool(cfg.get("respect_allowed_prefixes", False))
    url_whitelist_patterns = cfg.get("url_whitelist_patterns", ["*"])
    url_blacklist_patterns = cfg.get("url_blacklist_patterns", [])

    output_dir = cfg["output_dir"]
    os.makedirs(output_dir, exist_ok=True)
    global_status_path = os.path.join(output_dir, cfg.get("global_status_filename", "crawl_status.json"))
    resume = bool(cfg.get("resume", False))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = timestamp

    # State
    url_records: dict[str, dict] = {}   # url → {status, source, retries, depth, ...}
    visited: set[str] = set()           # urls fully done (ok or error, no more retries)
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
        pages_dir = (
            os.path.normpath(os.path.join(output_dir, sub))
            if isinstance(sub, str) and sub.strip()
            else os.path.join(output_dir, cfg.get("page_output_subdir", "pages"), run_id)
        )
        # Rebuild visited from completed records
        for u, e in url_records.items():
            if isinstance(e, dict) and e.get("status") in ("ok", "error"):
                visited.add(u)
    else:
        pages_dir = os.path.join(output_dir, cfg.get("page_output_subdir", "pages"), run_id)

    os.makedirs(pages_dir, exist_ok=True)

    def persist_state() -> None:
        atomic_write_json(global_status_path, {
            "schema_version": 1,
            "run_id": run_id,
            "pages_subdir": os.path.relpath(pages_dir, output_dir),
            "urls": {k: dict(v) for k, v in url_records.items()},
        })

    def url_allowed(url: str) -> bool:
        if respect_allowed_prefixes and not any(url.startswith(p) for p in allowed_prefixes):
            return False
        if url_whitelist_patterns and not any(fnmatch(url, p) for p in url_whitelist_patterns):
            return False
        if url_blacklist_patterns and any(fnmatch(url, p) for p in url_blacklist_patterns):
            return False
        return True

    # frontier: list of (url, source, depth, retries)
    frontier: list[tuple[str, str, int, int]] = []
    frontier_set: set[str] = set()

    def enqueue(url: str, source: str, depth: int, retries: int = 0) -> None:
        if max_depth is not None and depth > max_depth:
            return
        c = canonicalize_url(url)
        if not c:
            return
        if not url_allowed(c):
            return
        if c in visited or c in frontier_set:
            return
        if len(visited) + len(frontier_set) >= max_pages:
            return
        frontier.append((c, source, depth, retries))
        frontier_set.add(c)
        url_records[c] = {
            "status": "queued",
            "source": source,
            "depth": depth,
            "retries": retries,
            "error": None,
            "output_file": None,
            "scraped_at": None,
        }

    # Seed
    for seed_url in cfg["seed_urls"]:
        enqueue(make_prefix(seed_url), "seed", 0)

    # Resume: re-enqueue anything not completed
    if resume and url_records:
        for u, entry in url_records.items():
            if not isinstance(entry, dict):
                continue
            if entry.get("status") in ("ok", "error"):
                continue
            enqueue(u, entry.get("source") or "?", int(entry.get("depth", 0)), int(entry.get("retries", 0)))

    if not frontier:
        print("No URLs to crawl.")
        persist_state()
        return 0

    print(f"\nStarting batched crawl — engine: {_ENGINE_LABEL}")
    print(f"Seeds: {', '.join(make_prefix(u) for u in cfg['seed_urls'])}")
    print(f"Allowed prefixes: {', '.join(allowed_prefixes)}")
    print(f"Batch size (parallel_workers): {batch_size} | Max pages: {max_pages} | Max depth: {max_depth if max_depth is not None else 'unlimited'}")
    print(f"Retry limit: {retry_limit} | Output: {pages_dir}")

    success_count = 0
    error_count = 0
    round_num = 0

    while frontier and len(visited) < max_pages:
        round_num += 1
        # Take next batch respecting max_pages cap
        remaining = max_pages - len(visited)
        batch_entries = frontier[:min(batch_size, remaining)]
        frontier = frontier[len(batch_entries):]
        for url, _, _, _ in batch_entries:
            frontier_set.discard(url)

        batch_urls = [url for url, _, _, _ in batch_entries]
        depth_map = {url: depth for url, _, depth, _ in batch_entries}
        source_map = {url: src for url, src, _, _ in batch_entries}
        retry_map = {url: ret for url, _, _, ret in batch_entries}

        print(f"\nRound {round_num}: fetching {len(batch_urls)} URL(s) | visited={len(visited)}/{max_pages}")
        for i, url in enumerate(batch_urls, 1):
            print(f"  [{i}/{len(batch_urls)}] d={depth_map[url]} {url}")

        for url in batch_urls:
            url_records[url] = {**url_records.get(url, {}), "status": "in_progress"}

        try:
            results = fetch_batch(
                batch_urls,
                base_url=base_url,
                api_token=api_token,
                timeout_sec=timeout_sec,
                js_enabled=js_enabled,
                word_threshold=word_threshold,
            )
        except Exception as e:
            # Whole batch failed — mark all as error or retry
            print(f"  Batch request failed: {e}")
            for url in batch_urls:
                retries = retry_map[url]
                if retries < retry_limit:
                    print(f"  Re-queuing {url} (retry {retries + 1}/{retry_limit})")
                    enqueue(url, source_map[url], depth_map[url], retries + 1)
                else:
                    visited.add(url)
                    url_records[url] = {
                        "status": "error", "source": source_map[url],
                        "depth": depth_map[url], "retries": retries,
                        "error": str(e), "output_file": None,
                        "scraped_at": datetime.now(UTC).isoformat(),
                    }
                    error_count += 1
            persist_state()
            time.sleep(delay)
            continue

        # Build a lookup by canonical URL for matching results back to inputs
        result_map: dict[str, dict] = {}
        for r in results:
            result_map[r["url"]] = r
            # Also index by original (pre-canonicalize) URL in case they differ
            if r.get("url") and r["url"] not in result_map:
                result_map[r["url"]] = r

        now = datetime.now(UTC).isoformat()
        for url in batch_urls:
            result = result_map.get(url)
            retries = retry_map[url]
            depth = depth_map[url]
            source = source_map[url]
            page_output_file = os.path.join(pages_dir, url_output_filename(url))
            rel_out = os.path.relpath(page_output_file, output_dir)

            if result is None or not result.get("success"):
                err = (result or {}).get("error") or "no result returned"
                if retries < retry_limit:
                    print(f"  Error on {url}: {err} — retry {retries + 1}/{retry_limit}")
                    enqueue(url, source, depth, retries + 1)
                    error_record = {
                        "url": url, "source": source, "engine": _ENGINE,
                        "engine_label": _ENGINE_LABEL, "retries": retries,
                        "error": err, "scraped_at": now,
                    }
                    with open(page_output_file, "w", encoding="utf-8") as fh:
                        fh.write(json.dumps(error_record, indent=2, ensure_ascii=False))
                    continue
                else:
                    print(f"  Error on {url}: {err} — retry limit reached")
                    visited.add(url)
                    error_count += 1
                    url_records[url] = {
                        "status": "error", "source": source, "depth": depth,
                        "retries": retries, "error": err,
                        "output_file": rel_out, "scraped_at": now,
                    }
                    error_record = {
                        "url": url, "source": source, "engine": _ENGINE,
                        "engine_label": _ENGINE_LABEL, "retries": retries,
                        "error": err, "scraped_at": now,
                    }
                    with open(page_output_file, "w", encoding="utf-8") as fh:
                        fh.write(json.dumps(error_record, indent=2, ensure_ascii=False))
                    continue

            # Success
            visited.add(url)
            success_count += 1
            url_records[url] = {
                "status": "ok", "source": source, "depth": depth,
                "retries": retries, "error": None,
                "output_file": rel_out, "scraped_at": now,
            }

            record = {
                "url": result["url"],
                "source": source,
                "engine": _ENGINE,
                "engine_label": _ENGINE_LABEL,
                "markdown": result["markdown"],
                "metadata": result["metadata"],
                "links": result["links"],
                "media": result["media"],
                "scraped_at": now,
            }
            with open(page_output_file, "w", encoding="utf-8") as fh:
                fh.write(json.dumps(record, indent=2, ensure_ascii=False))

            # Discover new links for next rounds
            for link in result["links"]:
                enqueue(link, url, depth + 1)
            for pdf_url in result["media"].get("pdfs", []):
                enqueue(pdf_url, url, depth + 1)

            print(f"  OK  {url}  ({len(result['markdown'].split())} words, {len(result['links'])} links)")

        persist_state()
        if frontier:
            time.sleep(delay)

    print(f"\nDone. {success_count} pages OK, {error_count} errors ({len(visited)} visited, {len(frontier)} still queued).")
    if success_count == 0 and error_count > 0:
        return 2
    return 0


# ---------------------------------------------------------------------------
# CLI
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
