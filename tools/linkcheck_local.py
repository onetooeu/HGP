#!/usr/bin/env python3
"""Local static link check (basic).
- ensures referenced local href/src exist
- ignores external http(s) links
"""
from __future__ import annotations
from pathlib import Path
import re, sys

ROOT = Path(".")
htmls = list(ROOT.rglob("*.html"))
bad = 0
for p in htmls:
    s = p.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r'''(?:href|src)=["']([^"']+)["']''', s):
        u = m.group(1).strip()
        if "${" in u:
            continue
        if not u or u.startswith("#") or u.startswith("mailto:") or u.startswith("http://") or u.startswith("https://"):
            continue
        # normalize
        u2 = u.split("?")[0].split("#")[0]
        if u2.startswith("/"):
            target = ROOT / u2.lstrip("/")
        else:
            target = (p.parent / u2).resolve()
            try:
                target = target.relative_to(ROOT.resolve())
                target = ROOT / target
            except Exception:
                pass
        if not target.exists():
            print(f"Missing: {p.as_posix()} -> {u}", file=sys.stderr)
            bad += 1

print(f"Checked {len(htmls)} html files. Missing refs: {bad}")
sys.exit(1 if bad else 0)
