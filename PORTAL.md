# HGP Portal 2.0 (static, TFWS-style)

This portal is intentionally **static** (no backend). Submissions are accepted via GitHub Issues / Pull Requests.

- Submit: `/pages/portal.html` (SK) and `/en/pages/portal.html` (EN)
- Feed index: `/data/portal/index.json`
- Submission schema: `/data/portal/schema.submission.json`

## Workflow

1. User fills the form → JSON payload.
2. User opens a GitHub Issue (pre-filled) or creates a PR adding a file into `/data/portal/submissions/`.
3. Maintainers review, then add the accepted record into `/data/portal/index.json`.
4. Site updates automatically after merge.

## Safety

Do not accept posts that contain:
- build instructions (step-by-step),
- high-voltage schematics or operational parameters,
- weaponization / harmful guidance.

Publish: theory, measurement methodology, results, data, citations, and falsifiable claims.

Updated: 2026-01-10T09:28:29Z
