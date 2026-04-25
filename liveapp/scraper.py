"""Fetch a single URL and convert it to a PageResult.

Freshness logic
---------------
If `last_scraped_at` is provided (a previous scrape timestamp stored in the DB),
the request is sent with an ``If-Modified-Since`` header.  A 304 response means
the page hasn't changed — we return a ``not_modified`` result immediately without
re-processing anything.  A 200 means new content; we parse and hash it.

Content hash
------------
A short SHA-256 prefix of the raw HTML body lets us detect changes even for
servers that don't honour ``If-Modified-Since``.
"""

from __future__ import annotations

import hashlib
from datetime import datetime
from urllib.parse import urldefrag, urljoin, urlparse

import html2text
import requests
from bs4 import BeautifulSoup

from .schemas import PageResult


def normalize(url: str) -> str:
    url, _ = urldefrag(url)
    p = urlparse(url)
    return p._replace(scheme=p.scheme.lower(), netloc=p.netloc.lower()).geturl()


def fetch_and_process(
    *,
    url: str,
    seed_url: str,
    purpose: str,
    depth: int,
    session: requests.Session,
    last_scraped_at: str | None = None,
    force: bool = False,
) -> PageResult:
    now = datetime.utcnow().isoformat()

    headers: dict[str, str] = {}
    if last_scraped_at and not force:
        headers["If-Modified-Since"] = last_scraped_at

    try:
        resp = session.get(url, headers=headers, timeout=15, allow_redirects=True)
    except requests.RequestException as exc:
        return PageResult(
            url=url, seed_url=seed_url, purpose=purpose, depth=depth,
            status="error", error=str(exc), scraped_at=now,
        )

    # Server says nothing changed since we last scraped — skip processing.
    if resp.status_code == 304:
        return PageResult(
            url=url, seed_url=seed_url, purpose=purpose, depth=depth,
            status="not_modified", scraped_at=now,
            last_modified=last_scraped_at,
        )

    if resp.status_code != 200:
        return PageResult(
            url=url, seed_url=seed_url, purpose=purpose, depth=depth,
            status="error", scraped_at=now,
            error=f"HTTP {resp.status_code}",
        )

    content_type = resp.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        return PageResult(
            url=url, seed_url=seed_url, purpose=purpose, depth=depth,
            status="skipped", scraped_at=now,
            error=f"non-HTML content-type: {content_type}",
        )

    last_modified = resp.headers.get("Last-Modified")
    content_hash = hashlib.sha256(resp.content).hexdigest()[:16]

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove navigational chrome so markdown is content-only.
    for tag in soup.select("nav, footer, aside, script, style, [role='navigation']"):
        tag.decompose()

    # Convert to markdown — mirrors what Firecrawl produces.
    h2t = html2text.HTML2Text()
    h2t.ignore_images = False
    h2t.ignore_links = False
    h2t.body_width = 0
    markdown = h2t.handle(str(soup.body or soup)).strip()

    # Structured metadata.
    def _meta(name: str | None = None, prop: str | None = None) -> str | None:
        attrs = {"name": name} if name else {"property": prop}
        tag = soup.find("meta", attrs=attrs)
        return tag.get("content", "").strip() if tag else None  # type: ignore[union-attr]

    title = soup.title.get_text(strip=True) if soup.title else None
    metadata = {
        "title": title,
        "description": _meta(name="description") or _meta(prop="og:description"),
        "og_title": _meta(prop="og:title"),
        "og_image": _meta(prop="og:image"),
        "language": soup.html.get("lang") if soup.html else None,
        "content_type": content_type,
    }

    # Collect all absolute links (skip mailto / tel / js).
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href.startswith(("mailto:", "tel:", "javascript:")):
            links.append(normalize(urljoin(url, href)))

    return PageResult(
        url=url,
        seed_url=seed_url,
        purpose=purpose,
        depth=depth,
        status="scraped",
        title=title,
        markdown=markdown,
        metadata=metadata,
        links=links,
        content_hash=content_hash,
        last_modified=last_modified,
        scraped_at=now,
    )
