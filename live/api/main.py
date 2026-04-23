from __future__ import annotations

import json
import os
import sys
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from live.domain.schemas import (
    ApiStatus,
    HealthResponse,
    PipelineEnqueueResponse,
    PipelineRunRequest,
    PrepareRequest,
    ProcrastinateJobInfo,
    RunStatusResponse,
    ScrapeRequest,
    StopPipelineResponse,
    UploadRequest,
    coerce_step_responses,
)
from live.integrations.job_status import fetch_procrastinate_job
from live.pipeline.steps import cancel_flag_path, execute_prepare, execute_scrape, execute_upload
from live.settings import get_settings
from live.storage.runs import (
    ensure_run_dirs,
    guess_pages_dir_from_scrape_output,
    new_run_id,
    paths_for_run,
    run_subprocess,
    update_state,
    utc_now,
    write_scrape_config_yaml,
)
from live.worker.app import database_url_configured, procrastinate_app
from live.worker.tasks import pipeline_full


@asynccontextmanager
async def _lifespan(_app: FastAPI):
    if database_url_configured():
        async with procrastinate_app.open_async():
            yield
    else:
        yield


_OPENAPI_TAGS = [
    {"name": "health", "description": "Liveness and environment flags."},
    {"name": "runs", "description": "Procrastinate-backed scrape → prepare → upload pipeline."},
    {"name": "pipeline", "description": "Individual synchronous steps (same logic as inside a pipeline run)."},
]

app = FastAPI(
    title="Live ingestion API",
    version="1.0.0",
    lifespan=_lifespan,
    openapi_tags=_OPENAPI_TAGS,
    description=(
        "Scrape sites (Browserless), prepare `manifest.jsonl`, upsert to Pinecone. "
        "Use **pipeline** for single-step HTTP calls, or **runs** to enqueue the full chain on Postgres (Procrastinate) "
        "and poll `GET /runs/{run_id}` — response schemas are documented for each path."
    ),
)


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


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    return HealthResponse(
        ok=True,
        runs_root=str(get_settings().resolved_runs_root()),
        procrastinate_database=database_url_configured(),
    )


@app.get("/runs/{run_id}", response_model=RunStatusResponse, tags=["runs"])
def run_status(run_id: str) -> RunStatusResponse:
    """
    Poll run progress. ``state`` is the parsed ``state.json`` object, including:

    - ``pipeline`` — queue status, ``current_step`` (``scrape`` / ``prepare`` / ``upload`` / ``done`` / …)
    - ``scrape`` / ``prepare`` / ``upload`` — compact progress blobs written during each step
    - ``step_responses`` — when a step finishes, the matching entry is the same JSON shape as
      ``POST /scrape``, ``POST /prepare``, or ``POST /upload`` would return (``ApiStatus``), including
      ``outputs`` (manifest rows, crawl_status, Pinecone metrics, etc.) and ``logs`` paths.
    """
    p = paths_for_run(run_id)
    if not p.run_dir.exists():
        raise HTTPException(status_code=404, detail=f"run_id not found: {run_id}")
    state_text = p.state_path.read_text(encoding="utf-8")
    state_path = str(p.state_path)
    try:
        state_obj = json.loads(state_text)
    except json.JSONDecodeError:
        return RunStatusResponse(
            run_id=run_id,
            state_path=state_path,
            state=None,
            state_parse_error=True,
            state_raw=state_text,
        )

    if not isinstance(state_obj, dict):
        return RunStatusResponse(run_id=run_id, state_path=state_path, state=None)

    job_row: ProcrastinateJobInfo | None = None
    proc = state_obj.get("procrastinate")
    if isinstance(proc, dict) and proc.get("job_id") is not None:
        row = fetch_procrastinate_job(int(proc["job_id"]))
        if row is not None:
            job_row = ProcrastinateJobInfo.model_validate(row)

    pl = state_obj.get("pipeline")
    pipeline = pl if isinstance(pl, dict) else None
    current_step = pipeline.get("current_step") if pipeline else None
    pipeline_status = pipeline.get("status") if pipeline else None

    return RunStatusResponse(
        run_id=run_id,
        state_path=state_path,
        state=state_obj,
        procrastinate_job=job_row,
        pipeline=pipeline,
        current_step=current_step if isinstance(current_step, str) else None,
        pipeline_status=pipeline_status if isinstance(pipeline_status, str) else None,
        step_responses=coerce_step_responses(state_obj.get("step_responses")),
        scrape=state_obj.get("scrape") if isinstance(state_obj.get("scrape"), dict) else None,
        prepare=state_obj.get("prepare") if isinstance(state_obj.get("prepare"), dict) else None,
        upload=state_obj.get("upload") if isinstance(state_obj.get("upload"), dict) else None,
        paths=state_obj.get("paths") if isinstance(state_obj.get("paths"), dict) else None,
    )


@app.post("/runs", response_model=PipelineEnqueueResponse, tags=["runs"])
async def enqueue_pipeline(req: PipelineRunRequest) -> PipelineEnqueueResponse:
    if not database_url_configured():
        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL is not set; configure Postgres to enqueue background pipelines.",
        )
    run_id = new_run_id()
    p = paths_for_run(run_id)
    ensure_run_dirs(p)
    prep = req.prepare.model_copy(update={"run_id": run_id})
    upl = req.upload.model_copy(update={"run_id": run_id})
    cb = str(req.callback_url) if req.callback_url is not None else None
    created = utc_now()
    update_state(p, {"run_id": run_id, "created_at": created.isoformat()})
    job_id = await pipeline_full.defer_async(
        run_id=run_id,
        scrape=req.scrape.model_dump(mode="json"),
        prepare=prep.model_dump(mode="json"),
        upload=upl.model_dump(mode="json"),
        callback_url=cb,
    )
    update_state(
        p,
        {
            "procrastinate": {"job_id": job_id, "task_name": "pipeline.full"},
            "pipeline": {"status": "queued", "job_id": job_id, "created_at": created.isoformat()},
        },
    )
    return PipelineEnqueueResponse(
        ok=True,
        run_id=run_id,
        procrastinate_job_id=job_id,
        message="Pipeline job queued; run a procrastinate worker to execute it.",
    )


@app.post("/runs/{run_id}/stop", response_model=StopPipelineResponse, tags=["runs"])
async def stop_pipeline_run(run_id: str) -> StopPipelineResponse:
    p = paths_for_run(run_id)
    if not p.run_dir.exists():
        raise HTTPException(status_code=404, detail=f"run_id not found: {run_id}")
    try:
        state_obj = json.loads(p.state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        state_obj = {}
    cancel_flag_path(p).parent.mkdir(parents=True, exist_ok=True)
    cancel_flag_path(p).write_text("", encoding="utf-8")
    job_id = None
    if isinstance(state_obj, dict):
        raw = state_obj.get("procrastinate", {}).get("job_id")
        if raw is not None:
            job_id = int(raw)
            if database_url_configured():
                try:
                    await procrastinate_app.job_manager.cancel_job_by_id_async(job_id, abort=True)
                except Exception:
                    # Job may already be finished, or DB temporarily unavailable.
                    pass
    return StopPipelineResponse(
        ok=True,
        run_id=run_id,
        cancel_file=str(cancel_flag_path(p)),
        procrastinate_job_id=job_id,
    )


@app.post("/scrape", response_model=ApiStatus, tags=["pipeline"])
def scrape(req: ScrapeRequest) -> ApiStatus:
    run_id = new_run_id()
    p = paths_for_run(run_id)
    ensure_run_dirs(p)
    return execute_scrape(p, req)


@app.post("/scrape/stream", tags=["pipeline"])
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

    argv = [sys.executable, "-m", "live.engines.browserless_crawler", str(p.scrape_config_path)]

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
            cwd=str(get_settings().repo_root),
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


@app.post("/prepare", response_model=ApiStatus, tags=["pipeline"])
def prepare(req: PrepareRequest) -> ApiStatus:
    p = paths_for_run(req.run_id)
    try:
        return execute_prepare(p, req)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/upload", response_model=ApiStatus, tags=["pipeline"])
def upload(req: UploadRequest) -> ApiStatus:
    p = paths_for_run(req.run_id)
    try:
        return execute_upload(p, req)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

