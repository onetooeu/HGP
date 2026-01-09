#!/usr/bin/env python3
"""
Deterministic SHA-256 inventory generator for TFWS/ONETOO-style static sites.

- Walks repository tree
- Excludes .git, node_modules, venv, build artifacts by default
- Produces: .well-known/sha256.json

Usage:
  python tools/generate_sha256_manifest.py --root . --out .well-known/sha256.json
"""
from __future__ import annotations
import argparse, hashlib, json, os
from pathlib import Path

EXCLUDE_DIRS = {".git", ".github", "node_modules", ".venv", "venv", "dist", "build", "__pycache__"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db"}

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def should_skip(p: Path, root: Path) -> bool:
    rel_parts = p.relative_to(root).parts
    for part in rel_parts[:-1]:
        if part in EXCLUDE_DIRS:
            return True
    if p.name in EXCLUDE_FILES:
        return True
    if p.suffix in {".pyc", ".pyo", ".pyd"}:
        return True
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Root directory")
    ap.add_argument("--out", default=".well-known/sha256.json", help="Output JSON path")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    out = Path(args.out)
    entries = []

    for p in sorted(root.rglob("*")):
        if p.is_dir():
            continue
        if should_skip(p, root):
            continue
        rel = p.relative_to(root).as_posix()
        entries.append({
            "path": rel,
            "sha256": sha256_file(p),
            "bytes": p.stat().st_size
        })

    doc = {
        "schema_version": "onetoo.integrity.sha256.v1",
        "generated_utc": __import__("datetime").datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "root": root.name,
        "count": len(entries),
        "files": entries
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
