# HGPEdu Portal Autopilot – reálne funkčné zapojenie (GitHub Actions)

Tento repozitár je statický portál. „Autopilot“ znamená automatizované **schvaľovanie príspevkov** cez GitHub Issues
a následné publikovanie do statického feedu, ktorý sa zobrazuje na:

- `https://hgpedu.eu/pages/portal.html` (front-end)
- `data/portal/index.json` (statický feed)

## 1) Workflow dnes (plne funkčné)

1. Niekto vytvorí GitHub Issue s názvom začínajúcim na **`[PORTAL]`** (ideálne cez Issue template).
2. GitHub Actions spustí **Portal Autopilot**:
   - vytiahne JSON payload z Issue
   - striktne ho overí (HTTPS, povinné polia, limity)
   - zapíše audit log (`data/portal/entries.jsonl`)
   - publikuje do `data/portal/index.json`
   - zapíše rozhodnutie do `data/portal/decisions/<issue>.json`
3. Autopilot spraví commit + push do `main`.
4. Statický web (Pages/Cloudflare Pages) sa po novom commite obnoví.

## 2) TFWS verifikovateľné artefakty (sha256/minisign)

Repo už obsahuje:
- `.well-known/sha256.json`
- `.well-known/sha256.json.minisig`
- `.well-known/minisign.pub`

Autopilot workflow vie **automaticky** aktualizovať `.well-known/sha256.json`
a (ak nastavíš secrets) aj **podpísať** novú verziu.

### Nastav v GitHub Secrets:
- `MINISIGN_SECRET_KEY` – obsah súkromného kľúča (napr. súbor `minisign.key` ako text)
- `MINISIGN_PASSPHRASE` – passphrase kľúča (ak je nastavená)

Potom Autopilot po každom publish:
- prepočíta `.well-known/sha256.json`
- vytvorí/obnoví `.well-known/sha256.json.minisig`

> Bez týchto secrets bude portál stále fungovať, len sa podpis nebude automaticky obnovovať.

## 3) ONETOO integrácia (štandard 2026 – read-only)

V roku 2026 je verejný runtime `search.onetoo.eu` **GET-only** (napr. `/search/v1`) a
nezverejňuje verejný `POST /contrib/.../submit` endpoint.

Preto integrácia HGPEdu vyzerá takto:

1. Portál autopilot publikuje príspevky do `data/portal/index.json` (statický feed).
2. Aktualizuje integrity inventár (`.well-known/sha256.json`) a podpis (`.minisig`), ak máš secrets.
3. Vygeneruje sa ONETOO „candidate“ JSON payload (na zdieľanie s maintainerom).
4. ONETOO strana (kurátorsky/autopilot) zaradí záznam do accepted-set.

Praktický test ONETOO search runtime:

- `https://search.onetoo.eu/search/v1?q=hgpedu&limit=10`

> Ak ONETOO neskôr zverejní submit endpoint, dá sa doplniť voliteľný submit krok.


## 4) Lokálny test

Bez GitHub Actions si vieš otestovať validáciu takto:

```bash
export BODY='```json
{"type":"hgp.portal.submission","version":"2.0","date":"2026-01-10","title":"Claude (Anthropic)","url":"https://claude.ai","summary":"Constitutional AI assistant by Anthropic","categories":["AI","Assistant","Research"]}
```'
python tools/portal_autopilot.py --issue 9999
```

Potom skontroluj:
- `data/portal/index.json` (nový item)
- `data/portal/entries.jsonl` (audit)
- `data/portal/decisions/9999.json` (decision)

