# `/app` — FastAPI pipeline

This folder exposes the existing pipeline as HTTP APIs:

- `POST /scrape` → runs `scraper.py` into a new per-run folder
- `POST /prepare` → runs `prepare_ingestion.py` against that run’s pages
- `POST /upload` → runs `upsert_pinecone.py` using the prepared `manifest.jsonl`

Each step writes logs into `app_runs/<run_id>/` and returns JSON with output paths.

## Run locally

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Example calls

Scrape:

```bash
curl -sS -X POST "http://127.0.0.1:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "seed_urls": ["https://roboracer.ai/"],
    "allowed_prefixes": ["https://roboracer.ai/"],
    "respect_allowed_prefixes": true,
    "max_pages": 50,
    "parallel_workers": 4,
    "use_selenium": true
  }'
```

Prepare (no LLM):

```bash
curl -sS -X POST "http://127.0.0.1:8000/prepare" \
  -H "Content-Type: application/json" \
  -d '{
    "run_id": "PASTE_RUN_ID_HERE",
    "min_chars": 80,
    "finetune": false
  }'
```

Prepare with finetune (OpenRouter key; `finetune_model` and `finetune_prompt` required; `openrouter_model` optional fallback id):

```bash
curl -sS -X POST "http://127.0.0.1:8000/prepare" \
  -H "Content-Type: application/json" \
  -d '{
    "run_id": "PASTE_RUN_ID_HERE",
    "finetune": true,
    "openrouter_api_key": "sk-or-v1-…",
    "finetune_model": "openai/gpt-4o-mini",
    "openrouter_model": "google/gemini-2.5-flash-lite",
    "finetune_prompt": "You are cleaning web-scraped markdown for RAG. Output plain Markdown only."
  }'
```

Upload (requires env vars `PINECONE_API_KEY`, `PINECONE_INDEX_HOST`). Pass `live_prefix` per request; staging defaults to `{live_prefix}staging` (override with `staging_namespace`):

```bash
curl -sS -X POST "http://127.0.0.1:8000/upload" \
  -H "Content-Type: application/json" \
  -d '{
    "run_id": "PASTE_RUN_ID_HERE",
    "live_prefix": "live-v-",
    "vector_dim": 1024,
    "text_source": "markdown",
    "delete_previous_live": false
  }'
```

