"""
Domain scraper: crawls all pages reachable under a given URL prefix.
Uses Scrapy for the crawl engine. Results are saved to output/<domain>/

Usage:
    python scraper.py <url> [<url> ...] [options]

Examples:
    python scraper.py https://example.com/docs/
    python scraper.py https://github.com/xyz/ --max-pages 200 --delay 1.0
    python scraper.py https://a.com/x/ https://b.com/y/ --output-dir my_results
"""

import argparse
import os
import re
from datetime import datetime
from urllib.parse import urldefrag, urlparse, urljoin

import scrapy
from scrapy.crawler import CrawlerProcess


def normalize(url: str) -> str:
    url, _ = urldefrag(url)
    p = urlparse(url)
    return p._replace(scheme=p.scheme.lower(), netloc=p.netloc.lower()).geturl()


def make_prefix(url: str) -> str:
    """Return a prefix that ends with '/' so path boundaries are respected."""
    norm = normalize(url)
    p = urlparse(norm)
    last_segment = p.path.rstrip("/").split("/")[-1]
    # If last segment has no extension it's likely a directory; add trailing slash
    if "." not in last_segment:
        norm = norm.rstrip("/") + "/"
    return norm


def slug(url: str) -> str:
    """Turn a URL into a safe directory name."""
    p = urlparse(url)
    base = p.netloc + p.path.rstrip("/")
    return re.sub(r"[^\w\-]", "_", base).strip("_")


class PrefixSpider(scrapy.Spider):
    name = "prefix_spider"

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "USER_AGENT": "python-domain-scraper/1.0",
        "HTTPCACHE_ENABLED": False,
        "LOG_LEVEL": "INFO",
        "AUTOTHROTTLE_ENABLED": True,
    }

    def __init__(self, start_urls, prefixes, feeds, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.prefixes = prefixes
        self.custom_settings = {**self.custom_settings, "FEEDS": feeds}

    def parse(self, response):
        url = normalize(response.url)

        # Only emit items for pages that are within a watched prefix
        if not any(url.startswith(p) for p in self.prefixes):
            return

        yield {
            "url": url,
            "status": response.status,
            "title": (response.css("title::text").get() or "").strip(),
            "h1": [h.strip() for h in response.css("h1::text").getall() if h.strip()],
            "links": [
                normalize(urljoin(url, href))
                for href in response.css("a::attr(href)").getall()
            ],
            "scraped_at": datetime.utcnow().isoformat(),
        }

        for href in response.css("a::attr(href)").getall():
            abs_url = normalize(urljoin(url, href))
            if any(abs_url.startswith(p) for p in self.prefixes):
                yield response.follow(abs_url, callback=self.parse)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape all pages under one or more URL prefixes.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("urls", nargs="+", help="Base URL(s) to scrape")
    parser.add_argument("--max-pages", type=int, default=500, help="Max pages total (default: 500)")
    parser.add_argument("--delay", type=float, default=0.5, help="Download delay in seconds (default: 0.5)")
    parser.add_argument("--output-dir", default="output", help="Directory to write results (default: output/)")
    parser.add_argument("--format", choices=["jsonlines", "json", "csv"], default="jsonlines",
                        help="Output format (default: jsonlines)")
    args = parser.parse_args()

    start_urls = []
    prefixes = []
    for url in args.urls:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        prefix = make_prefix(url)
        start_urls.append(prefix)
        prefixes.append(prefix)

    # Build a FEEDS dict: one file per input URL, inside output/<slug>/
    ext = {"jsonlines": "jsonl", "json": "json", "csv": "csv"}[args.format]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    feeds = {}
    for prefix in prefixes:
        folder = os.path.join(args.output_dir, slug(prefix))
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"{timestamp}.{ext}")
        feeds[path] = {"format": args.format}
        print(f"  Output -> {path}")

    process = CrawlerProcess(settings={
        "CLOSESPIDER_PAGECOUNT": args.max_pages,
        "DOWNLOAD_DELAY": args.delay,
        "AUTOTHROTTLE_ENABLED": True,
    })

    process.crawl(PrefixSpider, start_urls=start_urls, prefixes=prefixes, feeds=feeds)
    process.start()


if __name__ == "__main__":
    main()
