"""Async BFS crawl pipeline using Obscura via Playwright CDP.

Each worker gets its own Playwright BrowserContext (separate cookie jar /
fingerprint) so Obscura's per-session fingerprint randomisation applies
independently.  Workers share a single asyncio.Queue; children are enqueued
before task_done() so queue.join() is safe.
"""

from __future__ import annotations

import asyncio
import fnmatch
import re
import secrets
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import Browser

from liveapp.db import PageDB
from liveapp.schemas import PageResult, SeedConfig, SessionSummary
from .scraper import _normalize, fetch_page

_ASSET_PATTERNS = [
    "*.css", "*.js", "*.svg", "*.png", "*.jpg", "*.jpeg",
    "*.gif", "*.webp", "*.ico", "*.pdf", "*.zip",
    "*.woff", "*.woff2", "*.ttf", "*.eot", "*.otf",
]


def _is_asset(url: str) -> bool:
    path = urlparse(url).path.lower()
    return any(fnmatch.fnmatch(path, p) for p in _ASSET_PATTERNS)


def _safe_slug(text: str, maxlen: int = 80) -> str:
    return re.sub(r"[^\w\-]", "_", text).strip("_")[:maxlen]


def _seed_for(url: str, seeds: list[SeedConfig]) -> SeedConfig | None:
    for s in seeds:
        if url.startswith(s.url):
            return s
    return None


async def run_crawl(
    *,
    browser: Browser,
    seeds: list[SeedConfig],
    max_pages: int = 500,
    workers: int = 4,
    delay: float = 0.3,
    force_rescrape: bool = False,
    db: PageDB,
    out_root: Path,
    stealth: bool = True,
    wait_until: str = "networkidle",
) -> SessionSummary:
    session_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S") + "_" + secrets.token_hex(3)
    started_at = datetime.utcnow().isoformat()

    visited: set[str] = set()
    visited_lock = asyncio.Lock()
    seed_queued: dict[str, int] = {s.url: 0 for s in seeds}

    counts: dict[str, int] = defaultdict(int)
    by_purpose: dict[str, int] = defaultdict(int)
    counts_lock = asyncio.Lock()

    # asyncio.Queue — items are (url, SeedConfig, depth) | None sentinel
    queue: asyncio.Queue[tuple[str, SeedConfig, int] | None] = asyncio.Queue()

    for seed in seeds:
        norm = _normalize(seed.url)
        visited.add(norm)
        seed_queued[seed.url] = 1
        await queue.put((norm, seed, 0))

    def _save(result: PageResult, markdown_path: str | None) -> None:
        db.upsert_page(result, markdown_path)

    async def _worker() -> None:
        # Each worker owns its own context → separate fingerprint per session.
        context = await browser.new_context()
        page = await context.new_page()
        try:
            while True:
                item = await queue.get()
                if item is None:
                    queue.task_done()
                    break

                url, seed, depth = item
                last_scraped = None if force_rescrape else db.get_last_scraped_at(url)

                result = await fetch_page(
                    url=url,
                    seed_url=seed.url,
                    purpose=seed.purpose,
                    depth=depth,
                    page=page,
                    last_scraped_at=last_scraped,
                    force=force_rescrape,
                    wait_until=wait_until,
                    use_lp_markdown=True,
                )

                # --- Save markdown to disk ---
                markdown_path: str | None = None
                markdown = result.markdown
                if result.status == "not_modified" and not markdown:
                    markdown = db.get_cached_markdown(url)
                if markdown:
                    purpose_dir = out_root / _safe_slug(result.purpose)
                    purpose_dir.mkdir(parents=True, exist_ok=True)
                    parsed = urlparse(url)
                    fname = _safe_slug(parsed.netloc + parsed.path)
                    markdown_path = str(purpose_dir / f"{fname}.md")
                    Path(markdown_path).write_text(markdown, encoding="utf-8")
                    # Attach so DB stores the body for future not_modified reuse.
                    if result.status == "not_modified":
                        result = result.model_copy(update={"markdown": markdown})

                _save(result, markdown_path)

                async with counts_lock:
                    counts[result.status] += 1
                    if result.status == "scraped":
                        by_purpose[result.purpose] += 1

                icon = {"scraped": "✓", "not_modified": "~", "skipped": "-", "error": "✗"}.get(
                    result.status, "?"
                )
                print(
                    f"  [{icon}] [{result.purpose}] depth={depth}  {url}"
                    + (f"\n       ↳ {result.error}" if result.error else "")
                )

                # --- Enqueue children BEFORE task_done ---
                if result.status == "scraped" and depth < seed.depth:
                    seed_limit = seed.max_pages or max_pages
                    for link in result.links:
                        if _is_asset(link) or not link.startswith(seed.url):
                            continue
                        if not seed.path_allowed(link):
                            continue
                        norm = _normalize(link)
                        async with visited_lock:
                            global_full = len(visited) >= max_pages
                            seed_full = seed_queued.get(seed.url, 0) >= seed_limit
                            if norm not in visited and not global_full and not seed_full:
                                visited.add(norm)
                                seed_queued[seed.url] = seed_queued.get(seed.url, 0) + 1
                                await queue.put((norm, seed, depth + 1))

                queue.task_done()
                await asyncio.sleep(delay)
        finally:
            await context.close()

    worker_tasks = [asyncio.create_task(_worker()) for _ in range(workers)]

    await queue.join()

    for _ in worker_tasks:
        await queue.put(None)
    await asyncio.gather(*worker_tasks)

    finished_at = datetime.utcnow().isoformat()

    return SessionSummary(
        session_id=session_id,
        started_at=started_at,
        finished_at=finished_at,
        total_queued=len(visited),
        scraped=counts["scraped"],
        not_modified=counts["not_modified"],
        skipped=counts["skipped"],
        errors=counts["error"],
        by_purpose=dict(by_purpose),
        output_dir=str(out_root),
        db_path=db._path,
    )
