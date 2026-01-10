# HGP Pre-registration Template (v4-mix)

Use this template **before** running an experiment. The goal is to minimize p-hacking and narrative drift.

---

## 1) Run metadata

- Run ID:
- Date/time:
- Operator:
- Location:
- Configuration name:
- A/B mapping definition:

---

## 2) Primary hypothesis (choose ONE)

- [ ] K3 signature (PSD/Allan/correlation)
- [ ] K4 local field coherence
- [ ] K2 thrust/weight
- [ ] K1 surplus power

**Primary statement (one sentence):**  
> ...

---

## 3) Primary metric (define exactly)

- Metric name:
- Calculation method / script:
- Window length:
- Band / frequency range (if applicable):
- Expected direction (+/-):
- PASS threshold:
- FAIL threshold:

---

## 4) Secondary metrics (optional)

List up to 3 secondary metrics. These cannot overrule the primary.

---

## 5) Confound references to log (mandatory)

- Temperature:
- Humidity:
- Vibration:
- EM reference channels:
- Power state / duty cycle:

---

## 6) Null tests & controls planned

- Null rig used? (Y/N)
- Randomized toggles? (Y/N)
- Grounding matrix? (Y/N)
- Thermal parity control? (Y/N)
- Sampling-rate parity? (Y/N)

---

## 7) Data exclusion & outliers policy

- Allowed exclusions:
- Outlier rule:
- Max percent excluded:

---

## 8) Decision rule (verdict)

- If PASS → next phase is:
- If FAIL → return to gate:
- If ambiguous → default action:

---

## 9) Integrity

- Raw data hash:
- Metadata hash:
- Storage location:

