# Contributing to HGP

HGP is an educational sandbox about **scientific hygiene**: assumptions, units, conservation laws, falsification, and responsible communication.

## What contributions are welcome
- New **case studies** for the Museum (with sources/links, your critique, and falsification ideas)
- Improvements to the **checklist**, **method pages**, or **educator pack**
- Better **toy simulations** (clearly labeled assumptions/simplifications/limitations)
- UI improvements (static, no backend required)

## What is NOT welcome
- Claims presented as real “free energy”, “over‑unity”, or “infinite power”
- Fundraising, investment pitch text, or marketing copy
- Misleading graphs without baseline, units, and explicit energy accounting

## Contribution rules (hard requirements)
1. Every equation must define variables + units.
2. Every model must state **energy source** and what decreases.
3. Every demo must include a **zero baseline** when appropriate.
4. Every speculative appendix must be labeled as **creative / science‑fantasy**.

## How to add a Museum case study
1. Copy `CASE_STUDY_TEMPLATE.md` → `case-studies/<slug>.md`
2. Add a short HTML page in `pages/museum/<slug>.html` (and EN mirror).
3. Link it from `pages/museum.html` and `en/pages/museum.html`.

## Code style
- Keep it static (HTML/CSS/JS)
- No trackers, no ads, no hidden scripts
- Prefer clarity over cleverness

Thank you for making the internet a little harder to fool.
