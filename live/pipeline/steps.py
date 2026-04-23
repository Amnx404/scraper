from __future__ import annotations

import argparse
import contextlib
import json
import os
import re
import traceback
from pathlib import Path
from unittest.mock import patch

from live.domain.schemas import ApiStatus, PrepareRequest, ScrapeRequest, UploadRequest
from live.engines import browserless_crawler, pinecone_upsert, prepare_ingestion
from live.integrations.pinecone_namespaces import compute_next_live_namespace
from live.storage.runs import (
    RunPaths,
    guess_pages_dir_from_scrape_output,
    pinecone_staging_namespace,
    read_state,
    update_state,
    utc_now,
    write_scrape_config_yaml,
    write_state,
)


@contextlib.contextmanager
def _capture_stdio(stdout_path: Path, stderr_path: Path):
    class _Writer:
        __slots__ = ("_fp",)

        def __init__(self, fp):
            self._fp = fp

        def write(self, s: str) -> int:
            n = self._fp.write(s)
            self._fp.flush()
            return n

        def flush(self) -> None:
            self._fp.flush()

    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    with stdout_path.open("w", encoding="utf-8") as out, stderr_path.open("w", encoding="utf-8") as err:
        with contextlib.redirect_stdout(_Writer(out)), contextlib.redirect_stderr(_Writer(err)):
            yield


_UPSERT_COMPLETE_RE = re.compile(
    r"Upsert complete:\s+"
    r"(?P<chunk_vectors>\d+)\s+chunk vectors across\s+"
    r"(?P<processed_urls>\d+)\s+URLs\s+"
    r"\(skipped\s+(?P<skipped_urls>\d+)\s+empty pages\)\."
)


def cancel_flag_path(p: RunPaths) -> Path:
    return p.run_dir / ".cancel_requested"


def cancel_requested(p: RunPaths) -> bool:
    return cancel_flag_path(p).is_file()


def record_step_api_response(p: RunPaths, step: str, status: ApiStatus) -> None:
    state = read_state(p)
    responses = state.get("step_responses")
    if not isinstance(responses, dict):
        responses = {}
    state["step_responses"] = {**responses, step: api_status_to_jsonable(status)}
    write_state(p, state)


def prepare_subprocess_env(req: PrepareRequest, base: dict[str, str]) -> dict[str, str]:
    env = dict(base)
    env.pop("FINETUNE_API_KEY", None)
    env.pop("OPENAI_API_KEY", None)
    if req.finetune:
        key = (env.get("OPENROUTER_API_KEY") or "").strip()
        if not key:
            raise ValueError(
                "When finetune is true, set OPENROUTER_API_KEY in the environment."
            )
    if (req.finetune_model or "").strip():
        env["FINETUNE_MODEL"] = req.finetune_model.strip()
    if (req.openrouter_model or "").strip():
        env["OPENROUTER_MODEL"] = req.openrouter_model.strip()
    if req.finetune and req.finetune_prompt is not None:
        env["FINETUNE_PROMPT"] = req.finetune_prompt.strip()
    return env


def execute_scrape(p: RunPaths, req: ScrapeRequest) -> ApiStatus:
    run_id = p.run_id
    started = utc_now()
    update_state(
        p,
        {
            "run_id": run_id,
            "created_at": started.isoformat(),
            "scrape": {"status": "started", "started_at": started.isoformat()},
            "paths": {
                "run_dir": str(p.run_dir),
                "scrape_dir": str(p.scrape_dir),
                "scrape_config": str(p.scrape_config_path),
                "scrape_stdout": str(p.scrape_log_path),
                "scrape_stderr": str(p.scrape_err_path),
            },
        },
    )

    cfg = req.model_dump()
    cfg["output_dir"] = str(p.scrape_dir)
    cfg["page_output_subdir"] = "pages"
    cfg["global_status_filename"] = "crawl_status.json"
    cfg["resume"] = False
    cfg["page_fetcher"] = "browserless"
    write_scrape_config_yaml(p, cfg)

    try:
        with _capture_stdio(p.scrape_log_path, p.scrape_err_path):
            code = browserless_crawler.run_browserless_crawl(cfg)
    except Exception:
        with p.scrape_err_path.open("a", encoding="utf-8") as ef:
            ef.write(traceback.format_exc())
        code = 1

    pages_dir = guess_pages_dir_from_scrape_output(p.scrape_dir)
    finished = utc_now()
    ok = code == 0 and pages_dir is not None

    crawl_status_path = p.scrape_dir / "crawl_status.json"
    crawl_status: dict | None = None
    if crawl_status_path.is_file():
        try:
            crawl_status = json.loads(crawl_status_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            crawl_status = None

    scraped_total = None
    scraped_ok = None
    if isinstance(crawl_status, dict) and isinstance(crawl_status.get("urls"), dict):
        urls = crawl_status["urls"]
        scraped_total = len(urls)
        scraped_ok = sum(1 for v in urls.values() if isinstance(v, dict) and v.get("status") == "ok")
    update_state(
        p,
        {
            "scrape": {
                "status": "ok" if ok else "error",
                "exit_code": code,
                "started_at": started.isoformat(),
                "finished_at": finished.isoformat(),
                "pages_dir": str(pages_dir) if pages_dir else None,
                "scraped_total": scraped_total,
                "scraped_ok": scraped_ok,
            }
        },
    )

    status = ApiStatus(
        ok=ok,
        step="scrape",
        run_id=run_id,
        started_at=started,
        finished_at=finished,
        message="scrape complete" if ok else "scrape failed",
        outputs={
            "run_dir": str(p.run_dir),
            "scrape_dir": str(p.scrape_dir),
            "pages_dir": str(pages_dir) if pages_dir else None,
            "config": cfg,
            "crawl_status": crawl_status,
            "counts": {"total": scraped_total, "ok": scraped_ok},
        },
        logs={"stdout": str(p.scrape_log_path), "stderr": str(p.scrape_err_path)},
    )
    record_step_api_response(p, "scrape", status)
    return status


def execute_prepare(p: RunPaths, req: PrepareRequest) -> ApiStatus:
    if not p.run_dir.exists():
        raise FileNotFoundError(f"run_id not found: {req.run_id}")

    started = utc_now()
    input_pages_dir = (
        Path(req.input_pages_dir) if req.input_pages_dir else guess_pages_dir_from_scrape_output(p.scrape_dir)
    )
    if input_pages_dir is None or not input_pages_dir.is_dir():
        raise ValueError("Could not resolve input_pages_dir; pass input_pages_dir explicitly.")

    out_dir = p.run_dir / req.output_subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    update_state(
        p,
        {
            "prepare": {
                "status": "started",
                "started_at": started.isoformat(),
                "input_pages_dir": str(input_pages_dir),
                "output_dir": str(out_dir),
            }
        },
    )

    merged_env = prepare_subprocess_env(req, os.environ.copy())
    try:
        with patch.dict(os.environ, merged_env, clear=True):
            with _capture_stdio(p.prepare_log_path, p.prepare_err_path):
                code = prepare_ingestion.run_prepare_ingestion(
                    input_dir=input_pages_dir,
                    output_dir=out_dir,
                    min_chars=req.min_chars,
                    keep_binary=req.keep_binary,
                    finetune=req.finetune,
                    finetune_concurrency=req.finetune_concurrency,
                    finetune_max_input_chars=req.finetune_max_input_chars,
                )
    except Exception:
        with p.prepare_err_path.open("a", encoding="utf-8") as ef:
            ef.write(traceback.format_exc())
        code = 1
    finished = utc_now()
    ok = code == 0 and (out_dir / "manifest.jsonl").is_file()

    summary: dict | None = None
    summary_path = out_dir / "summary.json"
    if summary_path.is_file():
        try:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            summary = None

    manifest_rows: list[dict] | None = None
    manifest_path = out_dir / "manifest.jsonl"
    if manifest_path.is_file():
        rows: list[dict] = []
        with manifest_path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        manifest_rows = rows

    doc_count = len(manifest_rows) if isinstance(manifest_rows, list) else None
    finetuned_count = None
    if isinstance(manifest_rows, list):
        finetuned_count = sum(1 for r in manifest_rows if isinstance(r, dict) and r.get("fine_markdown_path"))
    update_state(
        p,
        {
            "prepare": {
                "status": "ok" if ok else "error",
                "exit_code": code,
                "started_at": started.isoformat(),
                "finished_at": finished.isoformat(),
                "input_pages_dir": str(input_pages_dir),
                "output_dir": str(out_dir),
                "documents": doc_count,
                "finetuned": finetuned_count,
            }
        },
    )

    status = ApiStatus(
        ok=ok,
        step="prepare",
        run_id=req.run_id,
        started_at=started,
        finished_at=finished,
        message="prepare complete" if ok else "prepare failed",
        outputs={
            "run_dir": str(p.run_dir),
            "input_pages_dir": str(input_pages_dir),
            "ingestion_dir": str(out_dir),
            "summary": summary,
            "manifest": manifest_rows,
            "counts": {"documents": doc_count, "finetuned": finetuned_count},
        },
        logs={"stdout": str(p.prepare_log_path), "stderr": str(p.prepare_err_path)},
    )
    record_step_api_response(p, "prepare", status)
    return status


def execute_upload(p: RunPaths, req: UploadRequest) -> ApiStatus:
    if not p.run_dir.exists():
        raise FileNotFoundError(f"run_id not found: {req.run_id}")

    started = utc_now()
    ingestion_dir = Path(req.ingestion_dir) if req.ingestion_dir else p.prepare_dir
    if not ingestion_dir.is_dir():
        raise ValueError("ingestion_dir not found; run /prepare first or pass ingestion_dir.")
    if not (ingestion_dir / "manifest.jsonl").is_file():
        raise ValueError("manifest.jsonl missing in ingestion_dir; run /prepare first.")

    staging_ns = pinecone_staging_namespace(req.live_prefix, req.staging_namespace)

    api_key = (os.environ.get("PINECONE_API_KEY") or "").strip()
    index_host = (os.environ.get("PINECONE_INDEX_HOST") or "").strip()
    if not api_key:
        raise ValueError("Missing PINECONE_API_KEY in environment (required for upload).")
    if not index_host:
        raise ValueError("Missing PINECONE_INDEX_HOST in environment (required for upload).")
    live_info = compute_next_live_namespace(api_key=api_key, index_host=index_host, live_prefix=req.live_prefix.strip())
    update_state(
        p,
        {
            "upload": {
                "status": "started",
                "started_at": started.isoformat(),
                "ingestion_dir": str(ingestion_dir),
                "live_prefix": req.live_prefix.strip(),
                "staging_namespace": staging_ns,
                "previous_live_namespace": live_info.previous_live_namespace,
                "live_namespace": live_info.live_namespace,
            }
        },
    )

    upsert_args = argparse.Namespace(
        ingestion_dir=str(ingestion_dir.resolve()),
        text_source=req.text_source,
        no_sidecar_metadata=not req.include_sidecar_metadata,
        output_dir="output1",
        page_output_subdir="pages",
        timestamp_dir="latest",
        vector_dim=req.vector_dim,
        embed_model=req.embed_model,
        batch_size=req.batch_size,
        embed_batch_size=req.embed_batch_size,
        pool_threads=req.pool_threads,
        embed_workers=req.embed_workers,
        embed_max_retries=12,
        embed_retry_base_sec=3.0,
        staging_namespace=staging_ns,
        namespace=None,
        live_prefix=req.live_prefix.strip(),
        delete_previous_live=req.delete_previous_live,
        max_records=req.max_records,
        chunk_size_words=250,
        chunk_overlap_words=40,
    )
    try:
        with _capture_stdio(p.upload_log_path, p.upload_err_path):
            pinecone_upsert.run_upsert(upsert_args)
        code = 0
    except Exception:
        with p.upload_err_path.open("a", encoding="utf-8") as ef:
            ef.write(traceback.format_exc())
        code = 1
    finished = utc_now()
    ok = code == 0

    upload_metrics: dict | None = None
    try:
        stdout_text = p.upload_log_path.read_text(encoding="utf-8")
    except OSError:
        stdout_text = ""
    m = _UPSERT_COMPLETE_RE.search(stdout_text)
    if m:
        upload_metrics = {
            "chunk_vectors": int(m.group("chunk_vectors")),
            "processed_urls": int(m.group("processed_urls")),
            "skipped_urls": int(m.group("skipped_urls")),
        }
    update_state(
        p,
        {
            "upload": {
                "status": "ok" if ok else "error",
                "exit_code": code,
                "started_at": started.isoformat(),
                "finished_at": finished.isoformat(),
                "ingestion_dir": str(ingestion_dir),
                "live_prefix": req.live_prefix.strip(),
                "staging_namespace": staging_ns,
                "previous_live_namespace": live_info.previous_live_namespace,
                "live_namespace": live_info.live_namespace,
                "metrics": upload_metrics,
            }
        },
    )

    status = ApiStatus(
        ok=ok,
        step="upload",
        run_id=req.run_id,
        started_at=started,
        finished_at=finished,
        message="upload complete" if ok else "upload failed",
        outputs={
            "run_dir": str(p.run_dir),
            "ingestion_dir": str(ingestion_dir),
            "live_prefix": req.live_prefix.strip(),
            "staging_namespace": staging_ns,
            "previous_live_namespace": live_info.previous_live_namespace,
            "live_namespace": live_info.live_namespace,
            "metrics": upload_metrics,
            "request": {
                "vector_dim": req.vector_dim,
                "text_source": req.text_source,
                "embed_model": req.embed_model,
                "batch_size": req.batch_size,
                "embed_batch_size": req.embed_batch_size,
                "embed_workers": req.embed_workers,
                "pool_threads": req.pool_threads,
                "delete_previous_live": req.delete_previous_live,
                "include_sidecar_metadata": req.include_sidecar_metadata,
                "max_records": req.max_records,
            },
        },
        logs={"stdout": str(p.upload_log_path), "stderr": str(p.upload_err_path)},
    )
    record_step_api_response(p, "upload", status)
    return status


def api_status_to_jsonable(status: ApiStatus) -> dict:
    return status.model_dump(mode="json")
