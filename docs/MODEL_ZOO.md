# Model Zoo (Candidate Statistical Models)

Use these models as a structured progression; do not add complexity unless pre-registered.

## Base variables
- time index t
- confound proxies: temperature, humidity, EMI proxy, supply rails
- schedule variable: sched (0/1), ideally blinded

## M0 — Null / confounds only
sensor ~ 1 + confounds + time

## M1 — Add ON/OFF term
sensor ~ 1 + confounds + time + sched

## M2 — Add interaction (only if pre-registered)
sensor ~ 1 + confounds + time + sched + (sched × time)

## M3 — Multi-sensor / hierarchical
For multiple sensors, consider hierarchical priors or partial pooling (advanced).

## Evaluation
- permutation tests on sched labels
- Bayes factor BF10 for M1 vs M0
- cross-validated predictive accuracy as a sanity check
- prior sensitivity grid (v4)
