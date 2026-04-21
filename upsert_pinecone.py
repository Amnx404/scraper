import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import itertools
import json
import os
import random
import re
import sys
import time
from pathlib import Path

from pinecone import Pinecone
from pinecone.exceptions import NotFoundException, PineconeApiException
from dotenv import load_dotenv
from tqdm import tqdm


def pinecone_namespace_param(ns: str | None) -> str | None:
    """Empty string or None → Pinecone client uses default namespace (``)."""
    if ns is None or ns == "":
        return None
    return ns


def resolve_staging_namespace(args: argparse.Namespace) -> str:
    """Write target: env PINECONE_STAGING_NAMESPACE or chunk-staging."""
    staging = (
        (args.staging_namespace or "").strip()
        or (args.namespace or "").strip()
        or os.environ.get("PINECONE_STAGING_NAMESPACE", "").strip()
        or "chunk-staging"
    )
    if not staging:
        raise ValueError("Staging namespace must be non-empty (set --staging-namespace or PINECONE_STAGING_NAMESPACE).")
    return staging


def resolve_live_prefix(args: argparse.Namespace) -> str:
    p = (args.live_prefix or "").strip() or os.environ.get("PINECONE_LIVE_PREFIX", "").strip() or "live-v-"
    if not p:
        raise ValueError("Live namespace prefix must be non-empty (--live-prefix or PINECONE_LIVE_PREFIX).")
    return p


def collect_namespace_names(index) -> list[str]:
    names: list[str] = []
    for page in index.list_namespaces():
        for ns in page.namespaces or []:
            names.append(ns.name if ns.name is not None else "")
    return names


def max_live_version_number(namespace_names: list[str], prefix: str) -> int:
    """Largest N in namespaces named exactly `{prefix}{N}` with digits N (e.g. live-v-3)."""
    esc = re.escape(prefix)
    pat = re.compile(rf"^{esc}(\d+)$")
    best = 0
    for name in namespace_names:
        m = pat.match(name)
        if m:
            best = max(best, int(m.group(1)))
    return best


def previous_and_next_live_namespaces(
    namespace_names: list[str], prefix: str
) -> tuple[str | None, str]:
    m = max_live_version_number(namespace_names, prefix)
    prev_ns = f"{prefix}{m}" if m > 0 else None
    next_ns = f"{prefix}{m + 1}"
    return prev_ns, next_ns


def embed_passages_with_retry(
    pc: Pinecone,
    model: str,
    texts: list[str],
    *,
    max_retries: int,
    base_delay_sec: float,
):
    """
    Call Pinecone Inference embed. On HTTP 429 (token / request limits), backoff and retry.
    """
    parameters = {"input_type": "passage", "truncate": "END"}
    for attempt in range(max_retries + 1):
        try:
            return pc.inference.embed(
                model=model,
                inputs=texts,
                parameters=parameters,
            )
        except PineconeApiException as e:
            if getattr(e, "status", None) != 429:
                raise
            if attempt >= max_retries:
                raise
            delay = base_delay_sec * (2**attempt) + random.uniform(0, min(5.0, base_delay_sec))
            tqdm.write(
                f"Embedding hit rate limit (429); sleeping {delay:.1f}s "
                f"(retry {attempt + 1}/{max_retries})...",
                file=sys.stderr,
            )
            time.sleep(delay)
    raise RuntimeError("embed retries exhausted")  # pragma: no cover


def chunks(iterable, batch_size=200):
    """Yield tuples of size batch_size from an iterable."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))


def latest_timestamp_dir(base_dir: Path) -> Path:
    dirs = [p for p in base_dir.iterdir() if p.is_dir()]
    if not dirs:
        raise FileNotFoundError(f"No crawl page directories found under: {base_dir}")
    return sorted(dirs)[-1]


def split_into_chunks(text: str, chunk_size_words: int, chunk_overlap_words: int) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks_out: list[str] = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size_words, len(words))
        chunks_out.append(" ".join(words[start:end]).strip())
        if end >= len(words):
            break
        start = max(0, end - chunk_overlap_words)
    return [c for c in chunks_out if c]


def chunk_id_for_url(url: str, chunk_index: int, chunk_text: str) -> str:
    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    chunk_hash = hashlib.sha256(f"{url}|{chunk_index}|{chunk_text}".encode("utf-8")).hexdigest()[:16]
    return f"u{url_hash}-c{chunk_index:05d}-{chunk_hash}"


def chunk_id_for_page(page_id: str, url: str, chunk_index: int, chunk_text: str) -> str:
    """Stable chunk id when manifest page_id is available (preferred over url-only)."""
    pid = page_id or hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    chunk_hash = hashlib.sha256(f"{pid}|{chunk_index}|{chunk_text}".encode("utf-8")).hexdigest()[:16]
    return f"p{pid[:32]}-c{chunk_index:05d}-{chunk_hash}"


def _truncate_meta_str(s: str | None, max_len: int = 8192) -> str | None:
    if s is None:
        return None
    s = str(s).strip()
    if len(s) > max_len:
        return s[: max_len - 3] + "..."
    return s


def load_pages_from_manifest(
    ingestion_dir: Path,
    text_source: str,
    max_records: int | None,
    include_sidecar_metadata: bool,
):
    """
    Load pages from prepare_ingestion output: manifest.jsonl + markdown files.

    text_source: 'markdown' -> markdown_path, 'fine' -> fine_markdown_path.
    """
    manifest_path = ingestion_dir / "manifest.jsonl"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"manifest.jsonl not found: {manifest_path}")

    count = 0
    with manifest_path.open(encoding="utf-8") as mf:
        for line in mf:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            page_id = row.get("id") or ""
            url = row.get("url") or ""
            if not url:
                continue

            if text_source == "fine":
                rel = row.get("fine_markdown_path")
            else:
                rel = row.get("markdown_path")

            if not rel:
                tqdm.write(
                    f"[skip] page_id={page_id!r}: no "
                    f"{'fine_markdown_path' if text_source == 'fine' else 'markdown_path'} in manifest",
                    file=sys.stderr,
                )
                continue

            path = ingestion_dir / rel
            if not path.is_file():
                tqdm.write(f"[skip] page_id={page_id!r}: file missing {path}", file=sys.stderr)
                continue

            markdown = path.read_text(encoding="utf-8")

            extras: dict = {
                "page_id": page_id,
                "text_source": text_source,
            }
            if row.get("title") is not None:
                extras["title"] = _truncate_meta_str(str(row["title"]), 2048)
            if text_source == "fine":
                if row.get("fine_char_count") is not None:
                    extras["source_char_count"] = row["fine_char_count"]
            else:
                if row.get("char_count") is not None:
                    extras["source_char_count"] = row["char_count"]

            side_source = None
            side_scraped = None
            side_desc = None
            side_lang = None
            if include_sidecar_metadata and row.get("metadata_path"):
                side = ingestion_dir / row["metadata_path"]
                if side.is_file():
                    try:
                        m = json.loads(side.read_text(encoding="utf-8"))
                        side_source = m.get("source")
                        side_scraped = m.get("scraped_at")
                        side_desc = m.get("description")
                        side_lang = m.get("language")
                    except (json.JSONDecodeError, OSError):
                        pass

            yield {
                "url": url,
                "source": side_source,
                "scraped_at": side_scraped,
                "markdown": markdown,
                "page_id": page_id,
                "title": row.get("title"),
                "description": _truncate_meta_str(side_desc, 4096) if side_desc else None,
                "language": _truncate_meta_str(side_lang, 64) if side_lang else None,
                "manifest_extras": extras,
            }

            count += 1
            if max_records is not None and count >= max_records:
                return


def load_pages(pages_dir: Path, max_records: int | None):
    count = 0
    for page_file in sorted(pages_dir.glob("*.json")):
        with page_file.open() as f:
            data = json.load(f)

        if data.get("error"):
            continue

        url = data.get("url")
        markdown = data.get("markdown") or ""
        if not url:
            continue

        yield {
            "url": url,
            "source": data.get("source"),
            "scraped_at": data.get("scraped_at"),
            "markdown": markdown,
        }

        count += 1
        if max_records is not None and count >= max_records:
            return


def build_chunk_records_for_page(
    page: dict,
    chunk_size_words: int,
    chunk_overlap_words: int,
) -> list[dict]:
    chunks_for_page = split_into_chunks(page["markdown"], chunk_size_words, chunk_overlap_words)
    records: list[dict] = []
    page_id = page.get("page_id") or ""
    for idx, chunk_text in enumerate(chunks_for_page):
        if page_id:
            vector_id = chunk_id_for_page(page_id, page["url"], idx, chunk_text)
        else:
            vector_id = chunk_id_for_url(page["url"], idx, chunk_text)
        metadata: dict = {
            "url": page["url"],
            "source": page.get("source"),
            "scraped_at": page.get("scraped_at"),
            "chunk_index": idx,
            "chunk_count": len(chunks_for_page),
            "text": chunk_text,
        }
        if page.get("title") is not None:
            metadata["title"] = _truncate_meta_str(str(page["title"]), 2048) or ""
        if page.get("description"):
            metadata["description"] = page["description"]
        if page.get("language"):
            metadata["language"] = page["language"]
        for k, v in (page.get("manifest_extras") or {}).items():
            if v is None or k in metadata:
                continue
            if isinstance(v, (str, int, float, bool)):
                if isinstance(v, str):
                    metadata[k] = _truncate_meta_str(v, 8192) or ""
                else:
                    metadata[k] = v
        records.append({"id": vector_id, "metadata": metadata, "text": chunk_text})
    return records


def parse_args():
    parser = argparse.ArgumentParser(
        description="Upsert crawled page JSON (raw crawl) or prepare_ingestion manifest to Pinecone."
    )
    parser.add_argument(
        "--ingestion-dir",
        default=None,
        help="Directory containing manifest.jsonl from prepare_ingestion (alternative to raw crawl pages).",
    )
    parser.add_argument(
        "--text-source",
        choices=("markdown", "fine"),
        default="markdown",
        help="With --ingestion-dir: which file per row to chunk and embed (default: markdown).",
    )
    parser.add_argument(
        "--no-sidecar-metadata",
        action="store_true",
        help="With --ingestion-dir: do not merge metadata/*.json fields into Pinecone metadata.",
    )
    parser.add_argument("--output-dir", default="output1", help="Crawler output root directory.")
    parser.add_argument("--page-output-subdir", default="pages", help="Page JSON subdirectory name.")
    parser.add_argument(
        "--timestamp-dir",
        default="latest",
        help="Specific timestamp folder under pages/, or 'latest'.",
    )
    parser.add_argument(
        "--vector-dim",
        type=int,
        default=None,
        help="Optional expected embedding/index dimension to validate against.",
    )
    parser.add_argument(
        "--embed-model",
        default="llama-text-embed-v2",
        help="Pinecone embedding model for chunk embeddings.",
    )
    parser.add_argument("--batch-size", type=int, default=200, help="Vectors per upsert request.")
    parser.add_argument(
        "--embed-batch-size",
        type=int,
        default=64,
        help="Chunks per embedding request.",
    )
    parser.add_argument("--pool-threads", type=int, default=30, help="Pinecone async thread pool size.")
    parser.add_argument(
        "--embed-workers",
        type=int,
        default=1,
        help="Parallel embedding worker threads (default 1 to reduce TPM bursts; raise if your plan allows).",
    )
    parser.add_argument(
        "--embed-max-retries",
        type=int,
        default=12,
        help="Max retries per embed batch on HTTP 429 from Pinecone Inference (default 12).",
    )
    parser.add_argument(
        "--embed-retry-base-sec",
        type=float,
        default=3.0,
        help="Base seconds for exponential backoff on 429 (default 3).",
    )
    parser.add_argument(
        "--staging-namespace",
        default=None,
        help="Scratch namespace: cleared at start, then filled (default: PINECONE_STAGING_NAMESPACE or chunk-staging).",
    )
    parser.add_argument(
        "--namespace",
        default=None,
        help="Alias for --staging-namespace.",
    )
    parser.add_argument(
        "--live-prefix",
        default=None,
        help="Versioned live namespaces are {prefix}1, {prefix}2, … (default: PINECONE_LIVE_PREFIX or live-v-).",
    )
    parser.add_argument(
        "--delete-previous-live",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="After publishing the new live-v-N namespace, delete_all() on the previous live-v-* "
        "found at startup (highest N before this run). Safe only after the app queries the new namespace.",
    )
    parser.add_argument("--max-records", type=int, default=None, help="Optional cap for testing.")
    parser.add_argument("--chunk-size-words", type=int, default=250, help="Words per text chunk.")
    parser.add_argument("--chunk-overlap-words", type=int, default=40, help="Word overlap between chunks.")
    return parser.parse_args()


def main():
    load_dotenv()
    args = parse_args()

    api_key = os.environ.get("PINECONE_API_KEY")
    index_host = os.environ.get("PINECONE_INDEX_HOST")
    if not api_key:
        raise ValueError("Missing PINECONE_API_KEY in environment.")
    if not index_host:
        raise ValueError("Missing PINECONE_INDEX_HOST in environment.")

    if args.ingestion_dir:
        ingestion_dir = Path(args.ingestion_dir).resolve()
        if not ingestion_dir.is_dir():
            raise FileNotFoundError(f"Ingestion directory not found: {ingestion_dir}")
        print(f"Reading manifest from: {ingestion_dir / 'manifest.jsonl'} (text_source={args.text_source})")
        pages = list(
            load_pages_from_manifest(
                ingestion_dir,
                text_source=args.text_source,
                max_records=args.max_records,
                include_sidecar_metadata=not args.no_sidecar_metadata,
            )
        )
    else:
        pages_root = Path(args.output_dir) / args.page_output_subdir
        pages_dir = (
            latest_timestamp_dir(pages_root)
            if args.timestamp_dir == "latest"
            else pages_root / args.timestamp_dir
        )
        if not pages_dir.exists():
            raise FileNotFoundError(f"Pages directory not found: {pages_dir}")

        print(f"Reading pages from: {pages_dir}")

        pages = list(load_pages(pages_dir, args.max_records))
    if not pages:
        print("No eligible page records found.")
        return

    staging_ns = resolve_staging_namespace(args)
    live_prefix = resolve_live_prefix(args)

    pc = Pinecone(api_key=api_key, pool_threads=args.pool_threads)
    upserted_vectors = 0
    processed_urls = 0
    skipped_urls = 0
    all_chunk_records: list[dict] = []
    previous_live_ns: str | None = None
    new_live_ns = ""

    with pc.Index(host=index_host, pool_threads=args.pool_threads) as index:
        all_ns = collect_namespace_names(index)
        previous_live_ns, new_live_ns = previous_and_next_live_namespaces(all_ns, live_prefix)
        prev_disp = "none" if previous_live_ns is None else repr(previous_live_ns)
        print(
            f"Namespaces: staging={staging_ns!r}, new live={new_live_ns!r} "
            f"(previous live-v-* at start: {prev_disp})."
        )
        if new_live_ns == staging_ns:
            raise ValueError(
                f"Resolved new live namespace {new_live_ns!r} equals staging; change --staging-namespace or --live-prefix."
            )
        if args.delete_previous_live and previous_live_ns is not None:
            if pinecone_namespace_param(previous_live_ns) == pinecone_namespace_param(staging_ns):
                raise ValueError("Previous live namespace must not equal staging when using --delete-previous-live.")
            if previous_live_ns == new_live_ns:
                raise ValueError("Internal error: previous and new live namespaces collided.")

        tqdm.write(f"Clearing staging namespace {staging_ns!r}…", file=sys.stderr)
        try:
            index.delete(delete_all=True, namespace=staging_ns)
        except NotFoundException as e:
            if "Namespace not found" not in str(e):
                raise

        for page in tqdm(pages, desc="Building chunk records", unit="url"):
            chunk_records = build_chunk_records_for_page(
                page=page,
                chunk_size_words=args.chunk_size_words,
                chunk_overlap_words=args.chunk_overlap_words,
            )
            if not chunk_records:
                skipped_urls += 1
                continue
            all_chunk_records.extend(chunk_records)
            processed_urls += 1

        if not all_chunk_records:
            print("No chunk records generated after filtering.")
            return

        chunk_batches = list(chunks(all_chunk_records, batch_size=args.embed_batch_size))
        embedded_batches: dict[int, list[list[float]]] = {}

        def embed_batch_job(batch_idx: int, batch: list[dict]):
            response = embed_passages_with_retry(
                pc,
                args.embed_model,
                [rec["text"] for rec in batch],
                max_retries=args.embed_max_retries,
                base_delay_sec=args.embed_retry_base_sec,
            )
            return batch_idx, response

        with ThreadPoolExecutor(max_workers=max(1, int(args.embed_workers))) as executor:
            future_to_idx = {
                executor.submit(embed_batch_job, idx, list(batch)): idx
                for idx, batch in enumerate(chunk_batches)
            }
            for future in tqdm(
                as_completed(future_to_idx),
                total=len(future_to_idx),
                desc="Embedding batches",
                unit="batch",
            ):
                batch_idx, response = future.result()
                values = [item["values"] for item in response.data]
                if len(values) != len(chunk_batches[batch_idx]):
                    raise RuntimeError("Embedding API returned mismatched number of vectors.")
                if args.vector_dim is not None:
                    bad_dims = [len(v) for v in values if len(v) != args.vector_dim]
                    if bad_dims:
                        raise ValueError(
                            f"Embedding dimension mismatch. Expected {args.vector_dim}, "
                            f"got {bad_dims[0]} from model {args.embed_model}."
                        )
                embedded_batches[batch_idx] = values

        vectors: list[dict] = []
        for idx, batch in enumerate(chunk_batches):
            batch_values = embedded_batches[idx]
            for rec, values in zip(batch, batch_values, strict=True):
                vectors.append({"id": rec["id"], "values": values, "metadata": rec["metadata"]})

        upsert_batches = list(chunks(vectors, batch_size=args.batch_size))

        def upsert_batches_async(
            vector_batches: list,
            namespace: str | None,
            desc: str,
            *,
            show_batches: bool = True,
        ) -> None:
            ar = [
                index.upsert(vectors=list(b), namespace=namespace, async_req=True)
                for b in vector_batches
            ]
            iterator = tqdm(ar, desc=desc, unit="batch") if show_batches else ar
            for res in iterator:
                res.get()

        upsert_batches_async(upsert_batches, staging_ns, f"Upsert staging ({staging_ns!r})")

        upsert_batches_async(
            upsert_batches,
            new_live_ns,
            f"Publish live ({new_live_ns!r})",
        )

        tqdm.write(
            f"Point your app at namespace {new_live_ns!r} (e.g. PINECONE_NAMESPACE={new_live_ns}).",
            file=sys.stderr,
        )

        if args.delete_previous_live:
            if previous_live_ns is None:
                tqdm.write("No previous live-v-* namespace to delete (first publish).", file=sys.stderr)
            else:
                tqdm.write(
                    "Deleting previous live namespace: only safe if no clients still query "
                    f"{previous_live_ns!r}.",
                    file=sys.stderr,
                )
                try:
                    index.delete(delete_all=True, namespace=previous_live_ns)
                except NotFoundException as e:
                    if "Namespace not found" not in str(e):
                        raise
                tqdm.write(f"Deleted previous live namespace {previous_live_ns!r}.", file=sys.stderr)

        upserted_vectors = len(vectors)

    tail = ""
    if args.delete_previous_live and previous_live_ns is not None:
        tail = f" Deleted previous live {previous_live_ns!r}."
    print(
        "Upsert complete: "
        f"{upserted_vectors} chunk vectors across {processed_urls} URLs "
        f"(skipped {skipped_urls} empty pages).{tail} "
        f"Query namespace: {new_live_ns!r} (staging scratch: {staging_ns!r})."
    )


if __name__ == "__main__":
    main()
