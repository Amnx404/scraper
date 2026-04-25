"""Request / response models for the Obscura-backed scraping API."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, Field

# Re-export SeedConfig so callers only need to import from this module.
from liveapp.schemas import SeedConfig, SessionSummary


# ---------------------------------------------------------------------------
# Single-page scrape
# ---------------------------------------------------------------------------

class ScrapeRequest(BaseModel):
    url: str
    stealth: bool = True
    wait_until: Literal["load", "domcontentloaded", "networkidle"] = "networkidle"
    timeout: int = 30_000                   # ms
    use_lp_markdown: bool = True            # prefer Obscura LP.getMarkdown over html2text


class ScrapeResponse(BaseModel):
    url: str
    status: Literal["scraped", "not_modified", "skipped", "error"]
    title: str | None = None
    markdown: str | None = None
    links: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    content_hash: str | None = None
    last_modified: str | None = None
    scraped_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    error: str | None = None
    engine: str = "obscura"


# ---------------------------------------------------------------------------
# BFS crawl job
# ---------------------------------------------------------------------------

class CrawlRequest(BaseModel):
    seeds: list[SeedConfig]

    # Global URL prefix whitelist — any discovered link whose URL starts with
    # one of these is followed, even if it belongs to a different domain than
    # the originating seed.  Mirrors the original roboracer `allowed_prefixes`
    # config.  When empty the per-seed url + allowed_pages rules apply instead.
    global_allowed_prefixes: list[str] = Field(default_factory=list)

    max_pages: int = 500
    workers: int = 4                        # concurrent Playwright pages
    delay: float = 0.3                      # seconds between page fetches per worker
    force_rescrape: bool = False
    db_path: str = "obscuraapp.db"
    output_dir: str = "obscura_output"
    stealth: bool = True
    wait_until: Literal["load", "domcontentloaded", "networkidle"] = "networkidle"


class CrawlJob(BaseModel):
    job_id: str
    status: Literal["queued", "running", "done", "error"]
    started_at: str
    finished_at: str | None = None
    config: CrawlRequest
    summary: SessionSummary | None = None
    error: str | None = None


# ---------------------------------------------------------------------------
# Pages query
# ---------------------------------------------------------------------------

class PageRecord(BaseModel):
    url: str
    purpose: str
    depth: int
    status: str
    title: str | None = None
    markdown_path: str | None = None
    last_scraped_at: str
    last_modified: str | None = None
    scraped_count: int
    links_found: int


class PagesResponse(BaseModel):
    total: int
    pages: list[PageRecord]
