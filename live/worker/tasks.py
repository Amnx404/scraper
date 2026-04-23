"""Background tasks registered on ``live.worker.app.procrastinate_app``."""

from __future__ import annotations

import logging
from urllib.parse import urlparse
from typing import Any

import httpx
from procrastinate import exceptions

from live.domain.schemas import PrepareRequest, ScrapeRequest, UploadRequest
from live.pipeline.steps import api_status_to_jsonable, cancel_requested, execute_prepare, execute_scrape, execute_upload
from live.storage.runs import merge_state_key, paths_for_run, utc_now
from live.worker.app import procrastinate_app

log = logging.getLogger(__name__)


_REDACT_KEYS = {
    "api_key",
    "authorization",
    "Authorization",
    "token",
    "access_token",
    "secret",
}


def _redact(obj: Any) -> Any:
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for k, v in obj.items():
            if k in _REDACT_KEYS:
                out[k] = "***"
            else:
                out[k] = _redact(v)
        return out
    if isinstance(obj, list):
        return [_redact(v) for v in obj]
    return obj


def _is_clearly_localhost(url: str) -> bool:
    try:
        host = (urlparse(url).hostname or "").strip().lower()
    except Exception:
        return False
    return host in {"localhost", "127.0.0.1", "::1"}


def _notify(callback_url: str | None, payload: dict[str, Any]) -> None:
    if not callback_url:
        return
    try:
        if _is_clearly_localhost(callback_url):
            log.warning("Skipping callback to localhost url=%s payload=%s", callback_url, _redact(payload))
            return
        httpx.post(callback_url, json=payload, timeout=60.0)
    except Exception as e:
        # Callback delivery should never fail the pipeline job; keep logs concise.
        log.warning("pipeline callback failed url=%s error=%s payload=%s", callback_url, str(e), _redact(payload))


@procrastinate_app.task(name="pipeline.full", pass_context=True)
def pipeline_full(
    context: Any,
    run_id: str,
    scrape: dict[str, Any],
    prepare: dict[str, Any],
    upload: dict[str, Any],
    callback_url: str | None = None,
) -> None:
    p = paths_for_run(run_id)
    started = utc_now()
    merge_state_key(
        p,
        "pipeline",
        {
            "status": "running",
            "started_at": started.isoformat(),
            "current_step": "scrape",
        },
    )

    def _aborting() -> bool:
        return bool(context.should_abort()) or cancel_requested(p)

    try:
        scrape_req = ScrapeRequest(**scrape)
        prep_req = PrepareRequest(**prepare)
        up_req = UploadRequest(**upload)

        r_scrape = execute_scrape(p, scrape_req)
        _notify(callback_url, {"run_id": run_id, "step": "scrape", "result": api_status_to_jsonable(r_scrape)})
        if not r_scrape.ok:
            merge_state_key(
                p,
                "pipeline",
                {
                    "status": "failed",
                    "failed_step": "scrape",
                    "finished_at": utc_now().isoformat(),
                    "current_step": "scrape",
                },
            )
            _notify(callback_url, {"run_id": run_id, "step": "pipeline", "status": "failed", "after": "scrape"})
            return

        if _aborting():
            raise exceptions.JobAborted("cancelled before prepare")

        merge_state_key(p, "pipeline", {"current_step": "prepare"})
        r_prepare = execute_prepare(p, prep_req)
        _notify(callback_url, {"run_id": run_id, "step": "prepare", "result": api_status_to_jsonable(r_prepare)})
        if not r_prepare.ok:
            merge_state_key(
                p,
                "pipeline",
                {
                    "status": "failed",
                    "failed_step": "prepare",
                    "finished_at": utc_now().isoformat(),
                    "current_step": "prepare",
                },
            )
            _notify(callback_url, {"run_id": run_id, "step": "pipeline", "status": "failed", "after": "prepare"})
            return

        if _aborting():
            raise exceptions.JobAborted("cancelled before upload")

        merge_state_key(p, "pipeline", {"current_step": "upload"})
        r_upload = execute_upload(p, up_req)
        upload_result = api_status_to_jsonable(r_upload)
        live_namespace = None
        previous_live_namespace = None
        if isinstance(upload_result, dict):
            outputs = upload_result.get("outputs")
            if isinstance(outputs, dict):
                live_namespace = outputs.get("live_namespace")
                previous_live_namespace = outputs.get("previous_live_namespace")
        _notify(
            callback_url,
            {
                "run_id": run_id,
                "step": "upload",
                "result": upload_result,
                "pinecone": {
                    "live_namespace": live_namespace,
                    "previous_live_namespace": previous_live_namespace,
                },
            },
        )
        if not r_upload.ok:
            merge_state_key(
                p,
                "pipeline",
                {
                    "status": "failed",
                    "failed_step": "upload",
                    "finished_at": utc_now().isoformat(),
                    "current_step": "upload",
                },
            )
            _notify(callback_url, {"run_id": run_id, "step": "pipeline", "status": "failed", "after": "upload"})
            return

        merge_state_key(
            p,
            "pipeline",
            {"status": "succeeded", "finished_at": utc_now().isoformat(), "current_step": "done"},
        )
        _notify(
            callback_url,
            {
                "run_id": run_id,
                "step": "pipeline",
                "status": "succeeded",
                "pinecone": {
                    "live_namespace": live_namespace,
                    "previous_live_namespace": previous_live_namespace,
                },
            },
        )
    except exceptions.JobAborted:
        merge_state_key(
            p,
            "pipeline",
            {"status": "aborted", "finished_at": utc_now().isoformat(), "current_step": "aborted"},
        )
        _notify(callback_url, {"run_id": run_id, "step": "pipeline", "status": "aborted"})
        raise
    except Exception as e:
        log.exception("pipeline_full failed run_id=%s", run_id)
        merge_state_key(
            p,
            "pipeline",
            {
                "status": "error",
                "error": str(e),
                "finished_at": utc_now().isoformat(),
                "current_step": "error",
            },
        )
        _notify(callback_url, {"run_id": run_id, "step": "pipeline", "status": "error", "error": str(e)})
        raise
