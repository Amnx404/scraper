"""
Domain scraper: crawls all pages reachable under a given URL prefix.

Usage:
    python scraper.py <url> [<url> ...] [options]

Example:
    python scraper.py https://example.com/docs/ --max-pages 100 --output results.json
"""

import argparse
import json
import logging
import sys
import time
from collections import deque
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)


def normalize(url: str) -> str:
    """Strip fragment, trailing slash-normalise, lowercase scheme+host."""
    url, _ = urldefrag(url)
    parsed = urlparse(url)
    # Lowercase scheme and host, keep path as-is
    return parsed._replace(scheme=parsed.scheme.lower(), netloc=parsed.netloc.lower()).geturl()


def is_within_prefix(url: str, prefix: str) -> bool:
    """Return True if url starts with the given prefix (scheme+host+path)."""
    return normalize(url).startswith(prefix)


def scrape(
    base_urls: list[str],
    max_pages: int = 500,
    delay: float = 0.5,
    timeout: int = 10,
    user_agent: str = "python-domain-scraper/1.0",
) -> dict[str, dict]:
    """
    Crawl each base URL and every reachable link that shares its prefix.

    Returns a dict keyed by URL with keys:
        status_code, title, links_found, error
    """
    session = requests.Session()
    session.headers["User-Agent"] = user_agent

    results: dict[str, dict] = {}

    for base_url in base_urls:
        if not base_url.startswith(("http://", "https://")):
            base_url = "https://" + base_url

        prefix = normalize(base_url)
        # Ensure prefix ends with / so startswith works for path boundaries
        if not urlparse(prefix).path.endswith("/") and "." not in urlparse(prefix).path.split("/")[-1]:
            prefix = prefix.rstrip("/") + "/"

        log.info("Starting crawl of prefix: %s", prefix)
        queue: deque[str] = deque([prefix])
        visited: set[str] = set()

        while queue and len(results) < max_pages:
            url = queue.popleft()
            norm = normalize(url)

            if norm in visited:
                continue
            if not is_within_prefix(norm, prefix):
                continue

            visited.add(norm)
            log.info("[%d] Fetching %s", len(results) + 1, norm)

            entry: dict = {"status_code": None, "title": None, "links_found": [], "error": None}

            try:
                resp = session.get(norm, timeout=timeout, allow_redirects=True)
                entry["status_code"] = resp.status_code

                if resp.status_code == 200 and "text/html" in resp.headers.get("Content-Type", ""):
                    soup = BeautifulSoup(resp.text, "html.parser")

                    title_tag = soup.find("title")
                    entry["title"] = title_tag.get_text(strip=True) if title_tag else None

                    for tag in soup.find_all("a", href=True):
                        href = tag["href"].strip()
                        absolute = normalize(urljoin(norm, href))
                        if is_within_prefix(absolute, prefix) and absolute not in visited:
                            entry["links_found"].append(absolute)
                            queue.append(absolute)

                    # Deduplicate links_found list
                    entry["links_found"] = list(dict.fromkeys(entry["links_found"]))

            except requests.RequestException as exc:
                entry["error"] = str(exc)
                log.warning("Error fetching %s: %s", norm, exc)

            results[norm] = entry
            time.sleep(delay)

    log.info("Crawl complete. %d pages scraped.", len(results))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape all pages under one or more URL prefixes.")
    parser.add_argument("urls", nargs="+", help="Base URL(s) to scrape, e.g. https://example.com/docs/")
    parser.add_argument("--max-pages", type=int, default=500, help="Maximum total pages to scrape (default: 500)")
    parser.add_argument("--delay", type=float, default=0.5, help="Seconds to wait between requests (default: 0.5)")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds (default: 10)")
    parser.add_argument("--output", default="-", help="Output file path (default: stdout)")
    parser.add_argument("--user-agent", default="python-domain-scraper/1.0", help="User-Agent header")
    args = parser.parse_args()

    results = scrape(
        base_urls=args.urls,
        max_pages=args.max_pages,
        delay=args.delay,
        timeout=args.timeout,
        user_agent=args.user_agent,
    )

    output = json.dumps(results, indent=2)
    if args.output == "-":
        print(output)
    else:
        with open(args.output, "w") as fh:
            fh.write(output)
        log.info("Results written to %s", args.output)


if __name__ == "__main__":
    main()
