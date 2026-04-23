from __future__ import annotations

import os
from typing import Any


def _normalize_database_url(url: str) -> str:
    u = url.strip()
    if u.startswith("postgres://"):
        return "postgresql://" + u[len("postgres://") :]
    return u


def fetch_procrastinate_job(job_id: int) -> dict[str, Any] | None:
    """Read a single row from ``procrastinate_jobs`` (requires ``DATABASE_URL``)."""
    dsn = (os.environ.get("DATABASE_URL") or "").strip()
    if not dsn:
        return None
    import psycopg

    dsn = _normalize_database_url(dsn)
    with psycopg.connect(dsn) as conn:
        row = conn.execute(
            """
            SELECT id, status::text, task_name, queue_name, abort_requested
            FROM procrastinate_jobs
            WHERE id = %s
            """,
            (job_id,),
        ).fetchone()
    if row is None:
        return None
    return {
        "id": row[0],
        "status": row[1],
        "task_name": row[2],
        "queue_name": row[3],
        "abort_requested": row[4],
    }
