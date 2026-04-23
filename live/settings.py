"""Central configuration (12-factor): override with ``LIVE_*`` environment variables."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Process-wide settings. Defaults assume the repository layout (``app_runs/`` under repo root)."""

    model_config = SettingsConfigDict(
        env_prefix="LIVE_",
        env_file=(".env",),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    repo_root: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parents[1],
        description="Repository / deployment root (for subprocess cwd and static paths).",
    )
    runs_root: Path | None = Field(
        default=None,
        description="Per-run artifact directory. Default: ``{repo_root}/app_runs``.",
    )

    def resolved_runs_root(self) -> Path:
        return self.runs_root if self.runs_root is not None else (self.repo_root / "app_runs")


@lru_cache
def get_settings() -> Settings:
    return Settings()
