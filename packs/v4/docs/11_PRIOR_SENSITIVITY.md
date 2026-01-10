# Prior Sensitivity (Bayes Factor) — v4

Bayes factors depend on priors. This chapter adds a **sensitivity grid** over:
- beta prior variance (diagonal V0 scale)
- inverse-gamma scale parameter d0 (noise prior)

Outputs:
- `/out/bayes_sensitivity_grid_logBF10.csv` — grid of log BF10 values
- `/out/bayes_sensitivity_heatmap.png` — heatmap visualization
- `/out/bayes_sensitivity_curve_d0_1.csv` + `/out/bayes_sensitivity_curve.png` — 1D slice at d0=1

How to use:
1. Choose a reasonable prior family.
2. Compute BF10 across a range of hyperparameters.
3. Report the BF10 range (min/median/max) as part of robustness.

Rule of thumb:
- If the conclusion flips sign across plausible priors, the evidence is **not robust**.
