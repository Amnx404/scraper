import json
import os
import re
import sys
import time
from collections import deque
from datetime import datetime
from urllib.parse import urldefrag, urljoin, urlparse

import yaml
from firecrawl import Firecrawl


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
    return {
        "output_dir": "output",
        "max_pages": 500,
        "delay": 0.5,
        **cfg,
    }


def main() -> None:
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"

    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        sys.exit(1)

    cfg = load_config(config_path)

    if not cfg.get("base_urls"):
        print("No base_urls specified in config.")
        sys.exit(1)

    if not cfg.get("api_key"):
        print("No api_key specified in config.")
        sys.exit(1)

    app = Firecrawl(api_key=cfg["api_key"])
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
                    data = app.scrape(
                        norm,
                        only_main_content=False,
                        formats=["markdown", "links"],
                    )

                    for link in data.get("links", []):
                        abs_link = normalize(link if link.startswith("http") else urljoin(norm, link))
                        if abs_link.startswith(prefix) and abs_link not in visited:
                            queue.append(abs_link)

                    fh.write(json.dumps({
                        "url": norm,
                        "markdown": data.get("markdown"),
                        "metadata": data.get("metadata", {}),
                        "links": data.get("links", []),
                        "scraped_at": datetime.utcnow().isoformat(),
                    }) + "\n")
                    fh.flush()

                except Exception as e:
                    print(f"  Error: {e}")

                time.sleep(cfg["delay"])

        print(f"Done. {len(visited)} pages scraped.")


if __name__ == "__main__":
    main()
