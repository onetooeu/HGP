#!/usr/bin/env python3
"""HGPEdu Portal Autopilot (deterministic, TFWS-friendly)

- Extracts a JSON submission payload from a GitHub Issue body
- Validates + normalizes it against data/portal/schema.submission.json
- Writes an append-only audit log: data/portal/entries.jsonl
- Publishes into: data/portal/index.json (static feed consumed by /pages/portal.html)
- Writes a decision record: data/portal/decisions/<issue>.json

Designed to run inside GitHub Actions.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def _fail(msg: str, code: int = 2) -> None:
    print(f"[portal_autopilot] ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)

def extract_json(body: str) -> dict:
    """Supported formats:
    1) ```json { ... } ```
    2) Raw JSON somewhere in body (first {...} that parses)
    """
    body = body or ""
    m = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", body, re.IGNORECASE)
    if m:
        return json.loads(m.group(1))
    candidates = re.findall(r"(\{[\s\S]*?\})", body)
    for c in candidates:
        try:
            return json.loads(c)
        except Exception:
            continue
    _fail("No JSON payload found in issue body. Paste JSON inside ```json ...```.")

def load_schema(schema_path: Path) -> dict:
    return json.loads(schema_path.read_text(encoding="utf-8"))

def is_public_https_url(u: str) -> bool:
    try:
        p = urlparse(u.strip())
    except Exception:
        return False
    if p.scheme.lower() != "https":
        return False
    if not p.netloc:
        return False
    host = p.hostname or ""
    if host in {"localhost", "127.0.0.1", "::1"}:
        return False
    if re.match(r"^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[0-1])\.)", host):
        return False
    return True

def normalize(payload: dict, schema: dict) -> tuple[dict, list[str], list[str]]:
    required = set(schema.get("required", []))
    reasons_ok: list[str] = []
    reasons_fail: list[str] = []

    if not isinstance(payload, dict):
        reasons_fail.append("Payload must be a JSON object.")
        return payload, reasons_ok, reasons_fail

    missing = [k for k in required if k not in payload or payload.get(k) in (None, "", [])]
    if missing:
        reasons_fail.append(f"Missing required: {', '.join(missing)}")

    out: dict = {}
    out["type"] = str(payload.get("type", "hgp.portal.submission")).strip() or "hgp.portal.submission"
    out["version"] = str(payload.get("version", "2.0")).strip() or "2.0"
    out["date"] = str(payload.get("date") or utc_now_iso())
    out["title"] = str(payload.get("title", "")).strip()
    out["url"] = str(payload.get("url", "")).strip()
    out["summary"] = str(payload.get("summary", "")).strip()

    cats = payload.get("categories") or []
    if isinstance(cats, str):
        cats = [c.strip() for c in cats.split(",") if c.strip()]
    if not isinstance(cats, list):
        cats = []
    cats = [str(c).strip() for c in cats if str(c).strip()]
    cats = sorted(list(dict.fromkeys(cats)))[:12]
    out["categories"] = cats

    for k in ("author", "contact", "license"):
        v = payload.get(k)
        if v is None:
            continue
        out[k] = str(v).strip()

    safety = payload.get("safety")
    if safety is not None and not isinstance(safety, dict):
        reasons_fail.append("Field `safety` must be an object if present.")
    if isinstance(safety, dict):
        out["safety"] = safety

    if len(out["title"]) < 3:
        reasons_fail.append("title too short (min 3).")
    if len(out["title"]) > 120:
        reasons_fail.append("title too long (max 120).")
    if len(out["summary"]) > 600:
        reasons_fail.append("summary too long (max 600).")
    if not is_public_https_url(out["url"]):
        reasons_fail.append("url must be a public HTTPS URL (no localhost/private IP).")

    allow = {
        "AI","Assistant","Chat","Research","Physics","Education","Theory",
        "Engineering","Math","Materials","Electronics","Safety","Portal","TFWS","ONETOO"
    }
    if out["categories"]:
        unknown = [c for c in out["categories"] if c not in allow]
        if unknown:
            reasons_ok.append("Unknown categories kept (soft): " + ", ".join(unknown))

    if not reasons_fail:
        reasons_ok.append("Hard checks passed.")
    return out, reasons_ok, reasons_fail

def stable_id(title: str, url: str) -> str:
    h = hashlib.sha256((title.strip().lower()+"\n"+url.strip()).encode("utf-8")).hexdigest()
    return "hgp_" + h[:16]

def load_index(path: Path) -> dict:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if "items" not in obj or not isinstance(obj["items"], list):
        _fail(f"index.json missing items[] at {path}")
    return obj

def upsert_item(index_obj: dict, item: dict) -> tuple[dict, bool]:
    items = index_obj["items"]
    existing = next((x for x in items if x.get("id") == item["id"]), None)
    changed = False
    if existing:
        for k in ("title","url","summary","categories","author","contact","license","safety"):
            if k in item and item.get(k) != existing.get(k):
                existing[k] = item.get(k)
                changed = True
        existing["updated_utc"] = utc_now_iso()
        changed = True
    else:
        item["first_seen_utc"] = utc_now_iso()
        item["updated_utc"] = item["first_seen_utc"]
        items.insert(0, item)
        changed = True
    index_obj["items"] = items[:500]
    return index_obj, changed

def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue", required=True, help="Issue number (for decision log)")
    ap.add_argument("--body-env", default="BODY", help="Env var with issue body")
    ap.add_argument("--index", default="data/portal/index.json")
    ap.add_argument("--schema", default="data/portal/schema.submission.json")
    ap.add_argument("--log", default="data/portal/entries.jsonl")
    args = ap.parse_args()

    body = os.environ.get(args.body_env, "")
    issue = str(args.issue).strip()

    payload = extract_json(body)
    schema = load_schema(ROOT / args.schema)
    normalized, ok, fail = normalize(payload, schema)

    decision = {
        "type": "hgp.portal.decision",
        "version": "1.0",
        "decision_utc": utc_now_iso(),
        "issue": int(issue) if issue.isdigit() else issue,
        "result": "accepted" if not fail else "rejected",
        "reasons_ok": ok,
        "reasons_fail": fail,
        "payload": normalized if not fail else payload,
    }

    dec_path = ROOT / f"data/portal/decisions/{issue}.json"
    write_json(dec_path, decision)

    if fail:
        print(json.dumps(decision, ensure_ascii=False, indent=2))
        return 3

    entry = dict(normalized)
    entry["id"] = stable_id(entry["title"], entry["url"])
    entry["source"] = {"issue": int(issue) if issue.isdigit() else issue, "mode": "autopilot"}

    index_path = ROOT / args.index
    index_obj = load_index(index_path)
    index_obj["generated_utc"] = utc_now_iso()
    index_obj["generator"] = "tools/portal_autopilot.py"

    index_obj, changed = upsert_item(index_obj, entry)

    append_jsonl(ROOT / args.log, {"decision": decision, "entry": entry})

    if changed:
        write_json(index_path, index_obj)

    print(json.dumps(decision, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
