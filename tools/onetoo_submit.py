#!/usr/bin/env python3
"""
HGPEdu ↔ ONETOO integration helper (NEW standard: read-only status sync).

Why this file is still called onetoo_submit.py:
- Historically it was intended to POST into ONETOO contrib endpoints.
- Since ONETOO Universal Backend moved to a public GET-only surface (e.g. /search/v1),
  HGPEdu should NOT attempt to push data upstream automatically.
- Instead, we keep a transparent local ledger and periodically check whether a URL
  is already visible in the ONETOO accepted-set (search index).

What this tool does:
- reads portal feed items from data/portal/index.json
- calls: GET https://search.onetoo.eu/search/v1?q=<url>
- if it finds an exact URL match in results[] -> status = "accepted"
- if not found -> status = "missing"
- on errors -> status = "error"
- writes portal/submissions.json (machine-readable ledger)
- can be used in GitHub Actions (no secrets required)

Safe by design:
- NO POST requests to ONETOO
- NO tokens required
- deterministic and auditable
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse, quote
import urllib.request
import urllib.error


SEARCH_ENDPOINT_DEFAULT = "https://search.onetoo.eu/search/v1"
CANONICAL_SITE = "https://hgpedu.eu"
PORTAL_INDEX_URL = f"{CANONICAL_SITE}/data/portal/index.json"
TFWS_V2_URL = f"{CANONICAL_SITE}/.well-known/tfws-v2.json"


def utc_now() -> str:
    # timezone-aware UTC timestamp (no deprecation warning)
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def is_https(u: str) -> bool:
    try:
        p = urlparse(u)
        return p.scheme == "https" and bool(p.netloc)
    except Exception:
        return False


def normalize_url(u: str) -> str:
    """Normalize trivial variants (strip whitespace, remove trailing slash)."""
    u = (u or "").strip()
    if u.endswith("/") and u != "https://":
        u = u[:-1]
    return u


def build_publisher() -> dict:
    return {
        "name": "HGPEdu",
        "domain": "hgpedu.eu",
        "homepage": CANONICAL_SITE,
        "tfws": {"v2": TFWS_V2_URL},
        "portal_index": PORTAL_INDEX_URL,
    }


def portal_items(portal: dict) -> List[dict]:
    """
    Accept both historical shapes:
    - { "items": [...] }  (current HGPEdu portal index)
    - { "entries": [...] } (older drafts)
    """
    items = portal.get("items")
    if isinstance(items, list):
        return [x for x in items if isinstance(x, dict)]
    entries = portal.get("entries")
    if isinstance(entries, list):
        return [x for x in entries if isinstance(x, dict)]
    return []


def http_get_json(url: str, timeout: int = 25) -> Tuple[int, dict | str]:
    req = urllib.request.Request(url, method="GET")
    req.add_header("accept", "application/json")
    req.add_header("user-agent", "hgpedu-onetoo-status-sync/1.0 (+https://hgpedu.eu)")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                return resp.status, json.loads(raw)
            except Exception:
                return resp.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, raw
    except Exception as e:
        return 0, str(e)


def check_url_in_onetoo(url: str, endpoint: str, limit: int) -> Tuple[str, int, dict | str]:
    """
    Returns: (status, http_code, response)
    status in: accepted | missing | error
    """
    q = quote(url, safe="")
    full = f"{endpoint}?q={q}&limit={max(1, min(50, int(limit)))}"
    code, resp = http_get_json(full)

    if not (200 <= code < 300) or not isinstance(resp, dict):
        return "error", code, resp

    results = resp.get("results", [])
    if not isinstance(results, list):
        return "error", code, resp

    target = normalize_url(url)
    for r in results:
        if not isinstance(r, dict):
            continue
        rurl = normalize_url(str(r.get("url", "")))
        if rurl == target:
            return "accepted", code, resp

        # fallback: consider www/non-www equivalence
        if rurl.replace("https://www.", "https://") == target.replace("https://www.", "https://"):
            return "accepted", code, resp

    return "missing", code, resp


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--search-endpoint", default=SEARCH_ENDPOINT_DEFAULT, help="ONETOO search endpoint (/search/v1)")
    ap.add_argument("--portal-index", default="data/portal/index.json", help="Local portal feed JSON path")
    ap.add_argument("--state", default="portal/submissions.json", help="Local status ledger JSON path")
    ap.add_argument("--limit", type=int, default=50, help="Max entries to process per run")
    ap.add_argument("--query-limit", type=int, default=50, help="limit= query param for /search/v1 (1..50)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only-url", default="", help="Check only this URL")
    ap.add_argument("--sleep", type=float, default=0.5, help="Delay between requests (seconds)")
    args = ap.parse_args()

    portal_path = Path(args.portal_index)
    portal = load_json(portal_path, {})
    items = portal_items(portal)

    state_path = Path(args.state)
    state = load_json(
        state_path,
        {
            "schema_version": "hgpedu.onetoo.status.v1",
            "generated_utc": utc_now(),
            "publisher": build_publisher(),
            "items": {},
        },
    )

    ledger: Dict[str, Any] = state.get("items", {})
    if not isinstance(ledger, dict):
        ledger = {}

    processed = 0
    for it in items:
        url = normalize_url(str(it.get("url", "")))
        if not url or not is_https(url):
            continue
        if args.only_url and normalize_url(args.only_url) != url:
            continue

        status, code, resp = check_url_in_onetoo(url, args.search_endpoint, args.query_limit)

        ledger[url] = {
            "status": status,
            "http": int(code),
            "checked_utc": utc_now(),
        }

        # store a short debug sample only on errors (avoid noisy churn)
        if status == "error":
            if isinstance(resp, str):
                ledger[url]["error"] = resp[:500]
            else:
                ledger[url]["error"] = json.dumps(resp, ensure_ascii=False)[:500]

        line = f"{status.upper():8} {url} (HTTP {code})"
        print(line if status != "error" else "ERROR   " + line, file=sys.stderr if status == "error" else sys.stdout)

        processed += 1
        if processed >= int(args.limit):
            break
        time.sleep(max(0.0, float(args.sleep)))

    state["generated_utc"] = utc_now()
    state["items"] = ledger

    if args.dry_run:
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0

    save_json(state_path, state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
