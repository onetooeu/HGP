#!/usr/bin/env python3
"""
Generate an ONETOO AI Search 'publisher submission' payload from local manifests.

Outputs JSON to stdout by default.

Usage:
  python tools/generate_onetoo_submit_payload.py --base-url https://hgpedu.eu > submit.json
"""
from __future__ import annotations
import argparse, json

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True, help="Canonical base URL of the deployed site (e.g., https://hgpedu.eu)")
    args = ap.parse_args()
    base = args.base_url.rstrip("/")

    payload = {
        "name": "HGP EDU – ONETOO Showroom",
        "url": base,
        "description": "Educational showroom and demonstrator for the ONETOO.eu ecosystem (TFWS v2, AI Search, Autopilot, integrity bundles).",
        "categories": ["Education", "AI", "Trust Infrastructure", "Research", "Standards"],
        "manifests": {
            "ai_trust_hub": base + "/.well-known/ai-trust-hub.json",
            "tfws_v2": base + "/.well-known/tfws-v2.json",
            "ai_governance": base + "/.well-known/ai-governance.json",
            "ai_search_publisher": base + "/.well-known/ai-search.publisher.json",
            "integrity_sha256": base + "/.well-known/sha256.json",
            "integrity_sig": base + "/.well-known/sha256.json.minisig",
            "minisign_pub": base + "/.well-known/minisign.pub",
            "onetoo_sync": base + "/.well-known/onetoo-sync.json"
        }
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
