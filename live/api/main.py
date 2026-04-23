from __future__ import annotations

import json
import os
import sys
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse

from live.domain.schemas import (
    ApiStatus,
    HealthResponse,
    PipelineEnqueueResponse,
    PipelineRunRequest,
    PrepareRequest,
    ProcrastinateJobInfo,
    RunStatusResponse,
    RunListItem,
    RunsListResponse,
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


@app.get("/ui", response_class=HTMLResponse, tags=["runs"])
def runs_ui() -> HTMLResponse:
    # No external build tooling; keep a single-file dashboard that calls GET /runs.
    return HTMLResponse(
        """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Runs dashboard</title>
  <style>
    :root { color-scheme: light dark; }
    body { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; margin: 24px; }
    .row { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
    .muted { opacity: 0.75; }
    .pill { display: inline-block; padding: 2px 8px; border-radius: 999px; border: 1px solid rgba(127,127,127,0.35); font-size: 12px; }
    details { border: 1px solid rgba(127,127,127,0.25); border-radius: 10px; padding: 10px 12px; margin: 10px 0; }
    summary { cursor: pointer; }
    pre { white-space: pre-wrap; word-break: break-word; background: rgba(127,127,127,0.08); padding: 10px; border-radius: 10px; overflow: auto; }
    code { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, \"Liberation Mono\", \"Courier New\", monospace; }
    a { color: inherit; }
    input, button { font: inherit; padding: 8px 10px; border-radius: 8px; border: 1px solid rgba(127,127,127,0.35); background: transparent; }
    button { cursor: pointer; }
  </style>
</head>
<body>
  <div class="row">
    <h2 style="margin: 0;">Runs dashboard</h2>
    <span class="pill" id="runsRoot"></span>
  </div>
  <div class="row muted" style="margin: 10px 0 18px;">
    <label>Limit <input id="limit" type="number" min="1" max="500" value="50" style="width: 100px;" /></label>
    <label>Auto-refresh <input id="refresh" type="number" min="0" max="60" value="3" style="width: 100px;" />s (0 = off)</label>
    <button id="reload">Reload</button>
    <span id="status" class="muted"></span>
  </div>

  <div id="list"></div>

  <script>
    const elList = document.getElementById('list');
    const elStatus = document.getElementById('status');
    const elLimit = document.getElementById('limit');
    const elRefresh = document.getElementById('refresh');
    const elRunsRoot = document.getElementById('runsRoot');
    const elReload = document.getElementById('reload');

    function pill(text) {
      const s = document.createElement('span');
      s.className = 'pill';
      s.textContent = text;
      return s;
    }

    function safe(v) { return (v === null || v === undefined) ? '' : String(v); }

    async function fetchJSON(url) {
      const res = await fetch(url, { headers: { 'Accept': 'application/json' }});
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    }

    async function load() {
      const limit = Math.max(1, Math.min(500, parseInt(elLimit.value || '50', 10)));
      elStatus.textContent = 'Loading…';
      try {
        const data = await fetchJSON(`/runs?limit=${encodeURIComponent(limit)}`);
        elRunsRoot.textContent = `runs_root: ${data.runs_root}`;
        elList.innerHTML = '';
        if (!data.runs.length) {
          elList.textContent = 'No runs yet.';
          elStatus.textContent = '';
          return;
        }
        for (const r of data.runs) {
          const d = document.createElement('details');
          const s = document.createElement('summary');
          s.appendChild(pill(r.pipeline_status || 'unknown'));
          s.appendChild(document.createTextNode(` `));
          s.appendChild(document.createElement('code')).textContent = r.run_id;
          s.appendChild(document.createTextNode(` `));
          s.appendChild(pill(`step: ${r.current_step || '-'}`));
          s.appendChild(pill(`scrape: ${r.scrape_status || '-'}`));
          s.appendChild(pill(`prepare: ${r.prepare_status || '-'}`));
          s.appendChild(pill(`upload: ${r.upload_status || '-'}`));
          if (r.live_namespace) s.appendChild(pill(`live: ${r.live_namespace}`));
          if (r.updated_at) s.appendChild(pill(`updated: ${r.updated_at}`));
          d.appendChild(s);

          const inner = document.createElement('div');
          inner.style.marginTop = '10px';

          const p1 = document.createElement('div');
          p1.className = 'row muted';
          const a = document.createElement('a');
          a.href = `/runs/${encodeURIComponent(r.run_id)}`;
          a.textContent = 'JSON status';
          a.target = '_blank';
          p1.appendChild(a);
          p1.appendChild(pill(`state: ${r.state_path}`));
          inner.appendChild(p1);

          const pre = document.createElement('pre');
          pre.textContent = JSON.stringify(r, null, 2);
          inner.appendChild(pre);

          d.appendChild(inner);
          elList.appendChild(d);
        }
        elStatus.textContent = `Loaded ${data.runs.length} runs.`;
      } catch (e) {
        elStatus.textContent = `Failed: ${e}`;
      }
    }

    let timer = null;
    function setTimer() {
      if (timer) clearInterval(timer);
      timer = null;
      const sec = parseInt(elRefresh.value || '0', 10);
      if (sec > 0) timer = setInterval(load, sec * 1000);
    }

    elReload.addEventListener('click', () => load());
    elRefresh.addEventListener('change', () => setTimer());
    load(); setTimer();
  </script>
</body>
</html>
""".strip()
    )


@app.get("/runs", response_model=RunsListResponse, tags=["runs"])
def list_runs(limit: int = 50) -> RunsListResponse:
    runs_root = get_settings().resolved_runs_root()
    limit = max(1, min(500, int(limit)))
    if not runs_root.exists():
        return RunsListResponse(ok=True, runs_root=str(runs_root), count=0, runs=[])

    items: list[RunListItem] = []
    # Sort by state.json mtime when present; fall back to run_dir mtime.
    candidates = [p for p in runs_root.iterdir() if p.is_dir()]
    candidates.sort(key=lambda d: (d / "state.json").stat().st_mtime if (d / "state.json").exists() else d.stat().st_mtime, reverse=True)

    for run_dir in candidates[:limit]:
        run_id = run_dir.name
        state_path = run_dir / "state.json"
        state: dict | None = None
        if state_path.exists():
            try:
                state = json.loads(state_path.read_text(encoding="utf-8"))
            except Exception:
                state = None
        pipeline = (state or {}).get("pipeline") if isinstance(state, dict) else None
        scrape = (state or {}).get("scrape") if isinstance(state, dict) else None
        prepare = (state or {}).get("prepare") if isinstance(state, dict) else None
        upload = (state or {}).get("upload") if isinstance(state, dict) else None

        def _status(obj):
            return obj.get("status") if isinstance(obj, dict) else None

        updated_at = None
        try:
            ts = state_path.stat().st_mtime if state_path.exists() else run_dir.stat().st_mtime
            updated_at = datetime.fromtimestamp(ts).astimezone().isoformat()
        except Exception:
            updated_at = None

        items.append(
            RunListItem(
                run_id=run_id,
                updated_at=updated_at,
                state_path=str(state_path),
                pipeline_status=pipeline.get("status") if isinstance(pipeline, dict) else None,
                current_step=pipeline.get("current_step") if isinstance(pipeline, dict) else None,
                scrape_status=_status(scrape),
                prepare_status=_status(prepare),
                upload_status=_status(upload),
                live_namespace=upload.get("live_namespace") if isinstance(upload, dict) else None,
                previous_live_namespace=upload.get("previous_live_namespace") if isinstance(upload, dict) else None,
            )
        )

    return RunsListResponse(ok=True, runs_root=str(runs_root), count=len(items), runs=items)


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

