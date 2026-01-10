#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from urllib.parse import urlparse

ALLOWED_KEYS = {"title","url","category","notes","manifests","tags","contact"}

def die(msg: str, code: int = 2):
    print(msg, file=sys.stderr)
    sys.exit(code)

def is_https(u: str) -> bool:
    p = urlparse(u)
    return p.scheme == "https" and bool(p.netloc)

raw = sys.stdin.read()
try:
    obj = json.loads(raw)
except Exception as e:
    die(f"Invalid JSON: {e}")

if not isinstance(obj, dict):
    die("Payload must be a JSON object")

unknown = set(obj.keys()) - ALLOWED_KEYS
if unknown:
    die(f"Unknown keys: {sorted(unknown)}")

title = str(obj.get("title","")).strip()
url = str(obj.get("url","")).strip()
if not (3 <= len(title) <= 120):
    die("title length must be 3..120")
if not is_https(url):
    die("url must be valid https:// URL")

out = {"title": title, "url": url}

category = obj.get("category")
if category is not None:
    category = str(category).strip()
    if len(category) > 60: die("category too long (max 60)")
    if category: out["category"] = category

notes = obj.get("notes")
if notes is not None:
    notes = str(notes).strip()
    if len(notes) > 500: die("notes too long (max 500)")
    if notes: out["notes"] = notes

tags = obj.get("tags")
if tags is not None:
    if not isinstance(tags, list): die("tags must be array")
    out["tags"] = [str(t).strip()[:40] for t in tags if str(t).strip()]

manifests = obj.get("manifests")
if manifests is not None:
    if not isinstance(manifests, dict): die("manifests must be object")
    for k,v in manifests.items():
        if not isinstance(k,str): die("manifest keys must be strings")
        if not isinstance(v,str) or not is_https(v): die(f"manifest {k} must be https:// URL")
    out["manifests"] = manifests

contact = obj.get("contact")
if contact is not None:
    out["contact"] = str(contact).strip()[:120]

print(json.dumps(out, ensure_ascii=False, indent=2))
