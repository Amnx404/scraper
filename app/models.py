from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


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

    # Optional: compute the next Pinecone live namespace id during prepare.
    # This does not upload anything; it only inspects existing namespaces.
    live_prefix: str | None = None
    staging_namespace: str | None = None

    # Single vendor key for LLM calls (prepare_ingestion uses OpenRouter-compatible API).
    # If omitted, OPENROUTER_API_KEY from the environment must be set when finetune is true.
    openrouter_api_key: str | None = None
    # Model id for the markdown refinement / finetune step (maps to FINETUNE_MODEL).
    finetune_model: str | None = None
    # Optional default OpenRouter model id (maps to OPENROUTER_MODEL); used as fallback in
    # prepare_ingestion when FINETUNE_MODEL is unset, and may differ from finetune_model.
    openrouter_model: str | None = None
    # When finetune is true, instruction prompt for the LLM (maps to FINETUNE_PROMPT).
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

    # Versioned live namespaces are {live_prefix}{N} (e.g. live-v-1). Required per request.
    live_prefix: str = Field(min_length=1, description="e.g. live-v- → live-v-1, live-v-2, …")
    # Scratch namespace cleared at the start of each upsert. Default: {live_prefix}staging
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

