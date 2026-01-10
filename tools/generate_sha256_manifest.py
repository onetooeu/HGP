#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, datetime
from pathlib import Path

EXCLUDE_DIRS = {".git",".github","node_modules",".venv","venv","dist","build","__pycache__"}
EXCLUDE_FILES = {".DS_Store","Thumbs.db"}

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def should_skip(p: Path, root: Path) -> bool:
    rel = p.relative_to(root).parts
    for part in rel[:-1]:
        if part in EXCLUDE_DIRS:
            return True
    if p.name in EXCLUDE_FILES:
        return True
    if p.suffix in {".pyc",".pyo",".pyd"}:
        return True
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default=".well-known/sha256.json")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    out = Path(args.out)

    files = []
    for p in sorted(root.rglob("*")):
        if p.is_dir():
            continue
        if should_skip(p, root):
            continue
        rel = p.relative_to(root).as_posix()
        files.append({"path": rel, "sha256": sha256_file(p), "bytes": p.stat().st_size})

    doc = {
        "schema_version":"onetoo.integrity.sha256.v1",
        "generated_utc": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
        "root": root.name,
        "count": len(files),
        "files": files,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
