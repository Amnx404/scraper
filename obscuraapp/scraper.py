"""Fetch a single page through an Obscura/Playwright CDP connection.

Markdown extraction order
-------------------------
1. LP.getMarkdown() — Obscura's native DOM-to-Markdown via the LP CDP domain.
   This is the whole point of using Obscura: it converts the live rendered DOM
   (post-JS, post-stealth) directly to clean markdown without any Python-side
   HTML parsing.
2. html2text fallback — used when connected to a plain Playwright/Chrome instance
   that doesn't have the LP domain.

Freshness
---------
If `last_scraped_at` is given, the page's response headers are intercepted to
check Last-Modified before committing to a full render.  A matching date means
we return `not_modified` immediately.
"""

from __future__ import annotations

import hashlib
from datetime import datetime
from urllib.parse import urldefrag, urljoin, urlparse

import html2text
from bs4 import BeautifulSoup
from playwright.async_api import Page, Response

from liveapp.schemas import PageResult


def _normalize(url: str) -> str:
    url, _ = urldefrag(url)
    p = urlparse(url)
    return p._replace(scheme=p.scheme.lower(), netloc=p.netloc.lower()).geturl()


async def _lp_markdown(page: Page) -> str | None:
    """Call Obscura's LP.getMarkdown via CDP. Returns None if not available."""
    try:
        cdp = await page.context.new_cdp_session(page)
        result = await cdp.send("LP.getMarkdown")
        await cdp.detach()
        return result.get("markdown") or None
    except Exception:
        return None


async def _html2text_markdown(page: Page) -> str:
    """Fallback: grab rendered HTML and convert with html2text."""
    html = await page.content()
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.select("nav, footer, aside, script, style, [role='navigation']"):
        tag.decompose()
    h = html2text.HTML2Text()
    h.ignore_images = False
    h.ignore_links = False
    h.body_width = 0
    return h.handle(str(soup.body or soup)).strip()


async def fetch_page(
    *,
    url: str,
    seed_url: str,
    purpose: str,
    depth: int,
    page: Page,
    last_scraped_at: str | None = None,
    force: bool = False,
    wait_until: str = "networkidle",
    timeout: int = 30_000,
    use_lp_markdown: bool = True,
) -> PageResult:
    now = datetime.utcnow().isoformat()
    last_modified_seen: list[str] = []

    # Intercept response headers for Last-Modified / freshness check.
    async def _on_response(resp: Response) -> None:
        if resp.url == url or resp.url.rstrip("/") == url.rstrip("/"):
            lm = resp.headers.get("last-modified")
            if lm:
                last_modified_seen.append(lm)
            # If server says not modified (shouldn't happen on GET, but some do).
            if resp.status == 304 and not force:
                last_modified_seen.append("__304__")

    page.on("response", _on_response)

    # If we have a prior timestamp, set the request header for cheap bypass.
    if last_scraped_at and not force:
        await page.set_extra_http_headers({"If-Modified-Since": last_scraped_at})

    try:
        response = await page.goto(
            url, wait_until=wait_until, timeout=timeout  # type: ignore[arg-type]
        )
    except Exception as exc:
        return PageResult(
            url=url, seed_url=seed_url, purpose=purpose, depth=depth,
            status="error", error=str(exc), scraped_at=now,
        )
    finally:
        page.remove_listener("response", _on_response)

    if response is None:
        return PageResult(
            url=url, seed_url=seed_url, purpose=purpose, depth=depth,
            status="error", error="no response", scraped_at=now,
        )

    # 304 or header match → skip re-processing.
    last_modified = last_modified_seen[0] if last_modified_seen else None
    if "__304__" in last_modified_seen or (
        last_scraped_at
        and not force
        and last_modified
        and last_modified == last_scraped_at
    ):
        return PageResult(
            url=url, seed_url=seed_url, purpose=purpose, depth=depth,
            status="not_modified", scraped_at=now, last_modified=last_modified,
        )

    if response.status not in (200, 203):
        return PageResult(
            url=url, seed_url=seed_url, purpose=purpose, depth=depth,
            status="error", scraped_at=now, error=f"HTTP {response.status}",
        )

    # --- Markdown extraction ---
    markdown: str | None = None
    if use_lp_markdown:
        markdown = await _lp_markdown(page)
    if not markdown:
        markdown = await _html2text_markdown(page)

    # --- Metadata ---
    title = await page.title()
    description = await page.evaluate(
        "() => (document.querySelector('meta[name=description]') || "
        "document.querySelector('meta[property=\"og:description\"]') || {}).content || null"
    )
    og_title = await page.evaluate(
        "() => (document.querySelector('meta[property=\"og:title\"]') || {}).content || null"
    )
    lang = await page.evaluate("() => document.documentElement.lang || null")

    metadata = {
        "title": title,
        "description": description,
        "og_title": og_title,
        "language": lang,
        "status_code": response.status,
    }

    # --- Links ---
    hrefs: list[str] = await page.evaluate(
        "() => Array.from(document.querySelectorAll('a[href]')).map(a => a.href)"
    )
    links = [
        _normalize(h) for h in hrefs
        if not h.startswith(("mailto:", "tel:", "javascript:", "data:"))
    ]

    content_hash = hashlib.sha256(markdown.encode()).hexdigest()[:16]

    return PageResult(
        url=url,
        seed_url=seed_url,
        purpose=purpose,
        depth=depth,
        status="scraped",
        title=title or None,
        markdown=markdown,
        metadata=metadata,
        links=links,
        content_hash=content_hash,
        last_modified=last_modified,
        scraped_at=now,
    )
