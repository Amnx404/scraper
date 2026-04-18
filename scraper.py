import json
import os
import re
import sys
import threading
import time
from fnmatch import fnmatch
from hashlib import md5
from datetime import UTC, datetime
from queue import Empty, Queue
from urllib.parse import urldefrag, urljoin, urlparse

import html2text
import requests
import yaml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def normalize(url: str) -> str:
    url, _ = urldefrag(url)
    p = urlparse(url)
    return p._replace(scheme=p.scheme.lower(), netloc=p.netloc.lower()).geturl()


def make_prefix(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    norm = normalize(url)
    last_segment = urlparse(norm).path.rstrip("/").split("/")[-1]
    if "." not in last_segment:
        norm = norm.rstrip("/") + "/"
    return norm


def slug(url: str) -> str:
    p = urlparse(url)
    base = p.netloc + p.path.rstrip("/")
    return re.sub(r"[^\w\-]", "_", base).strip("_")


def url_output_filename(url: str) -> str:
    norm = normalize(url)
    short_hash = md5(norm.encode("utf-8")).hexdigest()[:10]
    return f"{slug(norm)}_{short_hash}.json"


def load_config(path: str) -> dict:
    with open(path) as f:
        cfg = yaml.safe_load(f)
    cfg = {
        "output_dir": "output",
        "max_pages": 500,
        "delay": 0.5,
        "use_selenium": True,
        "selenium_page_load_timeout": 20,
        "selenium_render_wait": 1.0,
        "respect_allowed_prefixes": False,
        "parallel_workers": 4,
        "retry_limit": 2,
        "page_output_subdir": "pages",
        "global_status_filename": "crawl_status.jsonl",
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
        **cfg,
    }
    # Backward compatibility: treat legacy base_urls as both seeds and allowed scope.
    legacy_base_urls = cfg.get("base_urls", [])
    if not cfg.get("seed_urls"):
        cfg["seed_urls"] = legacy_base_urls
    if not cfg.get("allowed_prefixes"):
        cfg["allowed_prefixes"] = legacy_base_urls

    # Ignore blank/null URLs from YAML lists.
    cfg["seed_urls"] = [u for u in cfg.get("seed_urls", []) if isinstance(u, str) and u.strip()]
    cfg["allowed_prefixes"] = [
        u for u in cfg.get("allowed_prefixes", []) if isinstance(u, str) and u.strip()
    ]
    return cfg


def create_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(), options=options)


def is_content_thin(markdown: str, raw_soup: BeautifulSoup) -> bool:
    text_len = len(markdown.strip())
    word_count = len(markdown.split())
    script_count = len(raw_soup.find_all("script"))
    has_spa_root = bool(raw_soup.select_one("#root, #app, #__next"))

    return (
        text_len < 300
        or word_count < 50
        or (has_spa_root and text_len < 800)
        or (script_count >= 5 and text_len < 500)
    )


def extract_page_data(
    html: str,
    final_url: str,
    status_code: int | None,
    content_type: str | None,
) -> tuple[dict, BeautifulSoup]:
    soup = BeautifulSoup(html, "html.parser")
    # IMPORTANT: collect links from the original, untouched DOM.
    raw_soup = BeautifulSoup(html, "html.parser")

    # Remove nav/footer/aside clutter so markdown is cleaner
    for tag in soup.select("nav, footer, aside, script, style, [role='navigation']"):
        tag.decompose()

    # Convert full body to markdown
    converter = html2text.HTML2Text()
    converter.ignore_images = False
    converter.ignore_links = False
    converter.body_width = 0  # no wrapping
    markdown = converter.handle(str(soup.body or soup))

    # Metadata — mirrors what Firecrawl returns
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

    # Anchor links from anywhere in the document (including nav/footer/aside).
    for a in raw_soup.find_all("a", href=True):
        href = a["href"].strip()
        if href:
            links.append(normalize(urljoin(final_url, href)))

    # Include iframe sources so embedded docs/apps can be crawled too.
    for frame in raw_soup.find_all("iframe", src=True):
        src = frame["src"].strip()
        if src:
            links.append(normalize(urljoin(final_url, src)))

    # Include link tags (canonical, alternate, preload, etc.).
    for tag in raw_soup.find_all("link", href=True):
        href = tag["href"].strip()
        if href:
            links.append(normalize(urljoin(final_url, href)))

    # Include URL-like metadata values where present.
    for key in ("og:url", "twitter:url"):
        tag = raw_soup.find("meta", attrs={"property": key}) or raw_soup.find(
            "meta", attrs={"name": key}
        )
        if tag and tag.get("content"):
            links.append(normalize(urljoin(final_url, tag["content"].strip())))

    return {
        "markdown": markdown.strip(),
        "metadata": metadata,
        "links": list(dict.fromkeys(links)),
        "final_url": normalize(final_url),
    }, raw_soup


def scrape_page(
    url: str,
    session: requests.Session,
    driver: webdriver.Chrome | None,
    render_wait: float,
) -> dict:
    resp = session.get(url, timeout=15, allow_redirects=True)
    final_url = resp.url
    request_ok = 200 <= resp.status_code < 400

    data, raw_soup = extract_page_data(
        html=resp.text,
        final_url=final_url,
        status_code=resp.status_code,
        content_type=resp.headers.get("Content-Type"),
    )

    should_try_selenium = driver is not None and (
        (not request_ok) or is_content_thin(data["markdown"], raw_soup)
    )
    if should_try_selenium:
        try:
            driver.get(url)
            time.sleep(render_wait)
            rendered_url = driver.current_url or final_url
            data, _ = extract_page_data(
                html=driver.page_source,
                final_url=rendered_url,
                status_code=resp.status_code,
                content_type=resp.headers.get("Content-Type"),
            )
            return data
        except Exception:
            # Fall through to request-based behavior if Selenium fails.
            pass

    if not request_ok:
        resp.raise_for_status()
    return data


def main() -> None:
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"

    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        sys.exit(1)

    cfg = load_config(config_path)

    if not cfg.get("seed_urls"):
        print("No seed_urls specified in config.")
        sys.exit(1)
    if not cfg.get("allowed_prefixes"):
        print("No allowed_prefixes specified in config.")
        sys.exit(1)

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
    pages_dir = os.path.join(output_dir, cfg.get("page_output_subdir", "pages"), timestamp)
    os.makedirs(pages_dir, exist_ok=True)
    global_status_path = os.path.join(
        output_dir, cfg.get("global_status_filename", "crawl_status.jsonl")
    )

    print("\nStarting parallel crawl")
    print(f"Seeds: {', '.join(make_prefix(url) for url in cfg['seed_urls'])}")
    print(f"Allowed prefixes: {', '.join(allowed_prefixes)}")
    print(f"Respect allowed prefixes: {respect_allowed_prefixes}")
    print(f"Workers: {workers}")
    print(f"Retry limit: {int(cfg.get('retry_limit', 2))}")
    print(f"Per-page output dir: {pages_dir}")
    print(f"Global status file: {global_status_path}")

    frontier: Queue[str] = Queue()
    state_lock = threading.Lock()
    write_lock = threading.Lock()
    stop_event = threading.Event()

    # Global hashmaps:
    # - to_crawl: URLs in queue or currently processing
    # - crawled: URLs completed (success or terminal error)
    to_crawl: dict[str, dict] = {}
    crawled: dict[str, dict] = {}
    max_pages = int(cfg["max_pages"])
    retry_limit = int(cfg.get("retry_limit", 2))

    def wildcard_allowed(url: str) -> bool:
        if url_whitelist_patterns and not any(fnmatch(url, p) for p in url_whitelist_patterns):
            return False
        if url_blacklist_patterns and any(fnmatch(url, p) for p in url_blacklist_patterns):
            return False
        return True

    def queue_candidates(url: str) -> list[str]:
        return [normalize(url)]

    def enqueue(url: str, discovered_from: str, retries: int = 0) -> None:
        for candidate in queue_candidates(url):
            if respect_allowed_prefixes and not any(candidate.startswith(p) for p in allowed_prefixes):
                continue
            if not wildcard_allowed(candidate):
                continue
            with state_lock:
                if stop_event.is_set():
                    return
                if candidate in to_crawl or candidate in crawled:
                    continue
                # Avoid unbounded queue growth once max pages has been reached.
                if len(crawled) + len(to_crawl) >= max_pages:
                    return
                to_crawl[candidate] = {
                    "source": discovered_from,
                    "retries": retries,
                    "in_progress": False,
                }
                frontier.put(candidate)

    for seed_url in cfg["seed_urls"]:
        enqueue(make_prefix(seed_url), discovered_from="seed")

    if not to_crawl:
        print("No URLs eligible to crawl after applying prefix rules.")
        return

    def worker(worker_id: int, status_file_handle) -> None:
        session = requests.Session()
        session.headers["User-Agent"] = cfg.get("user_agent", "python-domain-scraper/1.0")
        driver: webdriver.Chrome | None = None
        if cfg.get("use_selenium", True):
            try:
                driver = create_driver()
                driver.set_page_load_timeout(int(cfg.get("selenium_page_load_timeout", 20)))
            except Exception as e:
                print(f"Worker {worker_id}: Selenium unavailable, using requests-only mode: {e}")

        try:
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
                    if len(crawled) >= max_pages:
                        stop_event.set()
                        to_crawl.pop(url, None)
                        frontier.task_done()
                        continue
                    index = len(crawled) + 1

                print(f"  [{index}] {url}")

                status = "ok"
                error_message = None
                page_output_file = os.path.join(pages_dir, url_output_filename(url))
                try:
                    data = scrape_page(
                        url,
                        session,
                        driver,
                        float(cfg.get("selenium_render_wait", 1.0)),
                    )
                    for link in data["links"]:
                        enqueue(link, discovered_from=url)

                    record = {
                        "url": data["final_url"],
                        "source": parent,
                        "markdown": data["markdown"],
                        "metadata": data["metadata"],
                        "links": data["links"],
                        "scraped_at": datetime.now(UTC).isoformat(),
                    }
                    with open(page_output_file, "w") as page_fh:
                        page_fh.write(json.dumps(record, indent=2))
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
                        "retries": retries,
                        "error": error_message,
                        "scraped_at": datetime.now(UTC).isoformat(),
                    }
                    with open(page_output_file, "w") as page_fh:
                        page_fh.write(json.dumps(error_record, indent=2))
                finally:
                    status_record = {
                        "url": url,
                        "source": parent,
                        "retries": retries,
                        "status": status,
                        "error": error_message,
                        "output_file": page_output_file,
                        "scraped_at": datetime.now(UTC).isoformat(),
                    }
                    with write_lock:
                        status_file_handle.write(json.dumps(status_record) + "\n")
                        status_file_handle.flush()
                    with state_lock:
                        if status == "retrying":
                            if url in to_crawl:
                                to_crawl[url]["retries"] = retries + 1
                                to_crawl[url]["in_progress"] = False
                                frontier.put(url)
                        else:
                            to_crawl.pop(url, None)
                            crawled[url] = {
                                "status": status,
                                "error": error_message,
                                "retries": retries,
                                "output_file": page_output_file,
                                "scraped_at": datetime.now(UTC).isoformat(),
                            }
                            if len(crawled) >= max_pages:
                                stop_event.set()
                    frontier.task_done()
                    time.sleep(cfg["delay"])
        finally:
            if driver:
                driver.quit()

    with open(global_status_path, "a") as status_fh:
        threads = [
            threading.Thread(target=worker, args=(i + 1, status_fh), daemon=True)
            for i in range(workers)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    success_count = sum(1 for item in crawled.values() if item["status"] == "ok")
    print(
        f"Done. {success_count} pages scraped ({len(crawled)} URLs visited, "
        f"{len(to_crawl)} still queued)."
    )


if __name__ == "__main__":
    main()
