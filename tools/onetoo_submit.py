#!/usr/bin/env python3
"""
Submit HGPEdu portal entries to ONETOO AI Search (contrib API).

Goals:
- autonomous: runs in GitHub Actions with secrets
- idempotent: tracks submitted URLs in portal/submissions.json
- transparent: writes machine-readable state + prints clear errors
- canonical: uses https://hgpedu.eu (no www) everywhere

NOTE:
The exact submit payload may evolve. Adjust `build_payload()` to match ONETOO OpenAPI.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
import urllib.request
import urllib.error


DEFAULT_ENDPOINT = "https://search.onetoo.eu/contrib/v2/submit"

CANONICAL_SITE = "https://hgpedu.eu"
PORTAL_INDEX_URL = f"{CANONICAL_SITE}/data/portal/index.json"
TFWS_V2_URL = f"{CANONICAL_SITE}/.well-known/tfws-v2.json"


def utc_now() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


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


def compact(obj: Any) -> Any:
    """
    Remove empty/null-ish values recursively for cleaner payloads.
    Keeps 0 and False.
    """
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            vv = compact(v)
            if vv is None:
                continue
            if vv == "" or vv == [] or vv == {}:
                continue
            out[k] = vv
        return out
    if isinstance(obj, list):
        out = [compact(x) for x in obj]
        out = [x for x in out if x is not None and x != "" and x != [] and x != {}]
        return out
    return obj


def build_publisher() -> dict:
    return {
        "name": "HGPEdu",
        "domain": "hgpedu.eu",
        "homepage": CANONICAL_SITE,
        "tfws": {
            "v2": TFWS_V2_URL,
        },
        # Optional: link to trust hub/integrity if ONETOO schema supports it.
        # "trust_hub": f"{CANONICAL_SITE}/ai-trust-hub.json",
        # "integrity": f"{CANONICAL_SITE}/.well-known/sha256.json",
    }


def build_payload(entry: dict, publisher: dict) -> dict:
    """
    Build ONETOO submit payload.

    Current mapping (safe default):
    - title, url
    - description (from notes/summary fields)
    - categories + tags
    - publisher
    - manifests (if provided)
    - source backlink to HGPEdu portal index

    Adjust this function if ONETOO OpenAPI differs.
    """
    title = (entry.get("title") or "").strip()
    url = (entry.get("url") or "").strip()

    # Try to accept multiple possible fields for "description".
    description = (
        (entry.get("notes") or "").strip()
        or (entry.get("summary") or "").strip()
        or ""
    )

    # categories: accept either "category" (single) or "categories" (list)
    categories = []
    if isinstance(entry.get("categories"), list):
        categories = [str(x).strip() for x in entry.get("categories", []) if str(x).strip()]
    elif entry.get("category"):
        categories = [str(entry.get("category")).strip()]

    tags = entry.get("tags", [])
    if not isinstance(tags, list):
        tags = []

    manifests = entry.get("manifests", {})
    if not isinstance(manifests, dict):
        manifests = {}

    payload = {
        "title": title,
        "url": url,
        "description": description,
        "categories": categories,
        "tags": tags,
        "publisher": publisher,
        "manifests": manifests,
        "source": {
            "type": "hgpedu-portal",
            "portal_index": PORTAL_INDEX_URL,
            "submitted_utc": utc_now(),
        },
    }

    return compact(payload)


def post_json(url: str, data: dict, token: str | None, timeout: int = 25) -> tuple[int, dict | str]:
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    req.add_header("User-Agent", "hgpedu-onetoo-submit/1.0 (+https://hgpedu.eu)")

    if token:
        # Token style can differ; change header if ONETOO expects something else.
        req.add_header("Authorization", f"Bearer {token}")

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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", default=os.environ.get("ONETOO_SUBMIT_ENDPOINT", DEFAULT_ENDPOINT))
    ap.add_argument("--token", default=os.environ.get("ONETOO_TOKEN"))
    ap.add_argument("--portal-index", default="data/portal/index.json", help="Local portal feed JSON path")
    ap.add_argument("--state", default="portal/submissions.json", help="Local submission state JSON path")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only-url", default="", help="Submit only this URL if present in portal entries")
    ap.add_argument("--sleep", type=float, default=1.0, help="Delay between submits (seconds)")
    args = ap.parse_args()

    portal_path = Path(args.portal_index)
    portal = load_json(portal_path, {})
    entries = portal.get("entries", [])

    if not isinstance(entries, list):
        print(f"ERROR: {portal_path} entries must be an array", file=sys.stderr)
        return 2

    state_path = Path(args.state)
    state = load_json(
        state_path,
        {
            "schema_version": "hgpedu.onetoo.submissions.v1",
            "generated_utc": utc_now(),
            "items": {},
        },
    )

    items = state.get("items", {})
    if not isinstance(items, dict):
        items = {}

    publisher = build_publisher()

    submitted = 0
    for entry in entries:
        if not isinstance(entry, dict):
            continue

        url = str(entry.get("url", "")).strip()
        title = str(entry.get("title", "")).strip()

        if not url or not title:
            continue
        if not is_https(url):
            continue

        if args.only_url and url != args.only_url.strip():
            continue

        # idempotency
        if url in items and items[url].get("status") in ("submitted", "accepted"):
            continue

        payload = build_payload(entry, publisher)

        if args.dry_run:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            items[url] = {"status": "dry-run", "last_attempt_utc": utc_now()}
            submitted += 1
            if submitted >= args.limit:
                break
            continue

        code, resp = post_json(args.endpoint, payload, args.token)

        ok = 200 <= code < 300
        items[url] = {
            "status": "submitted" if ok else "error",
            "http": code,
            "last_attempt_utc": utc_now(),
            "response": resp,
        }

        if ok:
            print(f"OK   {url} -> HTTP {code}")
        else:
            print(f"FAIL {url} -> HTTP {code}", file=sys.stderr)
            if isinstance(resp, str):
                print(resp[:2000], file=sys.stderr)
            else:
                print(json.dumps(resp, ensure_ascii=False, indent=2)[:2000], file=sys.stderr)

        submitted += 1
        if submitted >= args.limit:
            break
        time.sleep(max(0.0, float(args.sleep)))

    state["generated_utc"] = utc_now()
    state["items"] = items
    save_json(state_path, state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())