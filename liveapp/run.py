"""Entry point: python -m liveapp [config.yaml]"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from pydantic import ValidationError

from .pipeline import run_pipeline
from .schemas import AppConfig


def main() -> None:
    config_path = sys.argv[1] if len(sys.argv) > 1 else "liveapp/config.yaml"

    if not Path(config_path).exists():
        print(f"Config not found: {config_path}")
        sys.exit(1)

    with open(config_path) as f:
        raw = yaml.safe_load(f)

    try:
        cfg = AppConfig.model_validate(raw)
    except ValidationError as exc:
        print(f"Config error:\n{exc}")
        sys.exit(1)

    print("liveapp scraper")
    print(f"  Seeds:        {len(cfg.seeds)}")
    for s in cfg.seeds:
        print(f"    [{s.purpose}] {s.url}  depth={s.depth}  allowed={s.allowed_pages}")
    print(f"  Max pages:    {cfg.max_pages}")
    print(f"  Workers:      {cfg.workers}")
    print(f"  Delay:        {cfg.delay}s")
    print(f"  Force rescrape: {cfg.force_rescrape}")
    print(f"  DB:           {cfg.db_path}")
    print(f"  Output:       {cfg.output_dir}")
    print()

    summary = run_pipeline(cfg)

    print()
    print("─" * 52)
    print(f"Session:       {summary.session_id}")
    print(f"Duration:      {summary.started_at}  →  {summary.finished_at}")
    print(f"Total queued:  {summary.total_queued}")
    print(f"Scraped:       {summary.scraped}")
    print(f"Not modified:  {summary.not_modified}  (already up-to-date in DB)")
    print(f"Skipped:       {summary.skipped}")
    print(f"Errors:        {summary.errors}")
    print(f"By purpose:    {json.dumps(summary.by_purpose, indent=2)}")
    print(f"Output dir:    {summary.output_dir}")
    print(f"DB:            {summary.db_path}")


if __name__ == "__main__":
    main()
