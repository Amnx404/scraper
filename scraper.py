import json
import os
import re
import sys
import time
from collections import deque
from datetime import datetime
from urllib.parse import urldefrag, urljoin, urlparse

import html2text
import requests
import yaml
from bs4 import BeautifulSoup


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


def load_config(path: str) -> dict:
    with open(path) as f:
        cfg = yaml.safe_load(f)
    return {"output_dir": "output", "max_pages": 500, "delay": 0.5, **cfg}


def scrape_page(url: str, session: requests.Session) -> dict:
    resp = session.get(url, timeout=15, allow_redirects=True)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

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
        "status_code": resp.status_code,
        "content_type": resp.headers.get("Content-Type"),
    }

    links = [
        normalize(urljoin(url, a["href"]))
        for a in soup.find_all("a", href=True)
        if not a["href"].startswith(("mailto:", "tel:", "javascript:"))
    ]

    return {"markdown": markdown.strip(), "metadata": metadata, "links": links}


def main() -> None:
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"

    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        sys.exit(1)

    cfg = load_config(config_path)

    if not cfg.get("base_urls"):
        print("No base_urls specified in config.")
        sys.exit(1)

    session = requests.Session()
    session.headers["User-Agent"] = cfg.get("user_agent", "python-domain-scraper/1.0")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for base_url in cfg["base_urls"]:
        prefix = make_prefix(base_url)
        folder = os.path.join(cfg["output_dir"], slug(prefix))
        os.makedirs(folder, exist_ok=True)
        out_path = os.path.join(folder, f"{timestamp}.jsonl")

        print(f"\nCrawling: {prefix}")
        print(f"Output:   {out_path}")

        queue: deque[str] = deque([prefix])
        visited: set[str] = set()

        with open(out_path, "w") as fh:
            while queue and len(visited) < cfg["max_pages"]:
                url = queue.popleft()
                norm = normalize(url)

                if norm in visited or not norm.startswith(prefix):
                    continue
                visited.add(norm)

                print(f"  [{len(visited)}] {norm}")
                try:
                    data = scrape_page(norm, session)

                    for link in data["links"]:
                        if link.startswith(prefix) and link not in visited:
                            queue.append(link)

                    fh.write(json.dumps({
                        "url": norm,
                        "markdown": data["markdown"],
                        "metadata": data["metadata"],
                        "links": data["links"],
                        "scraped_at": datetime.utcnow().isoformat(),
                    }) + "\n")
                    fh.flush()

                except Exception as e:
                    print(f"  Error: {e}")

                time.sleep(cfg["delay"])

        print(f"Done. {len(visited)} pages scraped.")


if __name__ == "__main__":
    main()
