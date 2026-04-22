from __future__ import annotations

import json
import os
import re
import sys
import asyncio
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from app.models import ApiStatus, PrepareRequest, ScrapeRequest, UploadRequest
from app.pinecone_utils import compute_next_live_namespace
from app.run_manager import (
    RUNS_ROOT,
    ensure_run_dirs,
    guess_pages_dir_from_scrape_output,
    new_run_id,
    paths_for_run,
    pinecone_staging_namespace,
    run_subprocess,
    update_state,
    utc_now,
    write_scrape_config_yaml,
)


APP_ROOT = Path(__file__).resolve().parents[1]

_UPSERT_COMPLETE_RE = re.compile(
    r"Upsert complete:\\s+"
    r"(?P<chunk_vectors>\\d+)\\s+chunk vectors across\\s+"
    r"(?P<processed_urls>\\d+)\\s+URLs\\s+"
    r"\\(skipped\\s+(?P<skipped_urls>\\d+)\\s+empty pages\\)\\."
)


def _prepare_subprocess_env(req: PrepareRequest, base: dict[str, str]) -> dict[str, str]:
    """LLM calls use OpenRouter only: drop FINETUNE_API_KEY / OPENAI_API_KEY for this process."""
    env = dict(base)
    env.pop("FINETUNE_API_KEY", None)
    env.pop("OPENAI_API_KEY", None)
    if req.finetune:
        key = (req.openrouter_api_key or "").strip() or (env.get("OPENROUTER_API_KEY") or "").strip()
        if not key:
            raise HTTPException(
                status_code=400,
                detail="When finetune is true, set openrouter_api_key on the request or OPENROUTER_API_KEY in the environment.",
            )
    if (req.openrouter_api_key or "").strip():
        env["OPENROUTER_API_KEY"] = req.openrouter_api_key.strip()
    if (req.finetune_model or "").strip():
        env["FINETUNE_MODEL"] = req.finetune_model.strip()
    if (req.openrouter_model or "").strip():
        env["OPENROUTER_MODEL"] = req.openrouter_model.strip()
    if req.finetune and req.finetune_prompt is not None:
        env["FINETUNE_PROMPT"] = req.finetune_prompt.strip()
    return env


app = FastAPI(title="Scraper Pipeline API", version="0.1.0")


def _sse(event: str, data: object) -> str:
    payload = json.dumps(data, ensure_ascii=False)
    # SSE format: event + data, separated by newlines, terminated by blank line.
    return f"event: {event}\ndata: {payload}\n\n"


async def _stream_subprocess_lines(
    *,
    argv: list[str],
    cwd: Path,
    env: dict[str, str],
    stdout_path: Path,
    stderr_path: Path,
):
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)

    proc = await asyncio.create_subprocess_exec(
        *argv,
        cwd=str(cwd),
        env=env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    assert proc.stdout is not None
    assert proc.stderr is not None

    # Tee stdout/stderr to files while streaming.
    out_f = stdout_path.open("w", encoding="utf-8")
    err_f = stderr_path.open("w", encoding="utf-8")

    async def read_stream(stream, sink, event_name: str):
        while True:
            line = await stream.readline()
            if not line:
                break
            text = line.decode("utf-8", errors="replace").rstrip("\n")
            sink.write(text + "\n")
            sink.flush()
            yield _sse(event_name, {"line": text})

    try:
        # Interleave streams: prefer sending stderr as it appears.
        stdout_iter = read_stream(proc.stdout, out_f, "stdout")
        stderr_iter = read_stream(proc.stderr, err_f, "stderr")

        stdout_task = asyncio.create_task(stdout_iter.__anext__())
        stderr_task = asyncio.create_task(stderr_iter.__anext__())

        while True:
            done, _pending = await asyncio.wait(
                {stdout_task, stderr_task}, return_when=asyncio.FIRST_COMPLETED
            )
            if stdout_task in done:
                try:
                    yield stdout_task.result()
                    stdout_task = asyncio.create_task(stdout_iter.__anext__())
                except StopAsyncIteration:
                    stdout_task = None  # type: ignore[assignment]
            if stderr_task in done:
                try:
                    yield stderr_task.result()
                    stderr_task = asyncio.create_task(stderr_iter.__anext__())
                except StopAsyncIteration:
                    stderr_task = None  # type: ignore[assignment]

            if stdout_task is None and stderr_task is None:  # type: ignore[truthy-bool]
                break

        exit_code = await proc.wait()
        yield _sse("exit", {"exit_code": int(exit_code)})
    finally:
        try:
            out_f.close()
        except Exception:
            pass
        try:
            err_f.close()
        except Exception:
            pass


@app.get("/health")
def health() -> dict:
    return {"ok": True, "runs_root": str(RUNS_ROOT)}


@app.get("/runs/{run_id}")
def run_status(run_id: str) -> dict:
    p = paths_for_run(run_id)
    if not p.run_dir.exists():
        raise HTTPException(status_code=404, detail=f"run_id not found: {run_id}")
    return {"ok": True, "run_id": run_id, "state_path": str(p.state_path), "state": p.state_path.read_text(encoding="utf-8")}


@app.post("/scrape", response_model=ApiStatus)
def scrape(req: ScrapeRequest) -> ApiStatus:
    run_id = new_run_id()
    p = paths_for_run(run_id)
    ensure_run_dirs(p)

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
    write_scrape_config_yaml(p, cfg)

    # Force Browserless-only scraping (no direct target-site requests).
    argv = [sys.executable, str(APP_ROOT / "scraper_browserless.py"), str(p.scrape_config_path)]
    code = run_subprocess(
        argv=argv,
        cwd=APP_ROOT,
        env=os.environ.copy(),
        stdout_path=p.scrape_log_path,
        stderr_path=p.scrape_err_path,
    )

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

    return ApiStatus(
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


@app.post("/scrape/stream")
async def scrape_stream(req: ScrapeRequest):
    """
    Run a scrape and stream subprocess output as SSE.

    Events:
    - started: {run_id, ...}
    - stdout: {line}
    - stderr: {line}
    - exit: {exit_code}
    - done: final ApiStatus-like payload
    """

    run_id = new_run_id()
    p = paths_for_run(run_id)
    ensure_run_dirs(p)

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
    # Force Browserless-only.
    cfg["page_fetcher"] = "browserless"
    write_scrape_config_yaml(p, cfg)

    argv = [sys.executable, str(APP_ROOT / "scraper_browserless.py"), str(p.scrape_config_path)]

    async def event_gen():
        yield _sse(
            "started",
            {
                "run_id": run_id,
                "run_dir": str(p.run_dir),
                "scrape_dir": str(p.scrape_dir),
                "config": cfg,
            },
        )

        exit_code = None
        async for chunk in _stream_subprocess_lines(
            argv=argv,
            cwd=APP_ROOT,
            env=os.environ.copy(),
            stdout_path=p.scrape_log_path,
            stderr_path=p.scrape_err_path,
        ):
            # Track exit_code event.
            try:
                obj = json.loads(chunk.split("data: ", 1)[1])
                if chunk.startswith("event: exit") and isinstance(obj, dict):
                    exit_code = obj.get("exit_code")
            except Exception:
                pass
            yield chunk

        pages_dir = guess_pages_dir_from_scrape_output(p.scrape_dir)
        finished = utc_now()
        ok = (exit_code == 0 or exit_code is None) and pages_dir is not None

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
                    "exit_code": exit_code,
                    "started_at": started.isoformat(),
                    "finished_at": finished.isoformat(),
                    "pages_dir": str(pages_dir) if pages_dir else None,
                    "scraped_total": scraped_total,
                    "scraped_ok": scraped_ok,
                }
            },
        )

        final_payload = {
            "ok": ok,
            "step": "scrape",
            "run_id": run_id,
            "started_at": started.isoformat(),
            "finished_at": finished.isoformat(),
            "message": "scrape complete" if ok else "scrape failed",
            "outputs": {
                "run_dir": str(p.run_dir),
                "scrape_dir": str(p.scrape_dir),
                "pages_dir": str(pages_dir) if pages_dir else None,
                "config": cfg,
                "crawl_status": crawl_status,
                "counts": {"total": scraped_total, "ok": scraped_ok},
            },
            "logs": {"stdout": str(p.scrape_log_path), "stderr": str(p.scrape_err_path)},
        }
        yield _sse("done", final_payload)

    return StreamingResponse(event_gen(), media_type="text/event-stream")


@app.post("/prepare", response_model=ApiStatus)
def prepare(req: PrepareRequest) -> ApiStatus:
    p = paths_for_run(req.run_id)
    if not p.run_dir.exists():
        raise HTTPException(status_code=404, detail=f"run_id not found: {req.run_id}")

    started = utc_now()
    input_pages_dir = Path(req.input_pages_dir) if req.input_pages_dir else guess_pages_dir_from_scrape_output(p.scrape_dir)
    if input_pages_dir is None or not input_pages_dir.is_dir():
        raise HTTPException(status_code=400, detail="Could not resolve input_pages_dir; pass input_pages_dir explicitly.")

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

    argv = [
        sys.executable,
        str(APP_ROOT / "prepare_ingestion.py"),
        str(input_pages_dir),
        "--output",
        str(out_dir),
        "--min-chars",
        str(req.min_chars),
    ]
    if req.keep_binary:
        argv.append("--keep-binary")
    if req.finetune:
        argv.extend(
            [
                "--finetune",
                "--finetune-concurrency",
                str(req.finetune_concurrency),
                "--finetune-max-input-chars",
                str(req.finetune_max_input_chars),
            ]
        )

    code = run_subprocess(
        argv=argv,
        cwd=APP_ROOT,
        env=_prepare_subprocess_env(req, os.environ.copy()),
        stdout_path=p.prepare_log_path,
        stderr_path=p.prepare_err_path,
    )
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

    return ApiStatus(
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


@app.post("/upload", response_model=ApiStatus)
def upload(req: UploadRequest) -> ApiStatus:
    p = paths_for_run(req.run_id)
    if not p.run_dir.exists():
        raise HTTPException(status_code=404, detail=f"run_id not found: {req.run_id}")

    started = utc_now()
    ingestion_dir = Path(req.ingestion_dir) if req.ingestion_dir else p.prepare_dir
    if not ingestion_dir.is_dir():
        raise HTTPException(status_code=400, detail="ingestion_dir not found; run /prepare first or pass ingestion_dir.")
    if not (ingestion_dir / "manifest.jsonl").is_file():
        raise HTTPException(status_code=400, detail="manifest.jsonl missing in ingestion_dir; run /prepare first.")

    staging_ns = pinecone_staging_namespace(req.live_prefix, req.staging_namespace)

    # Compute next live namespace id (full name) up-front for API response.
    # Uses Pinecone env vars (same ones required by upsert_pinecone.py).
    api_key = (os.environ.get("PINECONE_API_KEY") or "").strip()
    index_host = (os.environ.get("PINECONE_INDEX_HOST") or "").strip()
    if not api_key:
        raise HTTPException(status_code=400, detail="Missing PINECONE_API_KEY in environment (required for upload).")
    if not index_host:
        raise HTTPException(status_code=400, detail="Missing PINECONE_INDEX_HOST in environment (required for upload).")
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

    argv = [
        sys.executable,
        str(APP_ROOT / "upsert_pinecone.py"),
        "--ingestion-dir",
        str(ingestion_dir),
        "--live-prefix",
        req.live_prefix.strip(),
        "--staging-namespace",
        staging_ns,
        "--text-source",
        req.text_source,
        "--vector-dim",
        str(req.vector_dim),
        "--embed-model",
        req.embed_model,
        "--batch-size",
        str(req.batch_size),
        "--embed-batch-size",
        str(req.embed_batch_size),
        "--embed-workers",
        str(req.embed_workers),
        "--pool-threads",
        str(req.pool_threads),
        "--delete-previous-live" if req.delete_previous_live else "--no-delete-previous-live",
    ]
    if req.max_records is not None:
        argv.extend(["--max-records", str(req.max_records)])
    if not req.include_sidecar_metadata:
        argv.append("--no-sidecar-metadata")

    code = run_subprocess(
        argv=argv,
        cwd=APP_ROOT,
        env=os.environ.copy(),
        stdout_path=p.upload_log_path,
        stderr_path=p.upload_err_path,
    )
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

    return ApiStatus(
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

