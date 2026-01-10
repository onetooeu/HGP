# HGP Scorecard v4-mix (K1–K4)

**Scope:** This scorecard operationalizes the mixed-claim HGP program across four measurement channels:

- **K1:** measurable electrical surplus power
- **K2:** measurable thrust / weight change
- **K3:** measurable change in sensor noise / spectrum (signature)
- **K4:** measurable perturbation of a local field in the vicinity (grav/inertial/other)

**Philosophy:** *falsification-first*. The goal is not to “prove” HGP, but to **eliminate self-deception** and **separate anomalies from artefacts**.

## Legend

- **PASS** → proceed to the next gate/channel
- **FAIL** → stop the claim and return to the indicated gate (or redesign measurement)
- **RED FLAG** → classic confound; investigate and neutralize before interpreting

---

## G0–G1: Global gates (required for every channel)

| Gate | What is checked | PASS threshold | FAIL / Stop | RED FLAG (confound) |
|---|---|---:|---|---|
| **G0 Instrument sanity** | basic calibration, saturation checks, reference signals | drift < **0.2σ** per analysis window *or* stable Allan regime | uncontrolled drift / clipping / saturation | ADC clipping, sensor thermal drift, floating ground |
| **G0 Metadata** | complete logging: time, config, env refs, power state | **100% coverage** | missing logs → run is not interpretable | manual edits, missing segments |
| **G1 Blind / random toggles** | A/B configuration toggles are randomized; operator unaware if possible | effect survives without operator knowledge | effect disappears under blind | expectation bias |
| **G1 Null rig** | dummy configuration (same wiring/power) without the “active zone” | signal **collapses** or drops strongly | signal remains | measurement system generates signal |

> **Rule:** No K1–K4 claim can be evaluated above **E1/E2** without passing G0–G1.

---

## K3: Sensor noise / spectrum signature

| Area | What is scored | PASS threshold | FAIL | RED FLAG |
|---|---|---:|---|---|
| PSD shape | *shape* change (not only amplitude) between A/B | consistent change in ≥ **70%** windows; same direction | isolated peaks only | mains harmonics, EMI pickup, aliasing |
| Allan deviation | slope regime change or stable knee shift | consistent slope/knee change across runs | only during drift periods | temperature-driven random-walk |
| Confound regression | effect after regression on T/RH/vib/EM refs | ≥ **50%** of effect remains | effect vanishes after regression | env variables are the driver |
| Symmetry test | polarity/orientation/topology flip | predicted sign/phase change | no change under flip | “cable as antenna” |

**K3 Minimum Viable Claim:**  
> A reproducible statistical signature survives **G0–G1** and survives regression on the dominant confounds.

---

## K4: Local field perturbation (vicinity)

| Area | What is scored | PASS threshold | FAIL | RED FLAG |
|---|---|---:|---|---|
| Spatial coherence | distance law or spatial map consistency | stable gradient/profile across segments | no geometry; random hotspots | EM near-field, nearby metals |
| EM disentanglement | separation from EM sensors | effect does **not** track EM 1:1 | tracks EM strongly | pickup via loops/grounding |
| Reposition test | move active zone vs move cables | effect follows **zone**, not cables | effect follows cables | cabling dominates |
| Shielding parity | EM shielding as a control | EM changes; “field” persists | everything changes together | it’s just EM |

**K4 Minimum Viable Claim:**  
> A spatially coherent effect is present and cannot be explained as EM pickup or simple mechanics.

---

## K2: Thrust / weight change

| Area | What is scored | PASS threshold | FAIL | RED FLAG |
|---|---|---:|---|---|
| Sign flip / symmetry | 180° inversion / polarity flip | predicted sign flip or nulling | no change | convection, electrostatics |
| Thermal parity | same heat with different method | thrust does **not** follow heat | thrust ~ heat | convection dominates |
| Grounding matrix | isolation/ground variations | effect stable | jumps with grounding | electrostatic forces |
| Vibration sensitivity | controlled vibration injection | effect stable | correlates with vib | mechanical resonance |

**K2 Minimum Viable Claim:**  
> A repeatable weight/thrust signal survives thermal, electrostatic and vibration controls and exhibits the expected symmetries.

---

## K1: Electrical surplus power (strictest)

| Area | What is scored | PASS threshold | FAIL | RED FLAG |
|---|---|---:|---|---|
| Integrated energy | time-integral of net power with uncertainty | **E_net > 5σ** and stable across windows | 1–2 windows only | RMS/phase artefacts, harmonics |
| Storage audit | inventory of C/L/mechanical storage | negligible or fully accounted | could be stored energy | capacitors, inductors, flywheels |
| Method parity | alternate measurement method agrees | within stated uncertainty | incompatible results | meter-specific illusion |
| Calorimetry sanity | thermal consequences match trend | at least coarse consistency | no plausible waste heat | “surplus without waste” |

**K1 Minimum Viable Claim:**  
> A statistically significant positive energy balance survives alternate measurement methods and storage audits.

---

## Evidence Ladder mapping (E0–E5)

- **E0**: observation only  
- **E1**: passed G0  
- **E2**: passed G1 (blind + null)  
- **E3**: K3 robust signature  
- **E4**: K4 spatial coherence **or** K2 symmetry-surviving thrust  
- **E5**: K1 ≥5σ + method parity + replication

---

## Recommended progression

1) **G0–G1** (always)  
2) **K3** (signature)  
3) **K4** (spatial/field coherence)  
4) **K2** (thrust/weight)  
5) **K1** (surplus power, last)

