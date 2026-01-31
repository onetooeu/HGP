# Mozart Mode (HGPEdu Portal) — final tuning checklist

Mozart mode means: **everything is technically correct, and also harmonized**:
navigation, wording, URLs, trust artifacts, and the ONETOO integration story
all “play together” without rough edges.

## 1) Canonical domain & URLs

- Canonical site: **https://hgpedu.eu** (no `www`)
- Pretty URLs are the default surface:
  - `/pages/research` (not `/pages/research.html`)
  - `/en/pages/research` (not `/en/pages/research.html`)
- If `.html` files exist (static hosting), keep them as **implementation detail**.
  - Redirect `.html → pretty` where possible (308).
  - Sitemap should list the **canonical pretty URLs**.

## 2) Trust surface must be easy to verify

Expose and keep stable:

- `/.well-known/tfws-v2.json`
- `/.well-known/sha256.json`
- `/.well-known/sha256.json.minisig`
- `/.well-known/minisign.pub`
- `/ai-trust-hub.json`

Make sure your documentation explains:

- how to verify `sha256.json.minisig` using the published `minisign.pub`
- why the inventory exists (auditability, reproducibility, long‑term trust)

## 3) Portal “Autopilot” story is one sentence

> Issue/PR → validate JSON → publish portal feed → update integrity → rebuild site

Everything else (logs, decisions, signatures) is a detail.

## 4) ONETOO Standard 2026 integration (read‑only public backend)

In 2026, **search.onetoo.eu exposes GET-only endpoints** (e.g. `/search/v1`).
There is no public `POST /contrib/.../submit` endpoint.

So the correct HGPEdu story is:

1. Publish a TFWS‑verifiable trust surface + portal feed.
2. Generate an ONETOO *candidate* JSON payload.
3. Notify ONETOO maintainers (issue / PR / curated lane).
4. When accepted, it becomes discoverable via ONETOO accepted-set and `/search/v1`.

## 5) “One voice” copy rules

- Short paragraphs, consistent terminology:
  - **Portal feed** (what you publish)
  - **Integrity inventory** (what you verify)
  - **Accepted-set** (what ONETOO searches)
- Avoid promises the runtime cannot keep (e.g., “automatic submit” if there is no submit endpoint).

## 6) Quick smoke test (curl)

```bash
# HGPEdu pages (all should be 200)
for u in   "https://hgpedu.eu/"   "https://hgpedu.eu/pages/portal"   "https://hgpedu.eu/pages/research"   "https://hgpedu.eu/.well-known/tfws-v2.json"   "https://hgpedu.eu/.well-known/sha256.json"   "https://hgpedu.eu/.well-known/minisign.pub"   "https://hgpedu.eu/sitemap.xml"   "https://hgpedu.eu/robots.txt"
do
  echo "$(curl -sSI "$u" | head -n1)  $u"
done

# ONETOO search (read-only)
curl -sS "https://search.onetoo.eu/search/v1?q=hgpedu&limit=10"
```

If this passes, the orchestra is in tune.
