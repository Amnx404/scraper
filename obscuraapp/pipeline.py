"""Async BFS crawl pipeline using Obscura via Playwright CDP.

Each worker gets its own Playwright BrowserContext (separate cookie jar /
fingerprint) so Obscura's per-session fingerprint randomisation applies
independently.  Workers share a single asyncio.Queue; children are enqueued
before task_done() so queue.join() is safe.

Two link-following modes
------------------------
1. Per-seed mode (default): a discovered link is only followed if it lives
   under the originating seed's URL *and* matches its allowed_pages patterns.
   Patterns support **, e.g. /docs/** follows all subdirectories recursively.

2. Global-prefix mode (roboracer style): when global_allowed_prefixes is set,
   ANY discovered link whose URL starts with one of those prefixes is followed,
   even if it belongs to a completely different domain.  This lets a crawl of
   roboracer.ai automatically expand into f1tenth-coursekit.readthedocs.io,
   conference sites, etc. as links are encountered.  The purpose label of a
   URL is taken from the closest matching seed, falling back to "general".
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


def _best_seed(url: str, seeds: list[SeedConfig]) -> SeedConfig | None:
    """Return the seed whose URL is the longest prefix match for url."""
    match = None
    for s in seeds:
        if url.startswith(s.url):
            if match is None or len(s.url) > len(match.url):
                match = s
    return match


def _global_allowed(url: str, prefixes: list[str]) -> bool:
    return any(url.startswith(p) for p in prefixes)


def _should_follow(
    link: str,
    originating_seed: SeedConfig,
    all_seeds: list[SeedConfig],
    global_prefixes: list[str],
    depth: int,
) -> tuple[bool, SeedConfig, int]:
    """Return (should_follow, effective_seed, effective_depth).

    In global-prefix mode a link can jump to a different domain; the depth
    resets to 0 relative to the new effective seed (or stays as-is when no
    seed claims the new domain).
    """
    if _is_asset(link):
        return False, originating_seed, depth

    # --- Global-prefix mode ---
    if global_prefixes:
        if not _global_allowed(link, global_prefixes):
            return False, originating_seed, depth
        effective = _best_seed(link, all_seeds) or originating_seed
        # Depth relative to whichever seed "owns" this URL.
        new_depth = depth + 1
        if new_depth > effective.depth:
            return False, effective, new_depth
        return True, effective, new_depth

    # --- Per-seed mode ---
    if not link.startswith(originating_seed.url):
        return False, originating_seed, depth
    if not originating_seed.path_allowed(link):
        return False, originating_seed, depth
    new_depth = depth + 1
    if new_depth > originating_seed.depth:
        return False, originating_seed, new_depth
    return True, originating_seed, new_depth


async def run_crawl(
    *,
    browser: Browser,
    seeds: list[SeedConfig],
    global_allowed_prefixes: list[str] = [],
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

    counts: dict[str, int] = defaultdict(int)
    by_purpose: dict[str, int] = defaultdict(int)
    counts_lock = asyncio.Lock()

    queue: asyncio.Queue[tuple[str, SeedConfig, int] | None] = asyncio.Queue()

    # Seed with all starting URLs.
    for seed in seeds:
        norm = _normalize(seed.url)
        visited.add(norm)
        await queue.put((norm, seed, 0))

    async def _worker() -> None:
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

                # --- Persist markdown ---
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
                    if result.status == "not_modified":
                        result = result.model_copy(update={"markdown": markdown})

                db.upsert_page(result, markdown_path)

                async with counts_lock:
                    counts[result.status] += 1
                    if result.status == "scraped":
                        by_purpose[result.purpose] += 1

                icon = {"scraped": "✓", "not_modified": "~", "skipped": "-", "error": "✗"}.get(
                    result.status, "?"
                )
                mode = "global" if global_allowed_prefixes else seed.url
                print(
                    f"  [{icon}] [{result.purpose}] d={depth}  {url}"
                    + (f"\n       ↳ {result.error}" if result.error else "")
                )

                # --- Enqueue children (BEFORE task_done) ---
                if result.status == "scraped":
                    seed_limit = seed.max_pages or max_pages
                    for link in result.links:
                        norm = _normalize(link)
                        ok, eff_seed, child_depth = _should_follow(
                            norm, seed, seeds, global_allowed_prefixes, depth
                        )
                        if not ok:
                            continue
                        async with visited_lock:
                            global_full = len(visited) >= max_pages
                            if norm not in visited and not global_full:
                                visited.add(norm)
                                await queue.put((norm, eff_seed, child_depth))

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
