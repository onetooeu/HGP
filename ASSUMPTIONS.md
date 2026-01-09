# HGP — Assumptions & Model Hygiene

**Date:** 2026-01-09

This file defines the **minimum quality bar** for equations, units, and simulations in HGP.

## A0 — Naming & terminology
Some terms used on the site are **non‑standard** or **speculative**.  
Whenever a non-standard term appears, it must have:

- a short definition,
- a mapping to standard physics language *or* an explicit note: **“non-standard term”**.

## A1 — Units are mandatory
Every equation must define:
- variables and their units,
- constants and their units,
- the domain where the equation is intended to apply.

**Energy vs Power**
- Energy: **J** (joules)
- Power: **W = J/s**
If you state “W” without a time context, you are stating **power**, not energy.

## A2 — Conservation checks
For any claimed “output”, the documentation must include:
- the assumed input sources (energy, entropy, information, temperature gradients, etc.),
- a note about conservation constraints and where the model could break.

## A3 — Simulations are toy models unless proven otherwise
All scripts in `/sim/` are treated as **toy models** unless:
- inputs correspond to measurable physical quantities,
- outputs are validated against data or established references,
- uncertainty and error propagation are included.

## A4 — Reproducibility checklist
A result is “reproducible” if:
- the script runs with pinned dependencies (or uses stdlib only),
- there is a command shown to reproduce plots/numbers,
- parameters are documented and versioned.

## A5 — Communication rules
Avoid framing that implies certainty where there is none:
- prefer **“hypothesis / concept / model”** over “technology / device / generator”
- prefer **“explores”** over “proves”
- avoid “infinite energy” type marketing language

---
If a section does not meet these requirements yet, mark it clearly as **DRAFT**.
