# HGP Confound Atlas v4-mix (Signature Library)

Purpose: map the **most common confounds** to their typical fingerprints in:

- PSD / spectrum
- Allan deviation regimes
- cross-correlation with environmental references
- fast “kill tests” that can falsify the confound

This atlas is designed to stop false positives before they become narratives.

---

## Confound classes (high-level)

### C1 — Thermal drift & convection
- **Mechanism:** temperature gradients → sensor drift; convection → apparent thrust/weight artifacts.
- **PSD:** strong low-frequency power; drift-like; often no sharp lines.
- **Allan:** random-walk-like increase at long τ.
- **Correlates with:** temperature probes; airflow; duty cycle heating.
- **Kill test:** reproduce same heat flux with a different method and see if the effect follows heat.

### C2 — EMI pickup / ground loops
- **Mechanism:** loops + impedance → induced voltages/currents; common-mode coupling.
- **PSD:** mains harmonics (50/60 Hz + multiples), switching peaks.
- **Allan:** can look “structured” but collapses when grounding changes.
- **Correlates with:** EM reference sensors; cable routing.
- **Kill test:** grounding matrix + reroute cables; if effect follows cables, it’s EMI.

### C3 — Aliasing / sampling jitter / DSP artefacts
- **Mechanism:** sampling clock instability; spectral leakage; filtering.
- **PSD:** mirrored components; suspiciously stable narrow peaks tied to sampling.
- **Allan:** irregular slopes that change with sampling rate.
- **Correlates with:** acquisition settings more than physics.
- **Kill test:** repeat with different sampling rate / anti-alias settings; true physics should persist.

### C4 — Electrostatics (ES) & triboelectric effects
- **Mechanism:** charging of insulators; cable motion generating charge.
- **PSD:** can appear as low-frequency drift + bursts.
- **Allan:** bursty behaviour; large outliers.
- **Correlates with:** humidity; grounding; touch/motion.
- **Kill test:** controlled grounding/isolation matrix; add humidity control; if sign flips with grounding, it’s ES.

### C5 — Mechanical vibration & resonance
- **Mechanism:** micro-vibrations couple to scales/sensors; resonance amplifies.
- **PSD:** narrow peaks at mechanical resonance bands; often stable.
- **Allan:** may show plateau then spikes.
- **Correlates with:** vibration reference channels; building/nearby motion.
- **Kill test:** inject known vibration; if effect tracks vib amplitude, it’s mechanical.

### C6 — Magnetic coupling & magnetostriction
- **Mechanism:** magnets interact with nearby ferromagnets; magnetostrictive deformation.
- **PSD:** depends on drive frequency; can produce strong coherent lines.
- **Allan:** stable but configuration-sensitive.
- **Correlates with:** magnetometer readings; nearby metals.
- **Kill test:** move ferromagnetic objects; apply shielding; measure with magnetometers.

---

## “Red flag” checklist (quick triage)

If any item is true, **pause interpretation**:

- effect changes drastically when **only cable routing** changes  
- effect disappears when **grounding** changes  
- effect is dominated by **mains harmonics**  
- effect correlates strongly with **temperature** (especially long τ)  
- effect vanishes with different **sampling rate**  
- “thrust” follows heat or airflow

---

## How to use the atlas

1) Identify the dominant fingerprint in PSD/Allan/correlation.  
2) Run the corresponding kill test.  
3) If the confound survives, classify the observation as **H1/H2** and stop escalation.

