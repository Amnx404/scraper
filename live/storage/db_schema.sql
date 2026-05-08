-- Detailed scraper audit store.
-- Apply with: python3 -m live.storage.db_store --apply-schema

CREATE TABLE IF NOT EXISTS scraper_runs (
    run_id              TEXT PRIMARY KEY,
    created_at          TIMESTAMPTZ,
    status              TEXT NOT NULL DEFAULT 'queued',
    current_step        TEXT,

    -- Request config
    seed_urls           TEXT[],
    allowed_prefixes    TEXT[],
    max_pages           INT,
    page_fetcher        TEXT,
    live_prefix         TEXT,
    staging_namespace   TEXT,
    procrastinate_job_id INT,
    request_json        JSONB,

    -- Scrape step
    scrape_started_at   TIMESTAMPTZ,
    scrape_finished_at  TIMESTAMPTZ,
    scraped_total       INT,
    scraped_ok          INT,

    -- Prepare step
    prepare_started_at  TIMESTAMPTZ,
    prepare_finished_at TIMESTAMPTZ,
    prepared_docs       INT,
    finetuned_docs      INT,

    -- Upload step
    upload_started_at   TIMESTAMPTZ,
    upload_finished_at  TIMESTAMPTZ,
    live_namespace      TEXT,
    previous_live_namespace TEXT,
    vector_chunks       INT,
    processed_urls      INT,
    skipped_urls        INT,
    embed_model         TEXT,

    error               TEXT,
    finished_at         TIMESTAMPTZ
);

-- One row per scraped page
CREATE TABLE IF NOT EXISTS scraper_pages (
    id              BIGSERIAL PRIMARY KEY,
    run_id          TEXT NOT NULL REFERENCES scraper_runs(run_id) ON DELETE CASCADE,
    url             TEXT NOT NULL,
    source_url      TEXT,
    engine          TEXT,
    status          TEXT NOT NULL,           -- ok | error | retrying
    status_code     INT,
    content_type    TEXT,
    title           TEXT,
    description     TEXT,
    language        TEXT,
    markdown        TEXT,
    word_count      INT,
    char_count      INT,
    link_count      INT,
    links           TEXT[],
    media_images    TEXT[],
    media_videos    TEXT[],
    media_pdfs      TEXT[],
    error           TEXT,
    retries         INT DEFAULT 0,
    depth           INT DEFAULT 0,
    scraped_at      TIMESTAMPTZ,
    UNIQUE (run_id, url)
);

-- One row per prepared / finetuned doc (output of prepare step)
CREATE TABLE IF NOT EXISTS scraper_prepared_docs (
    id              BIGSERIAL PRIMARY KEY,
    run_id          TEXT NOT NULL REFERENCES scraper_runs(run_id) ON DELETE CASCADE,
    doc_id          TEXT,
    url             TEXT NOT NULL,
    title           TEXT,
    markdown        TEXT,
    fine_markdown   TEXT,
    char_count      INT,
    fine_char_count INT,
    skipped         BOOLEAN DEFAULT FALSE,
    skip_reason     TEXT,
    prepared_at     TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (run_id, url)
);

-- One row per upload step execution
CREATE TABLE IF NOT EXISTS scraper_uploads (
    id                      BIGSERIAL PRIMARY KEY,
    run_id                  TEXT NOT NULL REFERENCES scraper_runs(run_id) ON DELETE CASCADE,
    live_prefix             TEXT,
    staging_namespace       TEXT,
    live_namespace          TEXT,
    previous_live_namespace TEXT,
    vector_chunks           INT,
    processed_urls          INT,
    skipped_urls            INT,
    embed_model             TEXT,
    vector_dim              INT,
    text_source             TEXT,
    uploaded_at             TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS scraper_pages_run_id   ON scraper_pages (run_id);
CREATE INDEX IF NOT EXISTS scraper_pages_url      ON scraper_pages (url);
CREATE INDEX IF NOT EXISTS scraper_prepared_run   ON scraper_prepared_docs (run_id);
CREATE INDEX IF NOT EXISTS scraper_uploads_run    ON scraper_uploads (run_id);
CREATE INDEX IF NOT EXISTS scraper_runs_status    ON scraper_runs (status);
CREATE INDEX IF NOT EXISTS scraper_runs_created   ON scraper_runs (created_at DESC);
