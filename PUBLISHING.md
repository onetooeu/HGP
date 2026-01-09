# Publishing Protocol (Final Boss)

This repository is designed as a **static, verifiable publisher site** compatible with the ONETOO / TFWS v2 trust-first model.

## Canonical target
- Site: `https://hgpedu.eu`
- ONETOO trust root: `https://www.onetoo.eu`

## Recommended release flow
1. Edit content (HTML/MD/assets).
2. Generate integrity inventory:
   - `python tools/generate_sha256_manifest.py --root . --out .well-known/sha256.json`
3. Sign the inventory:
   - `MINISIGN_SECRET=./minisign.key bash tools/sign_minisign.sh`
4. Verify the signature:
   - `bash tools/verify_minisign.sh`
5. Commit, tag, push, deploy.

## ONETOO / AI Search onboarding
Generate a submission payload:
- `python tools/generate_onetoo_submit_payload.py --base-url https://hgpedu.eu > submit.json`

Then submit per your ONETOO AI Search contribution workflow.
