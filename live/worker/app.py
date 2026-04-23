"""Procrastinate application object (Postgres-backed job queue)."""

from __future__ import annotations

import os

from procrastinate import App, PsycopgConnector


def _normalize_database_url(url: str) -> str:
    u = url.strip()
    if u.startswith("postgres://"):
        return "postgresql://" + u[len("postgres://") :]
    return u


def _connector() -> PsycopgConnector:
    dsn = (os.environ.get("DATABASE_URL") or "").strip()
    if dsn:
        return PsycopgConnector(conninfo=_normalize_database_url(dsn))
    return PsycopgConnector()


procrastinate_app = App(connector=_connector(), import_paths=["live"])

# Ensure ``@procrastinate_app.task`` handlers are registered when the worker loads only this module.
import live.worker.tasks as _live_worker_tasks  # noqa: F401, E402


def database_url_configured() -> bool:
    return bool((os.environ.get("DATABASE_URL") or "").strip())
