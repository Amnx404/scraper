# Web Scraper (Selenium + Markdown JSONL)

A simple crawler that:

- starts from configured seed URLs,
- renders pages with Selenium (for JS-heavy sites),
- extracts page content as Markdown,
- collects page metadata and discovered links (including `iframe` sources),
- writes one JSON object per page to JSONL.

## Requirements

- Python 3.11+ (tested with 3.13)
- `uv`
- Google Chrome (or Chromium) available for Selenium headless mode

## Setup

From the project root:

```bash
uv venv
source .venv/bin/activate
python -m ensurepip --upgrade
python -m pip install -r requirements.txt
```

Or run without activating:

```bash
uv run python3 scraper.py
```

## Configuration

The scraper reads `config.yaml` by default (or a path you pass as CLI arg).

Create `config.yaml`:

```yaml
seed_urls:
  - https://roboracer.ai/

allowed_prefixes:
  - https://roboracer.ai/
  - https://f1tenth-coursekit.readthedocs.io/

# false = crawl every discovered link (recommended if filtering later)
# true  = only crawl URLs that match one of allowed_prefixes
respect_allowed_prefixes: false

output_dir: output
page_output_subdir: pages
global_status_filename: crawl_status.jsonl
max_pages: 500
delay: 0.5
user_agent: python-domain-scraper/1.0

use_selenium: true
selenium_page_load_timeout: 20
selenium_render_wait: 1.0
parallel_workers: 4
retry_limit: 2
url_whitelist_patterns:
  - "*"
url_blacklist_patterns:
  - "mailto:*"
  - "*.css*"
  - "*.js*"
  - "*.gif*"
```

### Config Notes

- `seed_urls`: crawl entry points.
- `allowed_prefixes`: URL scopes used only when `respect_allowed_prefixes: true`.
- `respect_allowed_prefixes: false`: crawler follows all discovered links.
- `output_dir`: root folder for crawl artifacts.
- `page_output_subdir`: subfolder where one JSON file per crawled URL is stored.
- `global_status_filename`: global JSONL file with status for every processed URL.
- `max_pages`: max visited URLs per seed crawl.
- `delay`: sleep between requests/pages in seconds.
- `selenium_render_wait`: extra wait after page load for JS-rendered content.
- `parallel_workers`: number of concurrent crawler threads (`<= 0` means auto: `CPU cores - 1`, minimum `1`).
- `retry_limit`: number of retries after an attempted scrape fails.
- `url_whitelist_patterns`: wildcard allow list for queueing URLs.
- `url_blacklist_patterns`: wildcard deny list for queueing URLs.
- Legacy `base_urls` is still supported for backward compatibility.

## Usage

Run with default config:

```bash
uv run python3 scraper.py
```

Run with explicit config:

```bash
uv run python3 scraper.py my_config.yaml
```

## Upsert To Pinecone

Each run:

1. **Lists** all index namespaces and finds the highest **`{prefix}{N}`** (default prefix `live-v-`, e.g. `live-v-2`). That namespace is remembered as **previous live** (for optional deletion later). The **new** live namespace is **`live-v-{N+1}`** (first run with no matches → `live-v-1`).
2. **`delete_all`** on the **staging** scratch namespace (e.g. `chunk-staging`), then embeds all chunks and upserts into staging until complete.
3. Upserts the **same** vectors again into the new **`live-v-N`** namespace (no re-embed). Point your app at **that** name (e.g. `PINECONE_NAMESPACE=live-v-3`).
4. Optionally **`--delete-previous-live`**: `delete_all` on the **previous** `live-v-*` recorded at step 1. Use only after traffic reads the **new** namespace.

Set environment variables (for example in `.env`):

```bash
PINECONE_API_KEY=...
PINECONE_INDEX_HOST=...

PINECONE_STAGING_NAMESPACE=chunk-staging
# Namespaces like live-v-1, live-v-2 (optional — default is live-v-):
PINECONE_LIVE_PREFIX=live-v-
```

Upsert crawled pages:

```bash
uv run python3 upsert_pinecone.py --vector-dim 1024 --output-dir output1 --timestamp-dir latest
```

Or upsert from **`prepare_ingestion` output** (directory with `manifest.jsonl`):

```bash
uv run python3 upsert_pinecone.py --vector-dim 1024 --ingestion-dir ingestion_ready --text-source fine
```

Use `--text-source markdown` for deterministic cleaned markdown, or `--text-source fine` for LLM-refined `fine_markdown/`. Manifest fields (`url`, `title`, paths, char counts) are stored in vector metadata; sidecar `metadata/*.json` is merged unless you pass `--no-sidecar-metadata`.

Useful flags:

- `--timestamp-dir latest` picks the newest crawl folder under `output1/pages/`.
- `--batch-size 200` controls upsert batch size.
- `--embed-batch-size 64` controls chunks per embedding request.
- `--pool-threads 30` controls parallel async upsert requests.
- `--embed-workers 1` controls parallel embedding requests (default **1** to avoid Pinecone Inference **tokens-per-minute** limits; increase only if your plan allows).
- On HTTP **429** from embeddings, the script **retries with exponential backoff** (`--embed-max-retries`, `--embed-retry-base-sec`).
- `--staging-namespace` / `--namespace` (alias): scratch namespace cleared at the start of each run (default `PINECONE_STAGING_NAMESPACE` or `chunk-staging`).
- `--live-prefix`: pattern for versioned live namespaces (default `PINECONE_LIVE_PREFIX` or `live-v-`).
- **`--delete-previous-live` / `--no-delete-previous-live`**: after publishing the new `live-v-N`, delete the previous `live-v-*` seen at the start of the run. Unsafe if anything still queries that old namespace.
- `--max-records 100` is useful for testing.
- `--embed-model llama-text-embed-v2` chooses the Pinecone embedding model.
- `--chunk-size-words 250` and `--chunk-overlap-words 40` control text chunking.

Chunk IDs are deterministic and hashed from `url + chunk_index + chunk_text`, which makes updates stable.

The script now embeds chunk text via Pinecone Inference (`pc.inference.embed`) before upsert.

## Output Format

Per-URL page files:

- `output/<page_output_subdir>/<timestamp>/<slug>_<hash>.json`

Each page file contains the page record (`url`, `markdown`, `metadata`, `links`, etc.).
If scraping fails for a URL, its file still exists and contains error details.

Global status file:

- `output/<global_status_filename>`

Each line is a JSON status record for one processed URL:

```json
{
  "url": "https://example.com/page",
  "source": "https://example.com",
  "status": "ok",
  "error": null,
  "output_file": "output/pages/20260417_172500/example_com_page_ab12cd34ef.json",
  "scraped_at": "2026-04-17T21:25:00.000000+00:00"
}
```

## Common Issues

- Empty markdown on SPA routes: page may be a wrapper around an iframe; iframe URLs are still collected in `links`.
- Selenium startup failure: scraper falls back to requests-only mode.
- No output: verify `seed_urls` is present and non-empty.
- Asset URLs (css/gif/js/images) are discovered and stored in `links`, but can be blocked from crawl queue via wildcard blacklist.

