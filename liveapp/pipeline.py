"""Concurrent scrape → process → save pipeline.

Architecture
------------
Three stages run simultaneously in separate threads:

  [BFS coordinator] ──puts──▶ fetch_queue
                                   │
                          N fetch workers  (threads)
                          each calls fetch_and_process()
                                   │
                              result_queue
                                   │
                           1 saver worker
                           writes markdown to disk + upserts DB

The BFS coordinator is the main thread.  It seeds fetch_queue from config,
then waits for fetch_queue to drain.  Each fetch worker enqueues child links
*before* calling task_done(), so fetch_queue.join() is safe.

Freshness
---------
Before fetching, each worker checks the DB for a stored last_scraped_at.
If found it sends ``If-Modified-Since``; a 304 bypasses all processing.

Limits
------
- Global max_pages cap (counts URLs added to visited set)
- Per-seed max_pages cap
- Per-seed depth cap
- Per-seed allowed_pages fnmatch patterns
"""

from __future__ import annotations

import fnmatch
import queue
import re
import secrets
import threading
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests

from .db import PageDB
from .scraper import fetch_and_process, normalize
from .schemas import AppConfig, PageResult, SeedConfig, SessionSummary

# Asset extensions we never want to queue.
_ASSET_PATTERNS = [
    "*.css", "*.js", "*.svg", "*.png", "*.jpg", "*.jpeg",
    "*.gif", "*.webp", "*.ico", "*.pdf", "*.zip",
    "*.woff", "*.woff2", "*.ttf", "*.eot", "*.otf",
]


def _is_asset(url: str) -> bool:
    path = urlparse(url).path.lower()
    return any(fnmatch.fnmatch(path, pat) for pat in _ASSET_PATTERNS)


def _safe_slug(text: str, maxlen: int = 80) -> str:
    return re.sub(r"[^\w\-]", "_", text).strip("_")[:maxlen]


def run_pipeline(cfg: AppConfig) -> SessionSummary:
    session_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S") + "_" + secrets.token_hex(3)
    started_at = datetime.utcnow().isoformat()

    db = PageDB(cfg.db_path)
    db.start_session(session_id, started_at, cfg.model_dump(mode="json"))

    out_root = Path(cfg.output_dir)
    out_root.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Shared state (all protected by visited_lock or counts_lock)
    # ------------------------------------------------------------------
    visited: set[str] = set()
    visited_lock = threading.Lock()

    # How many pages each seed has had *started* (queued into visited).
    seed_queued: dict[str, int] = {s.url: 0 for s in cfg.seeds}

    counts: dict[str, int] = defaultdict(int)
    by_purpose: dict[str, int] = defaultdict(int)
    counts_lock = threading.Lock()

    # ------------------------------------------------------------------
    # Queues
    # ------------------------------------------------------------------
    # Items: (url, SeedConfig, depth) | None (sentinel)
    fetch_queue: queue.Queue[tuple[str, SeedConfig, int] | None] = queue.Queue()
    # Items: PageResult | None (sentinel)
    result_queue: queue.Queue[PageResult | None] = queue.Queue()

    # ------------------------------------------------------------------
    # Seed the fetch queue
    # ------------------------------------------------------------------
    for seed in cfg.seeds:
        norm = normalize(seed.url)
        visited.add(norm)
        seed_queued[seed.url] += 1
        fetch_queue.put((norm, seed, 0))

    # ------------------------------------------------------------------
    # Fetch worker — one per cfg.workers threads
    # ------------------------------------------------------------------
    def _fetch_worker() -> None:
        # Each thread gets its own HTTP session (requests.Session isn't thread-safe).
        http = requests.Session()
        http.headers["User-Agent"] = cfg.user_agent

        while True:
            item = fetch_queue.get()
            if item is None:
                fetch_queue.task_done()
                break

            url, seed, depth = item
            last_scraped = None if cfg.force_rescrape else db.get_last_scraped_at(url)

            result = fetch_and_process(
                url=url,
                seed_url=seed.url,
                purpose=seed.purpose,
                depth=depth,
                session=http,
                last_scraped_at=last_scraped,
                force=cfg.force_rescrape,
            )
            result_queue.put(result)

            # Enqueue child links — must happen BEFORE task_done() so that
            # fetch_queue.join() doesn't return prematurely.
            if result.status == "scraped" and depth < seed.depth:
                seed_limit = seed.max_pages or cfg.max_pages
                for link in result.links:
                    if _is_asset(link):
                        continue
                    if not link.startswith(seed.url):
                        continue
                    if not seed.path_allowed(link):
                        continue
                    norm = normalize(link)
                    with visited_lock:
                        global_full = len(visited) >= cfg.max_pages
                        seed_full = seed_queued.get(seed.url, 0) >= seed_limit
                        if norm not in visited and not global_full and not seed_full:
                            visited.add(norm)
                            seed_queued[seed.url] = seed_queued.get(seed.url, 0) + 1
                            fetch_queue.put((norm, seed, depth + 1))

            fetch_queue.task_done()
            time.sleep(cfg.delay)

    # ------------------------------------------------------------------
    # Saver worker — single thread; writes markdown + upserts DB
    # ------------------------------------------------------------------
    def _saver_worker() -> None:
        while True:
            result = result_queue.get()
            if result is None:
                result_queue.task_done()
                break

            # For not_modified pages the scraper didn't re-fetch the body,
            # but the content is already in the DB.  Load it so we can still
            # write it to the output folder — scraping was the expensive step,
            # not saving.
            if result.status == "not_modified" and result.markdown is None:
                cached = db.get_cached_markdown(result.url)
                if cached:
                    result = result.model_copy(update={"markdown": cached})

            markdown_path: str | None = None
            if result.markdown:
                purpose_dir = out_root / _safe_slug(result.purpose)
                purpose_dir.mkdir(parents=True, exist_ok=True)
                parsed = urlparse(result.url)
                fname = _safe_slug(parsed.netloc + parsed.path)
                markdown_path = str(purpose_dir / f"{fname}.md")
                Path(markdown_path).write_text(result.markdown, encoding="utf-8")

            db.upsert_page(result, markdown_path)

            with counts_lock:
                counts[result.status] += 1
                if result.status == "scraped":
                    by_purpose[result.purpose] += 1

            _icon = {"scraped": "✓", "not_modified": "~", "skipped": "-", "error": "✗"}.get(
                result.status, "?"
            )
            print(
                f"  [{_icon}] [{result.purpose}] depth={result.depth}  {result.url}"
                + (f"\n       ↳ {result.error}" if result.error else "")
            )

            result_queue.task_done()

    # ------------------------------------------------------------------
    # Launch threads
    # ------------------------------------------------------------------
    fetch_threads = [
        threading.Thread(target=_fetch_worker, daemon=True, name=f"fetch-{i}")
        for i in range(cfg.workers)
    ]
    saver_thread = threading.Thread(target=_saver_worker, daemon=True, name="saver")

    saver_thread.start()
    for t in fetch_threads:
        t.start()

    # Wait for all fetch tasks (including dynamically added children) to finish.
    fetch_queue.join()

    # Signal fetch workers to stop.
    for _ in fetch_threads:
        fetch_queue.put(None)
    for t in fetch_threads:
        t.join()

    # Signal saver to stop and wait for all DB writes to finish.
    result_queue.put(None)
    saver_thread.join()

    # ------------------------------------------------------------------
    # Wrap up
    # ------------------------------------------------------------------
    finished_at = datetime.utcnow().isoformat()
    db.finish_session(session_id, finished_at, dict(counts))
    db.close()

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
        db_path=cfg.db_path,
    )
