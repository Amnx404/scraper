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
from urllib.parse import (
    parse_qsl,
    quote,
    unquote,
    urldefrag,
    urlencode,
    urljoin,
    urlparse,
    urlunparse,
)

import html2text
import requests
import yaml
from bs4 import BeautifulSoup

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None  # type: ignore[assignment]


def engine_label(fetcher: str) -> str:
    return {
        "browserless": "Browserless /content HTML (no direct target requests)",
    }.get(fetcher, fetcher)


_DYNAMIC_QUERY_KEYS = frozenset(
    {
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_term",
        "utm_content",
        "utm_id",
        "fbclid",
        "gclid",
        "gbraid",
        "wbraid",
        "msclkid",
        "yclid",
        "_ga",
        "_gl",
        "mc_cid",
        "mc_eid",
        "mkt_tok",
        "ref",
        "referrer",
        "referer",
        "igshid",
        "si",
        "ved",
        "ei",
        "session",
        "sid",
        "phpsessid",
        "jsessionid",
        "asp.net_sessionid",
        "nocache",
        "cache",
        "t",
        "ts",
        "time",
        "timestamp",
        "rnd",
        "random",
        "_",
        "_hsenc",
        "_hssc",
        "_hssrc",
        "_openstat",
    }
)


def _is_dynamic_query_key(key: str) -> bool:
    k = key.lower()
    if k.startswith("utm_"):
        return True
    if k.startswith("_hs") or k.startswith("hs_"):
        return True
    if k in _DYNAMIC_QUERY_KEYS:
        return True
    return False


def canonicalize_url(url: str) -> str | None:
    if not url or not isinstance(url, str):
        return None
    url = url.strip()
    if not url:
        return None
    url, _frag = urldefrag(url)
    for bad in ('"', "'", "\\", "\n", "\r", "\t", "<", ">", "{", "}"):
        if bad in url:
            return None
    try:
        p = urlparse(url)
    except ValueError:
        return None
    scheme = (p.scheme or "").lower()
    if scheme not in ("http", "https"):
        return None
    netloc = (p.netloc or "").lower().strip()
    if not netloc:
        return None
    if scheme == "http" and netloc.endswith(":80"):
        netloc = netloc[:-3]
    elif scheme == "https" and netloc.endswith(":443"):
        netloc = netloc[:-4]

    path = unquote(p.path or "")
    if not path.startswith("/"):
        path = "/" + path
    path = os.path.normpath(path).replace("\\", "/")
    if path == ".":
        path = "/"
    segments = []
    for seg in path.split("/"):
        if not seg:
            continue
        segments.append(quote(seg, safe="-_.~"))
    path = "/" + "/".join(segments) if segments else "/"

    if p.query:
        pairs = [
            (k, v)
            for k, v in parse_qsl(p.query, keep_blank_values=True)
            if not _is_dynamic_query_key(k)
        ]
        pairs.sort(key=lambda x: (x[0], x[1]))
        query = urlencode(pairs, doseq=True) if pairs else ""
    else:
        query = ""

    return urlunparse((scheme, netloc, path, "", query, ""))


def normalize(url: str) -> str | None:
    return canonicalize_url(url)


def make_prefix(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    norm = canonicalize_url(url)
    if norm is None:
        return url.rstrip("/") + "/"
    last_segment = urlparse(norm).path.rstrip("/").split("/")[-1]
    if "." not in last_segment:
        norm = norm.rstrip("/") + "/"
    return norm


def slug(url: str) -> str:
    p = urlparse(url)
    base = p.netloc + p.path.rstrip("/")
    return re.sub(r"[^\w\-]", "_", base).strip("_")


def url_output_filename(url: str) -> str:
    norm = canonicalize_url(url) or url
    short_hash = md5(norm.encode("utf-8")).hexdigest()[:10]
    return f"{slug(norm)}_{short_hash}.json"


def atomic_write_json(path: str, obj: dict) -> None:
    d = os.path.dirname(path) or "."
    os.makedirs(d, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def merge_scraper_defaults(raw: dict | None) -> dict:
    """Merge YAML / dict with defaults (same rules as the CLI config file)."""
    cfg = {
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
        "page_fetcher": "browserless",
        "max_depth": None,
        "browserless_timeout_sec": 60,
        "browserless_content_url": None,
        **(raw or {}),
    }
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
    return merge_scraper_defaults(raw)


def extract_page_data(
    html: str,
    final_url: str,
    status_code: int | None,
    content_type: str | None,
) -> tuple[dict, BeautifulSoup]:
    soup = BeautifulSoup(html, "html.parser")
    raw_soup = BeautifulSoup(html, "html.parser")

    for tag in soup.select("nav, footer, aside, script, style, [role='navigation']"):
        tag.decompose()

    converter = html2text.HTML2Text()
    converter.ignore_images = False
    converter.ignore_links = False
    converter.body_width = 0
    markdown = converter.handle(str(soup.body or soup))

    def meta(name=None, prop=None):
        tag = soup.find("meta", attrs={"name": name} if name else {"property": prop})
        return tag["content"].strip() if tag and tag.get("content") else None

    metadata = {
        "title": soup.title.get_text(strip=True) if soup.title else None,
        "description": meta(name="description") or meta(prop="og:description"),
        "og_title": meta(prop="og:title"),
        "og_image": meta(prop="og:image"),
        "language": soup.html.get("lang") if soup.html else None,
        "status_code": status_code,
        "content_type": content_type,
    }

    links: list[str] = []

    def add_canonical(href: str) -> None:
        href = href.strip()
        if not href:
            return
        c = canonicalize_url(urljoin(final_url, href))
        if c:
            links.append(c)

    for a in raw_soup.find_all("a", href=True):
        add_canonical(a["href"])
    for frame in raw_soup.find_all("iframe", src=True):
        add_canonical(frame["src"])
    for tag in raw_soup.find_all("link", href=True):
        add_canonical(tag["href"])
    for key in ("og:url", "twitter:url"):
        tag = raw_soup.find("meta", attrs={"property": key}) or raw_soup.find("meta", attrs={"name": key})
        if tag and tag.get("content"):
            add_canonical(tag["content"])

    fin = canonicalize_url(final_url) or final_url
    return (
        {
            "markdown": markdown.strip(),
            "metadata": metadata,
            "links": list(dict.fromkeys(links)),
            "final_url": fin,
        },
        raw_soup,
    )


def resolve_browserless_content_url(cfg: dict) -> str:
    url = (cfg.get("browserless_content_url") or "").strip() or (os.environ.get("BROWSERLESS_CONTENT_URL") or "").strip()
    if not url:
        raise ValueError(
            "Missing Browserless content endpoint. Set env BROWSERLESS_CONTENT_URL (e.g. https://.../content?token=...) "
            "or config browserless_content_url."
        )
    return url


def fetch_html_via_browserless(*, content_url: str, target_url: str, timeout_sec: int) -> requests.Response:
    payload = {"url": target_url}
    headers = {"Content-Type": "application/json"}
    return requests.request(
        "POST",
        content_url,
        headers=headers,
        data=json.dumps(payload),
        timeout=timeout_sec,
    )


def scrape_page_browserless(
    url: str,
    *,
    content_url: str,
    timeout_sec: int,
) -> dict:
    resp = fetch_html_via_browserless(content_url=content_url, target_url=url, timeout_sec=timeout_sec)
    html = resp.text or ""
    data, _raw = extract_page_data(
        html=html,
        final_url=url,
        status_code=resp.status_code,
        content_type=resp.headers.get("Content-Type"),
    )
    return data


def run_browserless_crawl(cfg: dict) -> int:
    """
    Run the browserless crawl from an in-memory config (same keys as YAML).

    Returns 0 on success, 1 for invalid/empty config, 2 when every visit errored.
    """
    if load_dotenv:
        load_dotenv()

    cfg = merge_scraper_defaults(dict(cfg))
    if not cfg.get("seed_urls"):
        print("No seed_urls specified in config.")
        return 1
    if not cfg.get("allowed_prefixes"):
        print("No allowed_prefixes specified in config.")
        return 1

    content_url = resolve_browserless_content_url(cfg)
    timeout_sec = int(cfg.get("browserless_timeout_sec", 60))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    configured_workers = int(cfg.get("parallel_workers", 4))
    if configured_workers <= 0:
        cpu_count = os.cpu_count() or 2
        workers = max(1, cpu_count - 1)
    else:
        workers = configured_workers

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
            print(f"Could not read {global_status_path}: {e}; starting a fresh run.", file=sys.stderr)
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

    def queue_candidates(url: str) -> list[str]:
        c = canonicalize_url(url)
        return [c] if c else []

    def terminal_ok_blocks_enqueue(candidate: str) -> bool:
        if candidate in seed_set:
            return False
        return url_records.get(candidate, {}).get("status") == "ok"

    def enqueue(url: str, discovered_from: str, retries: int = 0, *, depth: int = 0, force_seed: bool = False) -> None:
        if max_depth is not None and depth > max_depth:
            return
        for candidate in queue_candidates(url):
            if respect_allowed_prefixes and not any(candidate.startswith(p) for p in allowed_prefixes):
                continue
            if not wildcard_allowed(candidate):
                continue
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
                        continue
                    if terminal_ok_blocks_enqueue(candidate):
                        continue
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
    print(f"Engine: browserless — {engine_label('browserless')}")
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
                data = scrape_page_browserless(url, content_url=content_url, timeout_sec=timeout_sec)
                for link in data["links"]:
                    enqueue(link, discovered_from=url, depth=parent_depth + 1)

                record = {
                    "url": data["final_url"],
                    "source": parent,
                    "engine": "browserless",
                    "engine_label": engine_label("browserless"),
                    "markdown": data["markdown"],
                    "metadata": data["metadata"],
                    "links": data["links"],
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
                    "engine": "browserless",
                    "engine_label": engine_label("browserless"),
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


def main() -> None:
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        sys.exit(1)
    cfg = load_config(config_path)
    sys.exit(run_browserless_crawl(cfg))


if __name__ == "__main__":
    main()