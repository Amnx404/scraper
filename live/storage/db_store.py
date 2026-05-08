"""Write detailed run/page/prepare/upload data to Postgres for audit and history.

All functions are no-ops when DATABASE_URL is unset or psycopg is unavailable.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

_SCHEMA_PATH = Path(__file__).with_name("db_schema.sql")


def _db_url() -> str | None:
    url = (os.environ.get("DATABASE_URL") or "").strip()
    if not url:
        return None
    return url.replace("postgres://", "postgresql://", 1)


def _connect():
    url = _db_url()
    if not url:
        return None
    try:
        import psycopg  # type: ignore
        return psycopg.connect(url, autocommit=True)
    except Exception as exc:
        log.warning("db_store: could not connect to Postgres: %s", exc)
        return None


def apply_schema() -> None:
    con = _connect()
    if con is None:
        return
    try:
        con.execute(_SCHEMA_PATH.read_text())
        log.info("db_store: schema applied")
    except Exception as exc:
        log.warning("db_store: apply_schema failed: %s", exc)
    finally:
        con.close()


# ---------------------------------------------------------------------------
# Run-level helpers
# ---------------------------------------------------------------------------

def _upsert_run(con, run_id: str, fields: dict[str, Any]) -> None:
    cols = list(fields.keys())
    vals = list(fields.values())
    set_clause = ", ".join(f"{c} = EXCLUDED.{c}" for c in cols)
    col_str = "run_id, " + ", ".join(cols)
    placeholders = ", ".join(["%s"] * (len(cols) + 1))
    sql = (
        f"INSERT INTO scraper_runs ({col_str}) VALUES ({placeholders}) "
        f"ON CONFLICT (run_id) DO UPDATE SET {set_clause}"
    )
    con.execute(sql, [run_id] + vals)


def store_run_created(
    run_id: str,
    *,
    request: dict[str, Any],
    procrastinate_job_id: int | None = None,
) -> None:
    con = _connect()
    if con is None:
        return
    try:
        scrape = request.get("scrape") or {}
        upload = request.get("upload") or {}
        _upsert_run(con, run_id, {
            "created_at": datetime.now(UTC),
            "status": "queued",
            "seed_urls": scrape.get("seed_urls") or [],
            "allowed_prefixes": scrape.get("allowed_prefixes") or [],
            "max_pages": scrape.get("max_pages"),
            "page_fetcher": scrape.get("page_fetcher"),
            "live_prefix": upload.get("live_prefix"),
            "procrastinate_job_id": procrastinate_job_id,
            "request_json": json.dumps(request),
        })
    except Exception as exc:
        log.warning("db_store: store_run_created failed run_id=%s: %s", run_id, exc)
    finally:
        con.close()


def store_scrape_started(run_id: str) -> None:
    con = _connect()
    if con is None:
        return
    try:
        _upsert_run(con, run_id, {
            "status": "running",
            "current_step": "scrape",
            "scrape_started_at": datetime.now(UTC),
        })
    except Exception as exc:
        log.warning("db_store: store_scrape_started failed: %s", exc)
    finally:
        con.close()


def store_scrape_finished(
    run_id: str,
    *,
    pages_dir: Path | None,
    scraped_total: int | None,
    scraped_ok: int | None,
    ok: bool,
) -> None:
    """Write run-level scrape summary and bulk-insert all page records."""
    con = _connect()
    if con is None:
        return
    try:
        _upsert_run(con, run_id, {
            "scrape_finished_at": datetime.now(UTC),
            "scraped_total": scraped_total,
            "scraped_ok": scraped_ok,
            "status": "running" if ok else "failed",
            "current_step": "scrape" if not ok else "prepare",
        })
        if pages_dir and pages_dir.is_dir():
            _bulk_insert_pages(con, run_id, pages_dir)
    except Exception as exc:
        log.warning("db_store: store_scrape_finished failed: %s", exc)
    finally:
        con.close()


def _bulk_insert_pages(con, run_id: str, pages_dir: Path) -> None:
    rows = []
    for path in pages_dir.glob("*.json"):
        try:
            rec = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        md = rec.get("markdown") or ""
        meta = rec.get("metadata") or {}
        media = rec.get("media") or {}
        links = rec.get("links") or []

        rows.append((
            run_id,
            rec.get("url") or "",
            rec.get("source"),
            rec.get("engine"),
            "error" if rec.get("error") else "ok",
            meta.get("status_code"),
            meta.get("content_type"),
            meta.get("title"),
            meta.get("description"),
            meta.get("language"),
            md,
            len(md.split()) if md else 0,
            len(md) if md else 0,
            len(links),
            links or None,
            media.get("images") or None,
            media.get("videos") or None,
            media.get("pdfs") or None,
            rec.get("error"),
            int(rec.get("retries", 0)),
            int(rec.get("depth", 0)),
            rec.get("scraped_at"),
        ))

    if not rows:
        return

    from psycopg.extras import execute_values  # type: ignore
    execute_values(
        con,
        """
        INSERT INTO scraper_pages (
            run_id, url, source_url, engine, status,
            status_code, content_type, title, description, language,
            markdown, word_count, char_count, link_count, links,
            media_images, media_videos, media_pdfs,
            error, retries, depth, scraped_at
        ) VALUES %s
        ON CONFLICT (run_id, url) DO UPDATE SET
            status       = EXCLUDED.status,
            markdown     = EXCLUDED.markdown,
            word_count   = EXCLUDED.word_count,
            char_count   = EXCLUDED.char_count,
            link_count   = EXCLUDED.link_count,
            links        = EXCLUDED.links,
            media_images = EXCLUDED.media_images,
            media_videos = EXCLUDED.media_videos,
            media_pdfs   = EXCLUDED.media_pdfs,
            error        = EXCLUDED.error,
            scraped_at   = EXCLUDED.scraped_at
        """,
        rows,
    )
    log.info("db_store: inserted/updated %d page rows for run %s", len(rows), run_id)


def store_prepare_finished(
    run_id: str,
    *,
    ingestion_dir: Path,
    prepared_docs: int | None,
    finetuned_docs: int | None,
    ok: bool,
) -> None:
    con = _connect()
    if con is None:
        return
    try:
        _upsert_run(con, run_id, {
            "prepare_finished_at": datetime.now(UTC),
            "prepared_docs": prepared_docs,
            "finetuned_docs": finetuned_docs,
            "status": "running" if ok else "failed",
            "current_step": "prepare" if not ok else "upload",
        })
        if ok and ingestion_dir.is_dir():
            _bulk_insert_prepared_docs(con, run_id, ingestion_dir)
            _bulk_insert_skipped_docs(con, run_id, ingestion_dir)
    except Exception as exc:
        log.warning("db_store: store_prepare_finished failed: %s", exc)
    finally:
        con.close()


def _bulk_insert_prepared_docs(con, run_id: str, ingestion_dir: Path) -> None:
    manifest = ingestion_dir / "manifest.jsonl"
    if not manifest.is_file():
        return

    rows = []
    with manifest.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue

            fine_md = None
            fine_path = rec.get("fine_markdown_path")
            if fine_path:
                fp = ingestion_dir / fine_path
                if fp.is_file():
                    fine_md = fp.read_text(encoding="utf-8").strip()

            md = None
            md_path = rec.get("markdown_path")
            if md_path:
                mp = ingestion_dir / md_path
                if mp.is_file():
                    md = mp.read_text(encoding="utf-8").strip()

            rows.append((
                run_id,
                rec.get("id"),
                rec.get("url") or "",
                rec.get("title"),
                md,
                fine_md,
                rec.get("char_count"),
                rec.get("fine_char_count"),
                False,
                None,
            ))

    if not rows:
        return

    from psycopg.extras import execute_values  # type: ignore
    execute_values(
        con,
        """
        INSERT INTO scraper_prepared_docs (
            run_id, doc_id, url, title,
            markdown, fine_markdown,
            char_count, fine_char_count,
            skipped, skip_reason
        ) VALUES %s
        ON CONFLICT (run_id, url) DO UPDATE SET
            doc_id         = EXCLUDED.doc_id,
            title          = EXCLUDED.title,
            markdown       = EXCLUDED.markdown,
            fine_markdown  = EXCLUDED.fine_markdown,
            char_count     = EXCLUDED.char_count,
            fine_char_count = EXCLUDED.fine_char_count,
            skipped        = EXCLUDED.skipped,
            skip_reason    = EXCLUDED.skip_reason
        """,
        rows,
    )
    log.info("db_store: inserted %d prepared docs for run %s", len(rows), run_id)


def _bulk_insert_skipped_docs(con, run_id: str, ingestion_dir: Path) -> None:
    skipped_path = ingestion_dir / "skipped.jsonl"
    if not skipped_path.is_file():
        return

    rows = []
    with skipped_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            url = rec.get("url") or rec.get("file") or ""
            rows.append((run_id, None, url, None, None, None, None, None, True, rec.get("reason")))

    if not rows:
        return

    from psycopg.extras import execute_values  # type: ignore
    execute_values(
        con,
        """
        INSERT INTO scraper_prepared_docs (
            run_id, doc_id, url, title,
            markdown, fine_markdown,
            char_count, fine_char_count,
            skipped, skip_reason
        ) VALUES %s
        ON CONFLICT (run_id, url) DO UPDATE SET
            skipped     = EXCLUDED.skipped,
            skip_reason = EXCLUDED.skip_reason
        """,
        rows,
    )


def store_upload_finished(
    run_id: str,
    *,
    live_prefix: str,
    staging_namespace: str,
    live_namespace: str | None,
    previous_live_namespace: str | None,
    vector_chunks: int | None,
    processed_urls: int | None,
    skipped_urls: int | None,
    embed_model: str,
    vector_dim: int,
    text_source: str,
    ok: bool,
) -> None:
    con = _connect()
    if con is None:
        return
    try:
        now = datetime.now(UTC)
        _upsert_run(con, run_id, {
            "upload_finished_at": now,
            "live_namespace": live_namespace,
            "previous_live_namespace": previous_live_namespace,
            "staging_namespace": staging_namespace,
            "vector_chunks": vector_chunks,
            "processed_urls": processed_urls,
            "skipped_urls": skipped_urls,
            "embed_model": embed_model,
            "status": "succeeded" if ok else "failed",
            "current_step": "done" if ok else "upload",
            "finished_at": now,
        })
        con.execute(
            """
            INSERT INTO scraper_uploads (
                run_id, live_prefix, staging_namespace, live_namespace,
                previous_live_namespace, vector_chunks, processed_urls,
                skipped_urls, embed_model, vector_dim, text_source
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            [
                run_id, live_prefix, staging_namespace, live_namespace,
                previous_live_namespace, vector_chunks, processed_urls,
                skipped_urls, embed_model, vector_dim, text_source,
            ],
        )
    except Exception as exc:
        log.warning("db_store: store_upload_finished failed: %s", exc)
    finally:
        con.close()


def store_run_failed(run_id: str, *, error: str, step: str) -> None:
    con = _connect()
    if con is None:
        return
    try:
        _upsert_run(con, run_id, {
            "status": "failed",
            "current_step": step,
            "error": error,
            "finished_at": datetime.now(UTC),
        })
    except Exception as exc:
        log.warning("db_store: store_run_failed failed: %s", exc)
    finally:
        con.close()


def store_run_aborted(run_id: str) -> None:
    con = _connect()
    if con is None:
        return
    try:
        _upsert_run(con, run_id, {
            "status": "aborted",
            "finished_at": datetime.now(UTC),
        })
    except Exception as exc:
        log.warning("db_store: store_run_aborted failed: %s", exc)
    finally:
        con.close()


if __name__ == "__main__":
    import sys
    if "--apply-schema" in sys.argv:
        apply_schema()
        print("Schema applied.")
