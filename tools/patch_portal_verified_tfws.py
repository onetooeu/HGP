#!/usr/bin/env python3
"""
Patch HGPEdu Portal (SK+EN) to support VERIFIED_TFWS badge in legend + status UI.

Idempotent by design:
- Adds VERIFIED_TFWS badge to the legend if missing
- Adds colors.verified_tfws if missing

Usage:
  python tools/patch_portal_verified_tfws.py pages/portal.html en/pages/portal.html
"""

from __future__ import annotations
import sys
from pathlib import Path

BADGE_HTML = '<span style="padding:2px 6px;border-radius:999px;background:#e6f0ff;border:1px solid #eee">VERIFIED_TFWS</span>'

def patch_legend(text: str) -> str:
    if "VERIFIED_TFWS" in text:
        return text
    marker = "Status:"
    idx = text.find(marker)
    if idx == -1:
        return text
    after = text[idx:]
    vpos = after.find(">VERIFIED</span>")
    if vpos == -1:
        return text
    span_start = after.rfind("<span", 0, vpos)
    if span_start == -1:
        return text
    insert_at = idx + span_start
    return text[:insert_at] + BADGE_HTML + "\n      " + text[insert_at:]

def patch_colors(text: str) -> str:
    if "verified_tfws" in text:
        return text
    needle = "const colors = {"
    idx = text.find(needle)
    if idx == -1:
        return text
    line_end = text.find("\n", idx)
    if line_end == -1:
        return text
    insertion = '      verified_tfws: "#e6f0ff",\n'
    return text[:line_end+1] + insertion + text[line_end+1:]

def patch_file(p: Path) -> bool:
    if not p.exists():
        return False
    orig = p.read_text(encoding="utf-8", errors="replace")
    text = orig
    text = patch_legend(text)
    text = patch_colors(text)
    if text != orig:
        p.write_text(text, encoding="utf-8")
        return True
    return False

def main(argv: list[str]) -> int:
    for a in argv[1:]:
        path = Path(a)
        changed = patch_file(path)
        print(f"{'PATCHED' if changed else 'OK':7} {path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
