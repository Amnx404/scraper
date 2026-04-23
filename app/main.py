"""ASGI entry (backward compatible). Prefer ``uvicorn live.api.main:app``."""

from live.api.main import app

__all__ = ["app"]
