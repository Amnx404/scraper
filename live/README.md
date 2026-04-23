# `live` — production-oriented ingestion service

Self-contained package: **configuration**, **domain models**, **on-disk run state**, **pipeline orchestration**, **heavy engines** (crawl / prepare / Pinecone), **FastAPI** (`live.api.main:app`), and **Procrastinate** worker (`live.worker.app.procrastinate_app`).

## Configuration (environment)

| Variable | Purpose |
|----------|---------|
| `LIVE_REPO_ROOT` | Repository root (default: parent of `live/`). Used as subprocess cwd for streaming scrape. |
| `LIVE_RUNS_ROOT` | Per-run directories (default: `{repo_root}/app_runs`). |
| `DATABASE_URL` | Postgres for Procrastinate (`POST /runs`). |
| `BROWSERLESS_CONTENT_URL` | Browserless `/content` endpoint for crawls. |
| `PINECONE_API_KEY`, `PINECONE_INDEX_HOST` | Upload step. |
| `OPENROUTER_API_KEY`, … | Optional finetune during prepare. |

Dotenv is loaded via `pydantic-settings` on `Settings` (`.env` in cwd).

## Run the API

```bash
uv sync
uv run uvicorn live.api.main:app --host 0.0.0.0 --port 8000
```

## Run the worker

```bash
export DATABASE_URL=postgresql://…
uv run procrastinate --app=live.worker.app.procrastinate_app schema --apply
uv run procrastinate --app=live.worker.app.procrastinate_app worker
```

## Layout

- `live/settings.py` — `pydantic-settings` singleton.
- `live/domain/schemas.py` — request/response Pydantic models (OpenAPI).
- `live/storage/runs.py` — `RunPaths`, atomic `state.json`, logs.
- `live/pipeline/steps.py` — `execute_scrape` / `execute_prepare` / `execute_upload`.
- `live/engines/` — browserless crawler, ingestion prep, Pinecone upsert (moved from repo-root scripts).
- `live/integrations/` — Postgres job row fetch, Pinecone namespace math.
- `live/worker/` — Procrastinate `App` + `pipeline.full` task.
- `live/api/main.py` — FastAPI routes (same HTTP contract as before).

The legacy `app/` package remains thin re-exports for compatibility (`app.main:app`, `app.procrastinate_jobs`, …).
