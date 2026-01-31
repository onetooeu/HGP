#!/usr/bin/env python3
"""Regenerate .well-known/sha256.json (TFWS-style)

This script updates hashes for:
- every path already present in .well-known/sha256.json
- plus any extra paths provided via --include

It is *incremental* to keep file ordering stable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha256_file(p: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    n = 0
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
            n += len(chunk)
    return h.hexdigest(), n

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=".well-known/sha256.json")
    ap.add_argument("--include", action="append", default=[], help="extra paths to include")
    args = ap.parse_args()

    mpath = ROOT / args.manifest
    obj = json.loads(mpath.read_text(encoding="utf-8"))

    files = obj.get("files", [])
    if not isinstance(files, list):
        raise SystemExit("manifest.files must be an array")

    # existing
    seen = set()
    for rec in files:
        path = rec.get("path")
        if not path or not isinstance(path, str):
            continue
        seen.add(path)
        fp = ROOT / path
        if not fp.exists() or fp.is_dir():
            # keep record but mark missing
            rec["missing"] = True
            continue
        digest, n = sha256_file(fp)
        rec.pop("missing", None)
        rec["sha256"] = digest
        rec["bytes"] = n

    # extra include
    for p in args.include:
        p = p.strip()
        if not p or p in seen:
            continue
        fp = ROOT / p
        if not fp.exists() or fp.is_dir():
            continue
        digest, n = sha256_file(fp)
        files.append({"path": p, "sha256": digest, "bytes": n})
        seen.add(p)

    obj["generated_utc"] = utc_now()
    obj["count"] = len([r for r in files if not r.get("missing")])

    mpath.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
