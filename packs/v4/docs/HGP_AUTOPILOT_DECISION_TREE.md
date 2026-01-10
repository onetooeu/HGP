# HGP Autopilot Decision Tree (v4-mix)

This document defines a single **decision flow** (“autopilot”) for the mixed-claim HGP program across **K1–K4**.

**Core principle:** do not promote a claim to a higher rung unless lower rungs have survived falsification gates.

---

## Phase 0 — Entry requirements (G0)

**Input:** a recorded run (raw data + metadata).

### G0 checklist (must pass)
- calibration & saturation checks passed
- complete metadata logging (config + env references)
- data integrity preserved (hashes / immutable archive)

**If G0 FAIL:**  
→ stop interpretation → fix measurement/logging → re-run.

---

## Phase 1 — Bias control (G1)

### G1 tests (must pass)
- blind or randomized toggles (A/B)  
- null rig (dummy configuration)  
- pre-registered primary metric (if applicable)

**If G1 FAIL:**  
→ treat observed “effect” as **non-evidence** (E0/E1 only) → return to G0.

---

## Phase 2 — K3 (signature-first)

### Evaluate K3
- PSD shape change
- Allan deviation regime shift
- cross-correlation vs env references
- confound regression residual

**If K3 PASS:**  
→ proceed to Phase 3 (K4).

**If K3 FAIL:**  
→ run “Confound Hunt”:
- EMI/grounding matrix checks
- thermal stability checks
- sampling/aliasing checks  
→ return to G0/G1.

---

## Phase 3 — K4 (spatial/field coherence)

### Evaluate K4
- distance law / spatial map
- disentangle from EM references
- reposition test: active zone vs cabling
- shielding parity

**If K4 PASS:**  
→ proceed to Phase 4 (K2).

**If K4 FAIL:**  
- If effect follows **cables/EM**, classify as **H1/H2 candidate**  
→ return to G0 with improved reference instrumentation and cabling controls.

---

## Phase 4 — K2 (thrust/weight)

### Evaluate K2
- symmetry sign-flip under inversion
- thermal parity controls
- grounding/ES matrix
- vibration sensitivity

**If K2 PASS:**  
→ proceed to Phase 5 (K1).

**If K2 FAIL:**  
- If correlated with heat → convection/thermal confound  
- If correlated with grounding → electrostatics  
- If correlated with vibration → mechanics  
→ return to G0 with the dominant confound neutralized.

---

## Phase 5 — K1 (surplus power)

### Evaluate K1
- integrated net energy (E_net) with uncertainty
- storage audit (C/L/mechanical)
- measurement method parity (independent approach)
- calorimetry sanity trend

**If K1 PASS:**  
→ classify as **Candidate anomaly** (E5 pending replication)  
→ move to Phase 6 (replication).

**If K1 FAIL:**  
→ K1 claim rejected for this configuration; continue exploring K3/K4 as primary signals.

---

## Phase 6 — Replication (G4)

### Replication requirements
- different operator and/or location
- same pre-registered metrics and thresholds
- same G0–G1 discipline

**If replication PASS:**  
→ elevate claim strength; publish as “replication-grade candidate”.

**If replication FAIL:**  
→ demote to confound/locality; return to Phase 2–4 to isolate cause.

---

## Summary: The autopilot rule
> **Never** treat K1/K2 as credible unless K3 and/or K4 show robust, bias-controlled structure first.

