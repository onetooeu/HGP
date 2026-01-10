#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, datetime

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True, help="Site canonical base URL, e.g. https://hgpedu.eu")
    ap.add_argument("--title", default="HGP Edu Portal (TFWS v2)")
    ap.add_argument("--description", default="TFWS v2 / ONETOO compatible educational portal with verifiable manifests and integrity inventory.")
    ap.add_argument("--categories", default="Education,Research,AI,Trust,TFWS,ONETOO")
    args = ap.parse_args()

    base = args.base_url.rstrip("/")
    payload = {
        "schema_version": "onetoo.contrib.submit.v2",
        "submitted_utc": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
        "entry": {
            "title": args.title,
            "url": base,
            "description": args.description,
            "categories": [c.strip() for c in args.categories.split(",") if c.strip()],
            "manifests": {
                "ai_trust_hub": base + "/.well-known/ai-trust-hub.json",
                "tfws_v2": base + "/.well-known/tfws-v2.json",
                "ai_search_publisher": base + "/.well-known/ai-search.publisher.json",
                "integrity_sha256": base + "/.well-known/sha256.json",
                "integrity_sig": base + "/.well-known/sha256.json.minisig",
                "minisign_pub": base + "/.well-known/minisign.pub"
            }
        }
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
