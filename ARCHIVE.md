# HGP — Archival & Preservation Notes

This document describes how to preserve HGP long-term.

## Recommended archival steps

### 1. GitHub
- Keep repository public and immutable after final tag
- Protect `main` branch (no force-push)

### 2. Static hosting (optional)
The site is fully static and can be hosted on:
- GitHub Pages
- Netlify
- Cloudflare Pages

Suggested setup:
- root = repository root
- build step = none

### 3. Offline snapshot
Create a ZIP snapshot of the repository:
```
HGP_repo_phoenix_final.zip
```

### 4. Internet Archive
Submit the deployed site URL to:
https://web.archive.org/

## Archival philosophy
HGP is designed to remain:
- readable without dependencies
- understandable without prior context
- useful even decades later

This is intentional.
