# Bayesian Model Comparison (Deep Dive)

## Purpose
Bayesian model comparison helps answer: **Is the observed signal better explained by a confound-only model or by a model that includes an additional 'anomaly' term?**

## Recommended progression
1. Start with **M0** (null): confounds only (time drift, temperature, humidity, EMI proxies).
2. Add **M1**: include an ON/OFF (sched) term.
3. Add **M2**: include interaction terms (sched × time) only if pre-registered.
4. Compare using **Bayes factors** or model evidence.

## Bayes factor (BF10)
BF10 = p(data | M1) / p(data | M0)
- BF10 > 1 supports M1
- BF10 < 1 supports M0
Interpretation (rule-of-thumb):
- 1–3: weak
- 3–10: moderate
- 10–30: strong
- >30: very strong

## Sensitivity analysis (required)
Bayes factors depend on priors. Always:
- declare priors,
- vary reasonable prior widths,
- report BF10 range.

## Included demo
See:
- `/out/bayes_demo_data.csv`
- `/out/bayes_demo_summary.json`
- `/out/bayes_demo_residuals.png`

These are **synthetic** and meant to show workflow, not to claim an effect.

## Practical guidance
- Prefer simple models until evidence demands complexity.
- Confounds can easily masquerade as ON/OFF effects under drift and 1/f noise.
- Bayesian comparison pairs well with permutation tests and cross-validation.
