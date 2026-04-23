"""Run artifact layout and durable JSON state under ``LIVE_RUNS_ROOT`` (default ``<repo>/app_runs``)."""

from __future__ import annotations

import json
import os
import secrets
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from live.settings import get_settings


def utc_now() -> datetime:
    return datetime.now(UTC)


def new_run_id() -> str:
    return utc_now().strftime("%Y%m%d_%H%M%S") + "_" + secrets.token_hex(4)


@dataclass(frozen=True)
class RunPaths:
    run_id: str
    run_dir: Path
    state_path: Path

    scrape_dir: Path
    scrape_config_path: Path
    scrape_log_path: Path
    scrape_err_path: Path

    prepare_dir: Path
    prepare_log_path: Path
    prepare_err_path: Path

    upload_log_path: Path
    upload_err_path: Path


def paths_for_run(run_id: str) -> RunPaths:
    run_dir = get_settings().resolved_runs_root() / run_id
    return RunPaths(
        run_id=run_id,
        run_dir=run_dir,
        state_path=run_dir / "state.json",
        scrape_dir=run_dir / "scrape_output",
        scrape_config_path=run_dir / "scrape_config.yaml",
        scrape_log_path=run_dir / "scrape.stdout.log",
        scrape_err_path=run_dir / "scrape.stderr.log",
        prepare_dir=run_dir / "ingestion",
        prepare_log_path=run_dir / "prepare.stdout.log",
        prepare_err_path=run_dir / "prepare.stderr.log",
        upload_log_path=run_dir / "upload.stdout.log",
        upload_err_path=run_dir / "upload.stderr.log",
    )


def ensure_run_dirs(p: RunPaths) -> None:
    p.run_dir.mkdir(parents=True, exist_ok=True)
    p.scrape_dir.mkdir(parents=True, exist_ok=True)


def read_state(p: RunPaths) -> dict[str, Any]:
    if not p.state_path.exists():
        return {"run_id": p.run_id, "created_at": utc_now().isoformat()}
    return json.loads(p.state_path.read_text(encoding="utf-8"))


def write_state(p: RunPaths, state: dict[str, Any]) -> None:
    p.run_dir.mkdir(parents=True, exist_ok=True)
    tmp = p.state_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, p.state_path)


def update_state(p: RunPaths, patch: dict[str, Any]) -> dict[str, Any]:
    state = read_state(p)
    state.update(patch)
    write_state(p, state)
    return state


def merge_state_key(p: RunPaths, key: str, patch: dict[str, Any]) -> dict[str, Any]:
    state = read_state(p)
    cur = state.get(key)
    if not isinstance(cur, dict):
        cur = {}
    state[key] = {**cur, **patch}
    write_state(p, state)
    return state


def run_subprocess(
    *,
    argv: list[str],
    cwd: Path,
    env: dict[str, str] | None,
    stdout_path: Path,
    stderr_path: Path,
) -> int:
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    with stdout_path.open("w", encoding="utf-8") as out, stderr_path.open("w", encoding="utf-8") as err:
        proc = subprocess.run(
            argv,
            cwd=str(cwd),
            env=env,
            stdout=out,
            stderr=err,
            text=True,
        )
    return int(proc.returncode)


def write_scrape_config_yaml(p: RunPaths, cfg: dict[str, Any]) -> None:
    p.scrape_config_path.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")


def guess_pages_dir_from_scrape_output(scrape_dir: Path) -> Path | None:
    pages_root = scrape_dir / "pages"
    if not pages_root.is_dir():
        return None
    candidates = [d for d in pages_root.iterdir() if d.is_dir()]
    if not candidates:
        return None
    return sorted(candidates)[-1]


def pinecone_staging_namespace(live_prefix: str, explicit: str | None) -> str:
    if explicit and explicit.strip():
        return explicit.strip()
    return f"{live_prefix}staging"
