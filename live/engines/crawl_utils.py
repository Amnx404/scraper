from __future__ import annotations

import json
import os
import re
from hashlib import md5
from urllib.parse import parse_qsl, quote, unquote, urldefrag, urlencode, urlparse, urlunparse

_DYNAMIC_QUERY_KEYS = frozenset(
    {
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_term",
        "utm_content",
        "utm_id",
        "fbclid",
        "gclid",
        "gbraid",
        "wbraid",
        "msclkid",
        "yclid",
        "_ga",
        "_gl",
        "mc_cid",
        "mc_eid",
        "mkt_tok",
        "ref",
        "referrer",
        "referer",
        "igshid",
        "si",
        "ved",
        "ei",
        "session",
        "sid",
        "phpsessid",
        "jsessionid",
        "asp.net_sessionid",
        "nocache",
        "cache",
        "t",
        "ts",
        "time",
        "timestamp",
        "rnd",
        "random",
        "_",
        "_hsenc",
        "_hssc",
        "_hssrc",
        "_openstat",
    }
)


def _is_dynamic_query_key(key: str) -> bool:
    k = key.lower()
    if k.startswith("utm_"):
        return True
    if k.startswith("_hs") or k.startswith("hs_"):
        return True
    return k in _DYNAMIC_QUERY_KEYS


def canonicalize_url(url: str) -> str | None:
    if not url or not isinstance(url, str):
        return None
    url = url.strip()
    if not url:
        return None
    url, _frag = urldefrag(url)
    for bad in ('"', "'", "\\", "\n", "\r", "\t", "<", ">", "{", "}"):
        if bad in url:
            return None
    try:
        p = urlparse(url)
    except ValueError:
        return None
    scheme = (p.scheme or "").lower()
    if scheme not in ("http", "https"):
        return None
    netloc = (p.netloc or "").lower().strip()
    if not netloc:
        return None
    if scheme == "http" and netloc.endswith(":80"):
        netloc = netloc[:-3]
    elif scheme == "https" and netloc.endswith(":443"):
        netloc = netloc[:-4]

    path = unquote(p.path or "")
    if not path.startswith("/"):
        path = "/" + path
    path = os.path.normpath(path).replace("\\", "/")
    if path == ".":
        path = "/"
    segments = []
    for seg in path.split("/"):
        if not seg:
            continue
        segments.append(quote(seg, safe="-_.~"))
    path = "/" + "/".join(segments) if segments else "/"

    if p.query:
        pairs = [
            (k, v)
            for k, v in parse_qsl(p.query, keep_blank_values=True)
            if not _is_dynamic_query_key(k)
        ]
        pairs.sort(key=lambda x: (x[0], x[1]))
        query = urlencode(pairs, doseq=True) if pairs else ""
    else:
        query = ""

    return urlunparse((scheme, netloc, path, "", query, ""))


def make_prefix(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    norm = canonicalize_url(url)
    if norm is None:
        return url.rstrip("/") + "/"
    last_segment = urlparse(norm).path.rstrip("/").split("/")[-1]
    if "." not in last_segment:
        norm = norm.rstrip("/") + "/"
    return norm


def slug(url: str) -> str:
    p = urlparse(url)
    base = p.netloc + p.path.rstrip("/")
    return re.sub(r"[^\w\-]", "_", base).strip("_")


def url_output_filename(url: str) -> str:
    norm = canonicalize_url(url) or url
    short_hash = md5(norm.encode("utf-8")).hexdigest()[:10]
    return f"{slug(norm)}_{short_hash}.json"


def atomic_write_json(path: str, obj: dict) -> None:
    d = os.path.dirname(path) or "."
    os.makedirs(d, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
