import os
import re
import sys
from datetime import datetime
from urllib.parse import urldefrag, urljoin, urlparse

import scrapy
import yaml
from scrapy.crawler import CrawlerProcess


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


class PrefixSpider(scrapy.Spider):
    name = "prefix_spider"

    def __init__(self, start_urls, prefixes, feeds, settings_override, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.prefixes = prefixes
        self.custom_settings = {**settings_override, "FEEDS": feeds}

    def parse(self, response):
        url = normalize(response.url)
        if not any(url.startswith(p) for p in self.prefixes):
            return

        yield {
            "url": url,
            "status": response.status,
            "title": (response.css("title::text").get() or "").strip(),
            "h1": [h.strip() for h in response.css("h1::text").getall() if h.strip()],
            "links": [normalize(urljoin(url, h)) for h in response.css("a::attr(href)").getall()],
            "scraped_at": datetime.utcnow().isoformat(),
        }

        for href in response.css("a::attr(href)").getall():
            abs_url = normalize(urljoin(url, href))
            if any(abs_url.startswith(p) for p in self.prefixes):
                yield response.follow(abs_url, callback=self.parse)


def load_config(path: str) -> dict:
    with open(path) as f:
        cfg = yaml.safe_load(f)

    defaults = {
        "output_dir": "output",
        "format": "jsonlines",
        "max_pages": 500,
        "delay": 0.5,
        "obey_robots": True,
        "user_agent": "python-domain-scraper/1.0",
    }
    return {**defaults, **cfg}


def main() -> None:
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"

    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        sys.exit(1)

    cfg = load_config(config_path)

    if not cfg.get("urls"):
        print("No URLs specified in config.")
        sys.exit(1)

    prefixes = [make_prefix(u) for u in cfg["urls"]]
    ext = {"jsonlines": "jsonl", "json": "json", "csv": "csv"}[cfg["format"]]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    feeds = {}
    for prefix in prefixes:
        folder = os.path.join(cfg["output_dir"], slug(prefix))
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"{timestamp}.{ext}")
        feeds[path] = {"format": cfg["format"]}
        print(f"Output -> {path}")

    scrapy_settings = {
        "ROBOTSTXT_OBEY": cfg["obey_robots"],
        "USER_AGENT": cfg["user_agent"],
        "DOWNLOAD_DELAY": cfg["delay"],
        "CLOSESPIDER_PAGECOUNT": cfg["max_pages"],
        "AUTOTHROTTLE_ENABLED": True,
        "LOG_LEVEL": "INFO",
    }

    process = CrawlerProcess()
    process.crawl(
        PrefixSpider,
        start_urls=prefixes,
        prefixes=prefixes,
        feeds=feeds,
        settings_override=scrapy_settings,
    )
    process.start()


if __name__ == "__main__":
    main()
