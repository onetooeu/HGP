#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, datetime
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--in", dest="inp", required=True)
ap.add_argument("--out", dest="out", default="portal/index.json")
args = ap.parse_args()

entries = {}
p = Path(args.inp)
if p.exists():
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        obj = json.loads(line)
        entries[obj["url"]] = obj

now = datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
out_entries = []
for url, obj in sorted(entries.items(), key=lambda kv: (kv[1].get("title","").lower(), kv[0])):
    o = dict(obj)
    o["updated_utc"] = now
    out_entries.append(o)

doc = {"schema_version":"hgpedu.portal.index.v1","generated_utc":now,"count":len(out_entries),"entries":out_entries}
Path(args.out).parent.mkdir(parents=True, exist_ok=True)
Path(args.out).write_text(json.dumps(doc, ensure_ascii=False, indent=2)+"
", encoding="utf-8")
