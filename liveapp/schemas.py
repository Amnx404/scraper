from __future__ import annotations

import fnmatch
from datetime import datetime
from typing import Any, Literal
from urllib.parse import urlparse

from pydantic import BaseModel, Field, model_validator


class SeedConfig(BaseModel):
    """One entry in config.yaml seeds list.

    Each seed represents a base URL with its own purpose label, crawl depth,
    allowed page patterns, and optional page cap.  The `purpose` field is the
    category / type of content at this URL (e.g. "documentation", "blog",
    "api-reference") — stored on every scraped page in the DB.
    """

    url: str
    purpose: str = "general"                        # what this content is *about*
    depth: int = 3                                  # max BFS hops from the seed
    allowed_pages: list[str] = Field(default_factory=lambda: ["*"])  # fnmatch on path
    max_pages: int | None = None                    # per-seed cap; falls back to global

    @model_validator(mode="after")
    def _normalise_url(self) -> SeedConfig:
        if not self.url.endswith("/"):
            self.url = self.url + "/"
        return self

    def path_allowed(self, url: str) -> bool:
        """Return True if the URL's path matches any allowed_pages pattern."""
        path = urlparse(url).path
        return any(fnmatch.fnmatch(path, pat) for pat in self.allowed_pages)


class AppConfig(BaseModel):
    seeds: list[SeedConfig]

    output_dir: str = "liveapp_output"
    db_path: str = "liveapp.db"

    max_pages: int = 500          # global cap across all seeds
    delay: float = 0.5            # seconds between requests per worker
    user_agent: str = "liveapp-scraper/1.0"
    workers: int = 4              # concurrent fetch threads

    # Set true to ignore DB freshness and re-scrape every URL unconditionally.
    force_rescrape: bool = False


# ---------------------------------------------------------------------------
# Per-page result (produced by scraper, consumed by pipeline saver)
# ---------------------------------------------------------------------------

class PageResult(BaseModel):
    url: str
    seed_url: str
    purpose: str
    depth: int

    status: Literal["scraped", "not_modified", "skipped", "error"]
    title: str | None = None
    markdown: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    links: list[str] = Field(default_factory=list)

    content_hash: str | None = None
    last_modified: str | None = None           # value from Last-Modified header
    scraped_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    error: str | None = None

    @property
    def markdown_chars(self) -> int:
        return len(self.markdown) if self.markdown else 0


# ---------------------------------------------------------------------------
# Session-level summary returned after a full crawl
# ---------------------------------------------------------------------------

class SessionSummary(BaseModel):
    session_id: str
    started_at: str
    finished_at: str | None = None

    total_queued: int = 0
    scraped: int = 0
    not_modified: int = 0
    skipped: int = 0
    errors: int = 0

    # Breakdown of scraped pages by purpose label
    by_purpose: dict[str, int] = Field(default_factory=dict)

    output_dir: str
    db_path: str
