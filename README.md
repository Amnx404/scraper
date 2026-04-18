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

Set environment variables (for example in `.env`):

```bash
PINECONE_API_KEY=...
PINECONE_INDEX_HOST=...
```

Then upsert crawled pages:

```bash
uv run python3 upsert_pinecone.py --vector-dim 1024 --output-dir output1 --timestamp-dir latest
```

Useful flags:

- `--timestamp-dir latest` picks the newest crawl folder under `output1/pages/`.
- `--batch-size 200` controls upsert batch size.
- `--embed-batch-size 64` controls chunks per embedding request.
- `--pool-threads 30` controls parallel async upsert requests.
- `--embed-workers 4` controls parallel embedding requests.
- `--namespace your_namespace` writes to a Pinecone namespace.
- `--max-records 100` is useful for testing.
- `--embed-model llama-text-embed-v2` chooses the Pinecone embedding model.
- `--chunk-size-words 250` and `--chunk-overlap-words 40` control text chunking.
- `--replace-existing-by-url` (default true) deletes old vectors for each URL before upsert to prevent duplicates.

Chunk IDs are deterministic and hashed from `url + chunk_index + chunk_text`, which makes updates stable.
Also, with replace-by-url enabled, stale chunks are removed first and only fresh chunks remain for that URL.

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

