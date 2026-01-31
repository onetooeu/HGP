#!/usr/bin/env python3
"""Submit HGPEdu portal entries to ONETOO AI Search (contrib API).

Design goals:
- autonomous: can run in GitHub Actions with secrets
- idempotent: tracks submitted URLs in portal/submissions.json
- transparent: writes a machine-readable log and prints clear errors

NOTE: The exact submit payload may evolve. This tool supports a flexible adapter:
- Edit `build_payload()` to match current ONETOO OpenAPI schema.
"""

from __future__ import annotations
import argparse, json, os, sys, time
from pathlib import Path
from urllib.parse import urlparse
import urllib.request

DEFAULT_ENDPOINT = "https://search.onetoo.eu/contrib/v2/submit"

def utc_now() -> str:
    import datetime
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def load_json(p: Path, default):
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))

def save_json(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def is_https(u: str) -> bool:
    try:
        p = urlparse(u)
        return p.scheme == "https" and bool(p.netloc)
    except Exception:
        return False

def build_payload(entry: dict, publisher: dict) -> dict:
    """Build ONETOO submit payload. Adjust if OpenAPI differs."""
    # Common-sense mapping
    payload = {
        "title": entry.get("title"),
        "url": entry.get("url"),
        "description": entry.get("notes") or "",
        "categories": [entry.get("category")] if entry.get("category") else [],
        "tags": entry.get("tags", []),
        "publisher": publisher,
        "manifests": entry.get("manifests", {}),
        # Optional: link back to HGPEdu
        "source": {
            "type": "hgpedu-portal",
            "portal_index": "https://www.hgpedu.eu/data/portal/index.json",
            "submitted_utc": utc_now(),
        },
    }
    # Remove empty fields for cleaner payloads
    payload = {k:v for k,v in payload.items() if v not in (None, "", [], {}, ())}
    return payload

def post_json(url: str, data: dict, token: str | None, timeout: int = 20) -> tuple[int, dict | str]:
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    if token:
        # Token style can differ. Change header if needed.
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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", default=os.environ.get("ONETOO_SUBMIT_ENDPOINT", DEFAULT_ENDPOINT))
    ap.add_argument("--token", default=os.environ.get("ONETOO_TOKEN"))
    ap.add_argument("--portal-index", default="data/portal/index.json")
    ap.add_argument("--state", default="portal/submissions.json")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    portal = load_json(Path(args.portal_index), {})
    entries = portal.get("entries", [])
    if not isinstance(entries, list):
        print("data/portal/index.json entries must be an array", file=sys.stderr)
        return 2

    state = load_json(Path(args.state), {"schema_version":"hgpedu.onetoo.submissions.v1","generated_utc":utc_now(),"items":{}})
    items = state.get("items", {})
    if not isinstance(items, dict):
        items = {}

    publisher = {
        "name": "HGPEdu",
        "domain": "hgpedu.eu",
        "homepage": "https://www.hgpedu.eu",
        "tfws": {
            "v2": "https://www.hgpedu.eu/.well-known/tfws.json"
        }
    }

    submitted = 0
    for entry in entries:
        url = str(entry.get("url","")).strip()
        if not url or not is_https(url):
            continue
        if url in items and items[url].get("status") in ("submitted","accepted"):
            continue

        payload = build_payload(entry, publisher)

        if args.dry_run:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            items[url] = {"status":"dry-run","last_attempt_utc":utc_now()}
            submitted += 1
            if submitted >= args.limit:
                break
            continue

        code, resp = post_json(args.endpoint, payload, args.token)
        rec = {
            "status": "submitted" if 200 <= code < 300 else "error",
            "http": code,
            "last_attempt_utc": utc_now(),
            "response": resp,
        }
        items[url] = rec
        print(f"{url} -> HTTP {code}")
        submitted += 1
        time.sleep(1.0)
        if submitted >= args.limit:
            break

    state["generated_utc"] = utc_now()
    state["items"] = items
    save_json(Path(args.state), state)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
