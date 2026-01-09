# Falsification Gates (G0–G5)

A staged gate system to prevent self-deception.

- **G0: Instrument sanity** — calibration traceability; no saturation; full metadata.
- **G1: Null equivalence** — device-absent vs device-present indistinguishable under blinding.
- **G2: Polarity & topology** — polarity flips, wiring swaps, ground topology changes do not explain effect.
- **G3: Environment controls** — temperature/humidity/EMI/vibration are measured and regressed out.
- **G4: Replication** — independent repeat, same protocol, comparable statistics.
- **G5: Energy accounting (optional later)** — strict accounting, control loads, known-source exclusion.

**Rule:** A claim cannot advance to the next gate until the previous gate is passed.
