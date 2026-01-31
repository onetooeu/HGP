# ONETOO Standard 2026 — HGPEdu integration notes

This repository is aligned with the **ONETOO 2026 runtime** where:

- **`search.onetoo.eu` is a public GET-only service**
- search runs over a curated, autopilot-managed **accepted-set**
- the public runtime does **not** expose a public `POST /contrib/.../submit` endpoint

## What this means for HGPEdu

HGPEdu does **not** “push” content into ONETOO by POST requests.

Instead, HGPEdu publishes a *verifiable trust surface* and a *portal feed*.
ONETOO maintainers/autopilot can then curate and include it in the accepted-set.

### Your published artifacts (HGPEdu)

- Portal feed: `/data/portal/index.json`
- Trust surface: `/.well-known/tfws-v2.json`
- Integrity inventory: `/.well-known/sha256.json` + `.minisig` + `minisign.pub`
- Trust hub: `/ai-trust-hub.json`

### ONETOO runtime (public)

- OpenAPI: `https://search.onetoo.eu/openapi.json`
- Search: `https://search.onetoo.eu/search/v1?q=...&limit=...`

## Recommended submission workflow

1. **Publish** HGPEdu portal item + update integrity inventory (GitHub Actions autopilot).
2. **Generate** an ONETOO candidate JSON payload (see `tools/generate_onetoo_submit_payload.py`).
3. **Notify ONETOO** maintainers:
   - open an issue / PR in the ONETOO registry repo
   - attach the generated JSON + links to TFWS/integrity
4. After curation, the domain/URL becomes part of ONETOO accepted-set and appears in `/search/v1`.

## FAQ

### Why no public submit endpoint?
Because ONETOO’s 2026 public runtime is designed to be **audit-first and abuse-resistant**.
Curation happens in the trust root pipeline; the public runtime stays deterministic and safe.

### Can this change in future?
Yes. If ONETOO publishes a public contrib endpoint again, HGPEdu can add an optional submit tool.
Until then, keep HGPEdu honest: publish artifacts, provide proofs, let ONETOO curate.

