# Measurement Handbook (safe, practical)

This handbook describes *measurement logic* and *analysis protocol* without hazardous construction.

## Core principles
- Pre-register endpoints and analysis.
- Blind and randomize ON/OFF schedule.
- Log confounders (temperature, humidity, EMI, supply rails).
- Use PSD / Allan deviation to diagnose drift and 1/f noise.
- Use Monte Carlo and permutation tests to estimate false positives.

## Minimal run record
timestamp_utc, run_id, blinded_state, sensor_A_raw, sensor_B_raw,
temperature_C, humidity_pct, supply_V, ground_topology, notes, anomalies_flag

## Stop conditions
If any occurs, label run invalid:
- sensor saturation,
- undocumented wiring/topology changes,
- missing metadata,
- major EMI event without logging,
- post-hoc thresholding not pre-registered.
