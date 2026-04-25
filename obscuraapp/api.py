"""FastAPI app — Obscura-backed scraping endpoints.

Startup sequence
----------------
1. `obscura serve --stealth --port 9222` is launched as a subprocess.
2. Playwright connects to it over CDP.
3. The browser object is stored on app.state and shared across all requests.

Endpoints
---------
POST /scrape          Render a single URL, return markdown + metadata.
POST /crawl           Start a BFS crawl job in the background.
GET  /crawl/{job_id}  Poll crawl job status / summary.
GET  /pages           List pages stored in the DB (filterable by purpose).
GET  /health          Liveness check.

Set OBSCURA_ENDPOINT env var to point at an already-running Obscura instance
(skips launching the subprocess).
"""

from __future__ import annotations

import asyncio
import os
import secrets
import subprocess
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from playwright.async_api import async_playwright, Browser

from liveapp.db import PageDB
from liveapp.schemas import PageResult
from .pipeline import run_crawl
from .scraper import fetch_page
from .schemas import (
    CrawlJob,
    CrawlRequest,
    PagesResponse,
    PageRecord,
    ScrapeRequest,
    ScrapeResponse,
)

# ---------------------------------------------------------------------------
# In-memory job registry (keyed by job_id)
# ---------------------------------------------------------------------------
_jobs: dict[str, CrawlJob] = {}

# ---------------------------------------------------------------------------
# Obscura process + Playwright browser lifecycle
# ---------------------------------------------------------------------------

_obscura_proc: subprocess.Popen | None = None
_playwright_ctx: Any = None


def _obscura_endpoint() -> str:
    return os.environ.get("OBSCURA_ENDPOINT", "http://localhost:9222")


@asynccontextmanager
async def _lifespan(app: FastAPI):
    global _obscura_proc, _playwright_ctx

    endpoint = _obscura_endpoint()
    launched = False

    # Launch Obscura if no external endpoint is set.
    if "OBSCURA_ENDPOINT" not in os.environ:
        port = 9222
        cmd = ["obscura", "serve", "--stealth", "--port", str(port)]
        try:
            _obscura_proc = subprocess.Popen(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            launched = True
            print(f"[obscuraapp] launched: {' '.join(cmd)}  pid={_obscura_proc.pid}")
            await asyncio.sleep(1.5)  # give Obscura time to bind
        except FileNotFoundError:
            print(
                "[obscuraapp] WARNING: 'obscura' binary not found. "
                "Download from https://github.com/h4ckf0r0day/obscura/releases "
                "or set OBSCURA_ENDPOINT to connect to a running instance."
            )

    pw = await async_playwright().start()
    _playwright_ctx = pw
    try:
        browser = await pw.chromium.connect_over_cdp(endpoint)
        app.state.browser = browser
        print(f"[obscuraapp] connected to Obscura at {endpoint}")
    except Exception as exc:
        print(f"[obscuraapp] could not connect to {endpoint}: {exc}")
        app.state.browser = None

    yield

    if app.state.browser:
        try:
            await app.state.browser.close()
        except Exception:
            pass
    await pw.stop()
    if _obscura_proc and launched:
        _obscura_proc.terminate()
        print("[obscuraapp] Obscura process terminated.")


app = FastAPI(
    title="Obscura Scraping API",
    version="1.0.0",
    description=(
        "Scrape pages through [Obscura](https://github.com/h4ckf0r0day/obscura) — "
        "a Rust headless browser with native DOM→Markdown (LP domain), "
        "built-in stealth, and 85 ms page loads."
    ),
    lifespan=_lifespan,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_browser() -> Browser:
    browser: Browser | None = getattr(app.state, "browser", None)
    if browser is None:
        raise HTTPException(503, "Obscura browser not connected. Check server logs.")
    return browser


def _new_job_id() -> str:
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S") + "_" + secrets.token_hex(4)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
async def health() -> dict:
    browser = getattr(app.state, "browser", None)
    return {
        "ok": browser is not None,
        "obscura_endpoint": _obscura_endpoint(),
        "browser_connected": browser is not None,
        "active_jobs": len([j for j in _jobs.values() if j.status == "running"]),
    }


@app.post("/scrape", response_model=ScrapeResponse)
async def scrape_url(req: ScrapeRequest) -> ScrapeResponse:
    """Render a single URL through Obscura and return markdown + metadata."""
    browser = _get_browser()
    context = await browser.new_context()
    page = await context.new_page()
    try:
        result: PageResult = await fetch_page(
            url=req.url,
            seed_url=req.url,
            purpose="adhoc",
            depth=0,
            page=page,
            last_scraped_at=None,
            force=True,
            wait_until=req.wait_until,
            timeout=req.timeout,
            use_lp_markdown=req.use_lp_markdown,
        )
    finally:
        await context.close()

    return ScrapeResponse(
        url=result.url,
        status=result.status,
        title=result.title,
        markdown=result.markdown,
        links=result.links,
        metadata=result.metadata,
        content_hash=result.content_hash,
        last_modified=result.last_modified,
        scraped_at=result.scraped_at,
        error=result.error,
        engine="obscura",
    )


@app.post("/crawl", response_model=CrawlJob, status_code=202)
async def start_crawl(req: CrawlRequest) -> CrawlJob:
    """Start a BFS crawl.  Returns immediately with a job_id to poll."""
    browser = _get_browser()
    job_id = _new_job_id()
    started_at = datetime.utcnow().isoformat()

    job = CrawlJob(
        job_id=job_id,
        status="queued",
        started_at=started_at,
        config=req,
    )
    _jobs[job_id] = job

    async def _run() -> None:
        _jobs[job_id] = _jobs[job_id].model_copy(update={"status": "running"})
        db = PageDB(req.db_path)
        db.start_session(job_id, started_at, req.model_dump(mode="json"))
        out_root = Path(req.output_dir)
        out_root.mkdir(parents=True, exist_ok=True)
        try:
            summary = await run_crawl(
                browser=browser,
                seeds=req.seeds,
                max_pages=req.max_pages,
                workers=req.workers,
                delay=req.delay,
                force_rescrape=req.force_rescrape,
                db=db,
                out_root=out_root,
                stealth=req.stealth,
                wait_until=req.wait_until,
            )
            db.finish_session(
                job_id,
                summary.finished_at or datetime.utcnow().isoformat(),
                {
                    "scraped": summary.scraped,
                    "not_modified": summary.not_modified,
                    "skipped": summary.skipped,
                    "error": summary.errors,
                },
            )
            _jobs[job_id] = _jobs[job_id].model_copy(
                update={"status": "done", "finished_at": summary.finished_at, "summary": summary}
            )
        except Exception as exc:
            _jobs[job_id] = _jobs[job_id].model_copy(
                update={"status": "error", "finished_at": datetime.utcnow().isoformat(), "error": str(exc)}
            )
        finally:
            db.close()

    asyncio.create_task(_run())
    return job


@app.get("/crawl/{job_id}", response_model=CrawlJob)
async def get_crawl(job_id: str) -> CrawlJob:
    """Poll a crawl job by ID."""
    if job_id not in _jobs:
        raise HTTPException(404, f"job_id not found: {job_id}")
    return _jobs[job_id]


@app.get("/crawl", response_model=list[CrawlJob])
async def list_crawls() -> list[CrawlJob]:
    """List all crawl jobs (most recent first)."""
    return sorted(_jobs.values(), key=lambda j: j.started_at, reverse=True)


@app.get("/pages", response_model=PagesResponse)
async def list_pages(
    db_path: str = Query("obscuraapp.db"),
    purpose: str | None = Query(None),
    status: str | None = Query(None),
    limit: int = Query(100, le=1000),
    offset: int = Query(0),
) -> PagesResponse:
    """Query pages stored in the DB."""
    if not Path(db_path).exists():
        raise HTTPException(404, f"DB not found: {db_path}")

    db = PageDB(db_path)
    try:
        clauses = []
        params: list[Any] = []
        if purpose:
            clauses.append("purpose = ?")
            params.append(purpose)
        if status:
            clauses.append("status = ?")
            params.append(status)

        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        with db._lock:
            total = db._conn.execute(
                f"SELECT COUNT(*) FROM pages {where}", params
            ).fetchone()[0]
            rows = db._conn.execute(
                f"SELECT url, purpose, depth, status, title, markdown_path, "
                f"last_scraped_at, last_modified, scraped_count, links_found "
                f"FROM pages {where} ORDER BY last_scraped_at DESC LIMIT ? OFFSET ?",
                params + [limit, offset],
            ).fetchall()
    finally:
        db.close()

    return PagesResponse(
        total=total,
        pages=[PageRecord(**dict(r)) for r in rows],
    )
