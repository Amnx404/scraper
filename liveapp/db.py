"""SQLite persistence layer.

Tables
------
pages
    One row per URL.  Tracks the last scrape time, the Last-Modified date
    the server returned, a short content hash (for change detection when the
    server doesn't send Last-Modified), and where the markdown file lives.

sessions
    One row per crawl run — useful for auditing what was scraped when.
"""

from __future__ import annotations

import json
import os
import sqlite3
import threading
from datetime import datetime
from pathlib import Path
from typing import Any

from .schemas import PageResult

_DDL = """
CREATE TABLE IF NOT EXISTS pages (
    url                 TEXT PRIMARY KEY,
    seed_url            TEXT NOT NULL,
    purpose             TEXT NOT NULL,
    depth               INTEGER NOT NULL DEFAULT 0,

    status              TEXT NOT NULL,          -- scraped | not_modified | skipped | error
    title               TEXT,
    content_hash        TEXT,                   -- sha256[:16] of raw HTML
    markdown            TEXT,                   -- full markdown body (cached for not_modified reuse)
    markdown_path       TEXT,                   -- absolute path to .md file

    last_scraped_at     TEXT NOT NULL,          -- ISO-8601 UTC; sent as If-Modified-Since
    last_modified       TEXT,                   -- Last-Modified header from server

    scraped_count       INTEGER NOT NULL DEFAULT 1,
    links_found         INTEGER NOT NULL DEFAULT 0,
    error               TEXT
);

CREATE TABLE IF NOT EXISTS sessions (
    id                  TEXT PRIMARY KEY,
    started_at          TEXT NOT NULL,
    finished_at         TEXT,
    config_json         TEXT,

    pages_scraped       INTEGER DEFAULT 0,
    pages_not_modified  INTEGER DEFAULT 0,
    pages_skipped       INTEGER DEFAULT 0,
    pages_error         INTEGER DEFAULT 0
);
"""


class PageDB:
    def __init__(self, path: str | Path) -> None:
        self._path = str(path)
        # check_same_thread=False is safe because we serialise all writes via _lock.
        self._conn = sqlite3.connect(self._path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_DDL)
        self._conn.commit()
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Page helpers
    # ------------------------------------------------------------------

    def get_page(self, url: str) -> dict[str, Any] | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM pages WHERE url = ?", (url,)
            ).fetchone()
            return dict(row) if row else None

    def get_last_scraped_at(self, url: str) -> str | None:
        """Return the stored last_scraped_at for freshness check, or None."""
        with self._lock:
            row = self._conn.execute(
                "SELECT last_scraped_at FROM pages WHERE url = ?", (url,)
            ).fetchone()
            return row["last_scraped_at"] if row else None

    def get_cached_markdown(self, url: str) -> str | None:
        """Return the stored markdown for a URL, used when the page is not_modified."""
        with self._lock:
            row = self._conn.execute(
                "SELECT markdown FROM pages WHERE url = ?", (url,)
            ).fetchone()
            return row["markdown"] if row else None

    def upsert_page(self, result: PageResult, markdown_path: str | None = None) -> None:
        with self._lock:
            existing = self._conn.execute(
                "SELECT scraped_count FROM pages WHERE url = ?", (result.url,)
            ).fetchone()
            count = (existing["scraped_count"] + 1) if existing else 1

            # For not_modified results, keep the previously stored markdown
            # (result.markdown will be None — we never re-fetched the body).
            # The UPDATE clause below uses COALESCE so it only overwrites when
            # a fresh value is actually present.
            self._conn.execute(
                """
                INSERT INTO pages
                    (url, seed_url, purpose, depth, status, title, content_hash,
                     markdown, markdown_path, last_scraped_at, last_modified,
                     scraped_count, links_found, error)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(url) DO UPDATE SET
                    status          = excluded.status,
                    title           = COALESCE(excluded.title,        title),
                    content_hash    = COALESCE(excluded.content_hash, content_hash),
                    markdown        = COALESCE(excluded.markdown,     markdown),
                    markdown_path   = COALESCE(excluded.markdown_path, markdown_path),
                    last_scraped_at = excluded.last_scraped_at,
                    last_modified   = COALESCE(excluded.last_modified, last_modified),
                    scraped_count   = excluded.scraped_count,
                    links_found     = COALESCE(excluded.links_found,  links_found),
                    error           = excluded.error
                """,
                (
                    result.url,
                    result.seed_url,
                    result.purpose,
                    result.depth,
                    result.status,
                    result.title,
                    result.content_hash,
                    result.markdown,
                    markdown_path,
                    result.scraped_at,
                    result.last_modified,
                    count,
                    len(result.links),
                    result.error,
                ),
            )
            self._conn.commit()

    # ------------------------------------------------------------------
    # Session helpers
    # ------------------------------------------------------------------

    def start_session(self, session_id: str, started_at: str, config: dict) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT OR IGNORE INTO sessions (id, started_at, config_json) VALUES (?,?,?)",
                (session_id, started_at, json.dumps(config, default=str)),
            )
            self._conn.commit()

    def finish_session(self, session_id: str, finished_at: str, counts: dict) -> None:
        with self._lock:
            self._conn.execute(
                """
                UPDATE sessions
                SET finished_at         = ?,
                    pages_scraped       = ?,
                    pages_not_modified  = ?,
                    pages_skipped       = ?,
                    pages_error         = ?
                WHERE id = ?
                """,
                (
                    finished_at,
                    counts.get("scraped", 0),
                    counts.get("not_modified", 0),
                    counts.get("skipped", 0),
                    counts.get("error", 0),
                    session_id,
                ),
            )
            self._conn.commit()

    def close(self) -> None:
        self._conn.close()
