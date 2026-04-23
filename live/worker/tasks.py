"""Background tasks registered on ``live.worker.app.procrastinate_app``."""

from __future__ import annotations

import logging
from typing import Any

import httpx
from procrastinate import exceptions

from live.domain.schemas import PrepareRequest, ScrapeRequest, UploadRequest
from live.pipeline.steps import api_status_to_jsonable, cancel_requested, execute_prepare, execute_scrape, execute_upload
from live.storage.runs import merge_state_key, paths_for_run, utc_now
from live.worker.app import procrastinate_app

log = logging.getLogger(__name__)


def _notify(callback_url: str | None, payload: dict[str, Any]) -> None:
    if not callback_url:
        return
    try:
        httpx.post(callback_url, json=payload, timeout=60.0)
    except Exception:
        log.exception("pipeline callback failed url=%s", callback_url)


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
        _notify(callback_url, {"run_id": run_id, "step": "upload", "result": api_status_to_jsonable(r_upload)})
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
        _notify(callback_url, {"run_id": run_id, "step": "pipeline", "status": "succeeded"})
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
