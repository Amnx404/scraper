from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class ApiStatus(BaseModel):
    ok: bool
    step: Literal["scrape", "prepare", "upload", "status"]
    run_id: str
    started_at: datetime | None = None
    finished_at: datetime | None = None
    message: str | None = None
    outputs: dict[str, Any] = Field(default_factory=dict)
    logs: dict[str, str] = Field(default_factory=dict)


class ScrapeRequest(BaseModel):
    seed_urls: list[str]
    allowed_prefixes: list[str]

    respect_allowed_prefixes: bool = True
    max_pages: int = 500
    delay: float = 0.5
    user_agent: str = "roboracer-self-scraper/1.0"

    page_fetcher: Literal["selenium", "requests"] | None = None
    use_selenium: bool = True
    selenium_page_load_timeout: int = 20
    selenium_render_wait: float = 1.0
    parallel_workers: int = 4
    retry_limit: int = 2
    max_depth: int | None = None

    url_whitelist_patterns: list[str] = Field(default_factory=lambda: ["*"])
    url_blacklist_patterns: list[str] = Field(
        default_factory=lambda: [
            "mailto:*",
            "tel:*",
            "javascript:*",
            "*.css*",
            "*.js*",
            "*.svg*",
            "*.png*",
            "*.jpg*",
            "*.jpeg*",
            "*.gif*",
            "*.webp*",
            "*.ico*",
            "*.pdf*",
            "*.zip*",
            "*.woff*",
            "*.woff2*",
            "*.ttf*",
            "*.eot*",
        ]
    )


class PrepareRequest(BaseModel):
    run_id: str
    input_pages_dir: str | None = None

    output_subdir: str = "ingestion"
    min_chars: int = 80
    keep_binary: bool = False
    finetune: bool = False
    finetune_concurrency: int = 4
    finetune_max_input_chars: int = 120_000

    live_prefix: str | None = None
    staging_namespace: str | None = None

    openrouter_api_key: str | None = None
    finetune_model: str | None = None
    openrouter_model: str | None = None
    finetune_prompt: str | None = None

    @model_validator(mode="after")
    def _finetune_requires_prompt_and_model(self) -> PrepareRequest:
        if self.finetune:
            if not (self.finetune_prompt and str(self.finetune_prompt).strip()):
                raise ValueError("finetune_prompt is required when finetune is true")
            if not (self.finetune_model and str(self.finetune_model).strip()):
                raise ValueError("finetune_model is required when finetune is true")
        return self


class UploadRequest(BaseModel):
    run_id: str
    ingestion_dir: str | None = None

    live_prefix: str = Field(min_length=1, description="e.g. live-v- → live-v-1, live-v-2, …")
    staging_namespace: str | None = Field(
        default=None,
        description="Defaults to '{live_prefix}staging' when omitted.",
    )

    vector_dim: int = 1024
    text_source: Literal["markdown", "fine"] = "markdown"
    embed_model: str = "llama-text-embed-v2"
    batch_size: int = 200
    embed_batch_size: int = 64
    embed_workers: int = 1
    pool_threads: int = 30
    max_records: int | None = None
    delete_previous_live: bool = False
    include_sidecar_metadata: bool = True


class PipelineRunRequest(BaseModel):
    scrape: ScrapeRequest
    prepare: PrepareRequest
    upload: UploadRequest
    callback_url: HttpUrl | None = None


class PipelineEnqueueResponse(BaseModel):
    ok: bool
    run_id: str
    procrastinate_job_id: int
    message: str | None = None


class HealthResponse(BaseModel):
    ok: Literal[True] = True
    runs_root: str = Field(description="Directory containing per-run folders.")
    procrastinate_database: bool = Field(
        description="True when `DATABASE_URL` is set so `POST /runs` and the worker can use Postgres."
    )


class ProcrastinateJobInfo(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    status: str
    task_name: str
    queue_name: str
    abort_requested: bool


class StepResponses(BaseModel):
    model_config = ConfigDict(extra="ignore")

    scrape: ApiStatus | None = None
    prepare: ApiStatus | None = None
    upload: ApiStatus | None = None


def coerce_step_responses(raw: Any) -> StepResponses | None:
    if not isinstance(raw, dict):
        return None
    scrape = prepare = upload = None
    try:
        if raw.get("scrape") is not None:
            scrape = ApiStatus.model_validate(raw["scrape"])
    except Exception:
        scrape = None
    try:
        if raw.get("prepare") is not None:
            prepare = ApiStatus.model_validate(raw["prepare"])
    except Exception:
        prepare = None
    try:
        if raw.get("upload") is not None:
            upload = ApiStatus.model_validate(raw["upload"])
    except Exception:
        upload = None
    if scrape is None and prepare is None and upload is None:
        return None
    return StepResponses(scrape=scrape, prepare=prepare, upload=upload)


class RunStatusResponse(BaseModel):
    ok: Literal[True] = True
    run_id: str
    state_path: str = Field(description="Absolute path to `state.json` for this run.")
    state: dict[str, Any] | None = Field(
        default=None,
        description="Parsed `state.json` (authoritative merge of pipeline, paths, and nested data).",
    )
    state_parse_error: bool | None = Field(
        default=None,
        description="Set when `state.json` is not valid JSON; see `state_raw`.",
    )
    state_raw: str | None = Field(
        default=None,
        description="Raw `state.json` text when parsing failed.",
    )
    procrastinate_job: ProcrastinateJobInfo | None = Field(
        default=None,
        description="Live row from Postgres when `DATABASE_URL` is set and the run has a Procrastinate job id.",
    )
    pipeline: dict[str, Any] | None = Field(
        default=None,
        description="Convenience copy of `state.pipeline` (status, job_id, current_step, timestamps, …).",
    )
    current_step: str | None = Field(
        default=None,
        description="Worker-reported cursor, e.g. `scrape`, `prepare`, `upload`, `done`, `aborted`.",
    )
    pipeline_status: str | None = Field(
        default=None,
        description="`queued` | `running` | `succeeded` | `failed` | `aborted` | `error`.",
    )
    step_responses: StepResponses | None = Field(
        default=None,
        description="Full `ApiStatus` objects per finished step (manifest, crawl_status, metrics, log paths).",
    )
    scrape: dict[str, Any] | None = Field(
        default=None,
        description="Compact scrape progress dict from state (status, exit_code, counts, …).",
    )
    prepare: dict[str, Any] | None = Field(
        default=None,
        description="Compact prepare progress dict from state.",
    )
    upload: dict[str, Any] | None = Field(
        default=None,
        description="Compact upload progress dict from state.",
    )
    paths: dict[str, Any] | None = Field(
        default=None,
        description="Log and config paths written when scraping starts.",
    )


class StopPipelineResponse(BaseModel):
    ok: Literal[True] = True
    run_id: str
    cancel_file: str = Field(description="Path to `.cancel_requested` written for cooperative cancellation.")
    procrastinate_job_id: int | None = Field(
        default=None,
        description="Procrastinate job id from state, if any (cancel/abort requested on this id).",
    )
