#!/usr/bin/env python3
"""
Prepare scraper JSON output folders for RAG / embedding ingestion.

Reads recursive **/*.json page records (from scraper.py), cleans markdown, and writes:

  OUTPUT/
    markdown/          # one .md per page (cleaned, ingestion-friendly)
    fine_markdown/     # optional: LLM-refined copy (--finetune)
    metadata/          # one .json per page (url, title, paths, stats)
    manifest.jsonl       # one JSON object per line (full index for pipelines)
    skipped.jsonl        # pages skipped with reason (binary, empty, parse error)
    summary.json         # counts and options used

Example:
  python prepare_ingestion.py output_scraper_2/pages/20260420_115510 \\
      --output ingestion_ready

  python prepare_ingestion.py ... -o out --finetune --finetune-concurrency 6

Environment (see .env): FINETUNE_PROMPT, and API via FINETUNE_API_KEY or OPENROUTER_API_KEY or OPENAI_API_KEY.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import httpx
from tqdm import tqdm
from tqdm.asyncio import tqdm as tqdm_async

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # type: ignore[misc, assignment]


# Lines that are only asset links (images still allowed if they have alt text we keep as content)
_ASSET_ONLY_LINE = re.compile(
    r"^\s*!?\[([^\]]*)\]\([^)]+\.(?:css|js|woff2?|ttf|eot|map)(?:\?[^)]*)?\)\s*$",
    re.IGNORECASE,
)
# Repeated bare image lines (navigation icons)
_IMAGE_ONLY_LINE = re.compile(r"^\s*!\[\s*\]\([^)]+\)\s*$")
# Excessive repeated punctuation / noise
_NOISE_LINE = re.compile(r"^[\s*#\-_|=~.]{12,}$")


@dataclass
class IngestionRecord:
    stem: str
    jpath: Path
    data: dict
    cleaned: str
    warnings: list[str]


def _strip_control_chars(text: str) -> str:
    out: list[str] = []
    for ch in text:
        o = ord(ch)
        if ch in "\n\t":
            out.append(ch)
        elif o == 13:  # CR
            out.append("\n")
        elif o >= 32 or ch in "\u0085\u00a0":
            out.append(ch)
    return "".join(out)


def is_likely_binary_markdown(text: str) -> bool:
    """Heuristic: ZIP/office/XML binary mistaken as text."""
    if not text or not text.strip():
        return False
    head = text[:4096]
    if "PK\x03\x04" in head or head.startswith("PK\x03\x04"):
        return True
    if "<?xml" in head[:200] and "word/" in head[:2000]:
        return True
    sample = head if len(head) > 200 else text[:200]
    n = len(sample)
    if n == 0:
        return True
    bad = sum(1 for c in sample if ord(c) < 32 and c not in "\n\t\r")
    return (bad / n) > 0.08


def clean_markdown_for_ingestion(raw: str) -> tuple[str, list[str]]:
    warnings: list[str] = []
    if is_likely_binary_markdown(raw):
        warnings.append("likely_binary")

    text = raw.replace("\r\n", "\n").replace("\r", "\n")
    text = text.lstrip("\ufeff")
    text = _strip_control_chars(text)
    try:
        text = unicodedata.normalize("NFKC", text)
    except Exception:
        pass

    lines = text.split("\n")
    cleaned_lines: list[str] = []
    prev_blank = False
    image_run = 0

    for line in lines:
        stripped = line.rstrip()
        if not stripped:
            if not prev_blank:
                cleaned_lines.append("")
            prev_blank = True
            continue
        prev_blank = False

        if _NOISE_LINE.match(stripped):
            continue
        if _ASSET_ONLY_LINE.match(stripped):
            continue

        if _IMAGE_ONLY_LINE.match(stripped):
            image_run += 1
            if image_run > 6:
                continue
            cleaned_lines.append(stripped)
            continue
        image_run = 0

        cleaned_lines.append(stripped)

    out = "\n".join(cleaned_lines)
    out = re.sub(r"\n{4,}", "\n\n\n", out)
    out = out.strip()
    return out, warnings


def load_page_json(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def iter_json_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.json"))


def resolve_finetune_config() -> tuple[str, str, str, str]:
    """Returns (api_key, api_base, model, system_prompt)."""
    api_key = (
        os.environ.get("FINETUNE_API_KEY", "").strip()
        or os.environ.get("OPENROUTER_API_KEY", "").strip()
        or os.environ.get("OPENAI_API_KEY", "").strip()
    )
    default_base = (
        "https://openrouter.ai/api/v1"
        if os.environ.get("OPENROUTER_API_KEY", "").strip()
        else "https://api.openai.com/v1"
    )
    api_base = os.environ.get("FINETUNE_API_BASE", "").strip() or default_base
    model = (
        os.environ.get("FINETUNE_MODEL", "").strip()
        or os.environ.get("OPENROUTER_MODEL", "").strip()
        or "gpt-4o-mini"
    )
    prompt = os.environ.get("FINETUNE_PROMPT", "").strip()
    if not prompt:
        prompt = (
            "You are cleaning web-scraped markdown for retrieval (RAG).\n"
            "Remove boilerplate and noise; keep facts and structure.\n"
            "Output plain Markdown only, no fences or preamble."
        )
    else:
        prompt = prompt.replace("\\n", "\n")
    return api_key, api_base.rstrip("/"), model, prompt


def _truncate_input(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 80] + "\n\n[…truncated for LLM input…]\n"


async def finetune_markdown_async(
    client: httpx.AsyncClient,
    sem: asyncio.Semaphore,
    *,
    api_base: str,
    api_key: str,
    model: str,
    system_prompt: str,
    markdown: str,
    max_input_chars: int,
) -> tuple[str, str | None]:
    """Returns (fine_markdown, error_message_or_none)."""
    user_body = (
        "Clean and refine the following markdown for RAG ingestion. "
        "Output only the refined markdown.\n\n---\n\n"
        + _truncate_input(markdown, max_input_chars)
    )
    url = f"{api_base}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if "openrouter.ai" in api_base:
        headers["HTTP-Referer"] = os.environ.get("FINETUNE_HTTP_REFERER", "https://github.com/").strip()
        headers["X-Title"] = os.environ.get("FINETUNE_X_TITLE", "prepare_ingestion").strip()

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_body},
        ],
        "temperature": 0.2,
    }

    async with sem:
        try:
            r = await client.post(url, json=payload, headers=headers, timeout=180.0)
            r.raise_for_status()
            data = r.json()
            choice = (data.get("choices") or [{}])[0]
            msg = (choice.get("message") or {}).get("content")
            if not isinstance(msg, str) or not msg.strip():
                return markdown, "empty_llm_response"
            return msg.strip(), None
        except httpx.HTTPStatusError as e:
            err = e.response.text[:500] if e.response else str(e)
            return markdown, f"http_{e.response.status_code if e.response else '?'}:{err}"
        except Exception as e:
            return markdown, str(e)[:500]


async def run_finetune_batch(
    records: list[IngestionRecord],
    *,
    concurrency: int,
    max_input_chars: int,
) -> dict[str, tuple[str, str | None]]:
    """Map stem -> (fine_text, error_or_none). On error, fine_text is fallback (cleaned)."""
    api_key, api_base, model, system_prompt = resolve_finetune_config()
    if not api_key:
        raise SystemExit(
            "Finetune requires an API key: set FINETUNE_API_KEY, OPENROUTER_API_KEY, or OPENAI_API_KEY in .env"
        )

    sem = asyncio.Semaphore(max(1, concurrency))
    out: dict[str, tuple[str, str | None]] = {}

    async with httpx.AsyncClient() as client:
        tasks = [
            finetune_markdown_async(
                client,
                sem,
                api_base=api_base,
                api_key=api_key,
                model=model,
                system_prompt=system_prompt,
                markdown=rec.cleaned,
                max_input_chars=max_input_chars,
            )
            for rec in records
        ]
        results = await tqdm_async.gather(
            *tasks,
            desc="Finetune LLM",
            unit="page",
        )
        for rec, (fine, err) in zip(records, results):
            out[rec.stem] = (fine, err)

    return out


def run_prepare_ingestion(
    *,
    input_dir: Path,
    output_dir: Path,
    min_chars: int = 80,
    keep_binary: bool = False,
    finetune: bool = False,
    finetune_concurrency: int = 4,
    finetune_max_input_chars: int = 120_000,
) -> int:
    """Convert scraper JSON under ``input_dir`` into markdown + manifest under ``output_dir``."""
    if load_dotenv:
        load_dotenv()

    skip_binary = not keep_binary

    input_dir = input_dir.resolve()
    if not input_dir.is_dir():
        print(f"Not a directory: {input_dir}", file=sys.stderr)
        return 1

    out_root = output_dir.resolve()
    md_dir = out_root / "markdown"
    fine_dir = out_root / "fine_markdown"
    meta_dir = out_root / "metadata"
    md_dir.mkdir(parents=True, exist_ok=True)
    meta_dir.mkdir(parents=True, exist_ok=True)
    if finetune:
        fine_dir.mkdir(parents=True, exist_ok=True)

    files = iter_json_files(input_dir)
    if not files:
        print(f"No .json files under {input_dir}", file=sys.stderr)
        return 1

    manifest_path = out_root / "manifest.jsonl"
    skipped_path = out_root / "skipped.jsonl"

    stats: dict = {
        "input_dir": str(input_dir),
        "output_dir": str(out_root),
        "total_json": len(files),
        "written": 0,
        "skipped": 0,
        "min_chars": min_chars,
        "skip_binary_default": skip_binary,
        "finetune": bool(finetune),
        "generated_at": datetime.now(UTC).isoformat(),
    }

    records: list[IngestionRecord] = []

    with skipped_path.open("w", encoding="utf-8") as sk:
        for jpath in tqdm(files, desc="Scanning JSON", unit="file"):
            data = load_page_json(jpath)
            if data is None:
                sk.write(
                    json.dumps({"file": str(jpath), "reason": "json_parse_error"}, ensure_ascii=False)
                    + "\n"
                )
                stats["skipped"] += 1
                continue

            if data.get("error"):
                sk.write(
                    json.dumps(
                        {
                            "file": str(jpath),
                            "url": data.get("url"),
                            "reason": "scrape_error",
                            "error": data.get("error"),
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
                stats["skipped"] += 1
                continue

            raw_md = data.get("markdown")
            if not isinstance(raw_md, str):
                sk.write(
                    json.dumps(
                        {"file": str(jpath), "url": data.get("url"), "reason": "no_markdown_field"},
                        ensure_ascii=False,
                    )
                    + "\n"
                )
                stats["skipped"] += 1
                continue

            cleaned, warnings = clean_markdown_for_ingestion(raw_md)
            if skip_binary and "likely_binary" in warnings:
                sk.write(
                    json.dumps(
                        {
                            "file": str(jpath),
                            "url": data.get("url"),
                            "reason": "likely_binary",
                            "warnings": warnings,
                            "cleaned_len": len(cleaned),
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
                stats["skipped"] += 1
                continue

            if len(cleaned) < min_chars:
                sk.write(
                    json.dumps(
                        {
                            "file": str(jpath),
                            "url": data.get("url"),
                            "reason": "too_short",
                            "cleaned_len": len(cleaned),
                            "min_chars": min_chars,
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
                stats["skipped"] += 1
                continue

            stem = jpath.stem or "page"
            records.append(IngestionRecord(stem=stem, jpath=jpath, data=data, cleaned=cleaned, warnings=warnings))

    finetune_results: dict[str, tuple[str, str | None]] = {}
    if finetune and records:
        _, api_base, model_used, _ = resolve_finetune_config()
        tqdm.write(
            f"Finetune: {len(records)} pages, model={model_used}, base={api_base}, "
            f"concurrency={finetune_concurrency}",
            file=sys.stderr,
        )
        finetune_results = asyncio.run(
            run_finetune_batch(
                records,
                concurrency=finetune_concurrency,
                max_input_chars=finetune_max_input_chars,
            )
        )

    finetune_model_name = ""
    if finetune:
        _, _, finetune_model_name, _ = resolve_finetune_config()

    with manifest_path.open("w", encoding="utf-8") as mf:
        for rec in tqdm(records, desc="Writing output", unit="page"):
            md_file = md_dir / f"{rec.stem}.md"
            md_file.write_text(rec.cleaned + "\n", encoding="utf-8")

            fine_rel: str | None = None
            fine_err: str | None = None
            fine_text = rec.cleaned
            if finetune and rec.stem in finetune_results:
                fine_text, fine_err = finetune_results[rec.stem]
                fine_file = fine_dir / f"{rec.stem}.md"
                fine_file.write_text(fine_text + "\n", encoding="utf-8")
                fine_rel = str(fine_file.relative_to(out_root))

            meta: dict = {
                "url": rec.data.get("url"),
                "source": rec.data.get("source"),
                "title": (rec.data.get("metadata") or {}).get("title")
                if isinstance(rec.data.get("metadata"), dict)
                else None,
                "description": (rec.data.get("metadata") or {}).get("description")
                if isinstance(rec.data.get("metadata"), dict)
                else None,
                "language": (rec.data.get("metadata") or {}).get("language")
                if isinstance(rec.data.get("metadata"), dict)
                else None,
                "scraped_at": rec.data.get("scraped_at"),
                "source_json": str(rec.jpath),
                "markdown_file": str(md_file.relative_to(out_root)),
                "char_count": len(rec.cleaned),
                "warnings": rec.warnings,
            }
            if finetune:
                meta["fine_markdown_file"] = fine_rel
                meta["fine_char_count"] = len(fine_text)
                meta["finetune_model"] = finetune_model_name
                if fine_err:
                    meta["finetune_error"] = fine_err

            meta_file = meta_dir / f"{rec.stem}.json"
            meta_file.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            row: dict = {
                "id": rec.stem,
                "url": meta["url"],
                "title": meta["title"],
                "markdown_path": str(md_file.relative_to(out_root)),
                "metadata_path": str(meta_file.relative_to(out_root)),
                "char_count": len(rec.cleaned),
            }
            if finetune and fine_rel:
                row["fine_markdown_path"] = fine_rel
                row["fine_char_count"] = len(fine_text)

            mf.write(json.dumps(row, ensure_ascii=False) + "\n")
            stats["written"] += 1

    stats["skipped_total"] = stats["skipped"]
    summary_path = out_root / "summary.json"
    summary_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")

    print(f"Wrote {stats['written']} pages to {out_root}")
    print(f"  markdown/   — {stats['written']} .md files")
    if finetune:
        print(f"  fine_markdown/ — {stats['written']} .md files (LLM)")
    print(f"  metadata/   — sidecar JSON per page")
    print(f"  manifest.jsonl — one line per ingested doc")
    print(f"Skipped {stats['skipped']} → skipped.jsonl")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert scraper page JSON folders into cleaned markdown for ingestion."
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Folder containing scraper *.json files (searched recursively)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        required=True,
        help="Output directory (created if missing)",
    )
    parser.add_argument(
        "--min-chars",
        type=int,
        default=80,
        help="Minimum cleaned character count to keep a page (default 80)",
    )
    parser.add_argument(
        "--keep-binary",
        action="store_true",
        help="Include pages that look like ZIP/Office binary mistaken as markdown (default: skip them)",
    )
    parser.add_argument(
        "--finetune",
        action="store_true",
        help="Run each kept page through one LLM call; write fine_markdown/ (uses .env FINETUNE_PROMPT and API keys)",
    )
    parser.add_argument(
        "--finetune-concurrency",
        type=int,
        default=4,
        metavar="N",
        help="Max concurrent LLM requests with --finetune (default 4)",
    )
    parser.add_argument(
        "--finetune-max-input-chars",
        type=int,
        default=120_000,
        help="Truncate cleaned markdown past this length before the LLM call (default 120000)",
    )
    args = parser.parse_args()
    return run_prepare_ingestion(
        input_dir=args.input_dir,
        output_dir=args.output,
        min_chars=args.min_chars,
        keep_binary=args.keep_binary,
        finetune=args.finetune,
        finetune_concurrency=args.finetune_concurrency,
        finetune_max_input_chars=args.finetune_max_input_chars,
    )


if __name__ == "__main__":
    raise SystemExit(main())
