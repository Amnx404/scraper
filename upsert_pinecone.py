import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import itertools
import json
import os
from pathlib import Path

from pinecone import Pinecone
from pinecone.exceptions import NotFoundException
from dotenv import load_dotenv
from tqdm import tqdm


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
    for idx, chunk_text in enumerate(chunks_for_page):
        vector_id = chunk_id_for_url(page["url"], idx, chunk_text)
        metadata = {
            "url": page["url"],
            "source": page.get("source"),
            "scraped_at": page.get("scraped_at"),
            "chunk_index": idx,
            "chunk_count": len(chunks_for_page),
            "text": chunk_text,
        }
        records.append({"id": vector_id, "metadata": metadata, "text": chunk_text})
    return records


def parse_args():
    parser = argparse.ArgumentParser(description="Upsert crawled page JSON files to Pinecone.")
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
        default=4,
        help="Parallel embedding worker threads.",
    )
    parser.add_argument("--namespace", default=None, help="Optional Pinecone namespace.")
    parser.add_argument("--max-records", type=int, default=None, help="Optional cap for testing.")
    parser.add_argument("--chunk-size-words", type=int, default=250, help="Words per text chunk.")
    parser.add_argument("--chunk-overlap-words", type=int, default=40, help="Word overlap between chunks.")
    parser.add_argument(
        "--replace-existing-by-url",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Delete existing vectors for each URL before upserting new chunks.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    api_key = os.environ.get("PINECONE_API_KEY")
    index_host = os.environ.get("PINECONE_INDEX_HOST")
    if not api_key:
        raise ValueError("Missing PINECONE_API_KEY in environment.")
    if not index_host:
        raise ValueError("Missing PINECONE_INDEX_HOST in environment.")

    pages_root = Path(args.output_dir) / args.page_output_subdir
    pages_dir = latest_timestamp_dir(pages_root) if args.timestamp_dir == "latest" else pages_root / args.timestamp_dir
    if not pages_dir.exists():
        raise FileNotFoundError(f"Pages directory not found: {pages_dir}")

    print(f"Reading pages from: {pages_dir}")

    pages = list(load_pages(pages_dir, args.max_records))
    if not pages:
        print("No eligible page records found.")
        return

    pc = Pinecone(api_key=api_key, pool_threads=args.pool_threads)
    upserted_vectors = 0
    processed_urls = 0
    skipped_urls = 0
    all_chunk_records: list[dict] = []

    with pc.Index(host=index_host, pool_threads=args.pool_threads) as index:
        for page in tqdm(pages, desc="Deleting existing by URL", unit="url"):
            if args.replace_existing_by_url:
                try:
                    index.delete(filter={"url": {"$eq": page["url"]}}, namespace=args.namespace)
                except NotFoundException as e:
                    # Deleting from a namespace that does not exist yet should be treated as no-op.
                    if "Namespace not found" not in str(e):
                        raise

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
        with ThreadPoolExecutor(max_workers=max(1, int(args.embed_workers))) as executor:
            future_to_idx = {
                executor.submit(
                    pc.inference.embed,
                    model=args.embed_model,
                    inputs=[rec["text"] for rec in batch],
                    parameters={"input_type": "passage", "truncate": "END"},
                ): idx
                for idx, batch in enumerate(chunk_batches)
            }
            for future in tqdm(
                as_completed(future_to_idx),
                total=len(future_to_idx),
                desc="Embedding batches",
                unit="batch",
            ):
                idx = future_to_idx[future]
                response = future.result()
                values = [item["values"] for item in response.data]
                if len(values) != len(chunk_batches[idx]):
                    raise RuntimeError("Embedding API returned mismatched number of vectors.")
                if args.vector_dim is not None:
                    bad_dims = [len(v) for v in values if len(v) != args.vector_dim]
                    if bad_dims:
                        raise ValueError(
                            f"Embedding dimension mismatch. Expected {args.vector_dim}, "
                            f"got {bad_dims[0]} from model {args.embed_model}."
                        )
                embedded_batches[idx] = values

        vectors: list[dict] = []
        for idx, batch in enumerate(chunk_batches):
            batch_values = embedded_batches[idx]
            for rec, values in zip(batch, batch_values, strict=True):
                vectors.append({"id": rec["id"], "values": values, "metadata": rec["metadata"]})

        upsert_batches = list(chunks(vectors, batch_size=args.batch_size))
        async_results = [
            index.upsert(vectors=vector_batch, namespace=args.namespace, async_req=True)
            for vector_batch in upsert_batches
        ]
        for async_result in tqdm(async_results, desc="Upserting batches", unit="batch"):
            async_result.get()

        upserted_vectors = len(vectors)

    print(
        "Upsert complete: "
        f"{upserted_vectors} chunk vectors across {processed_urls} URLs "
        f"(skipped {skipped_urls} empty pages)."
    )


if __name__ == "__main__":
    load_dotenv()
    main()
