# ONETOO Standard 2026 — HGPEdu integration notes (EN)

This repo is aligned with the ONETOO 2026 runtime where `search.onetoo.eu` is **public GET-only**.

## Key idea

HGPEdu does not POST submissions to ONETOO. Instead it publishes **verifiable artifacts**
(TFWS + integrity + portal feed) and provides an ONETOO *candidate* JSON for maintainer curation.

## Public runtime endpoints

- OpenAPI: `https://search.onetoo.eu/openapi.json`
- Search: `https://search.onetoo.eu/search/v1?q=...&limit=...`

## Recommended workflow

1. Publish portal item → update integrity inventory/signature.
2. Generate candidate JSON payload.
3. Notify ONETOO maintainers (issue/PR) with links to TFWS/integrity.
4. After acceptance, it appears in the accepted-set and becomes searchable.

