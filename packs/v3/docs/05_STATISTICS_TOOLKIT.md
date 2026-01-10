# Statistics Toolkit (quick recipes)

## Effect size
- Mean difference ON vs OFF (with confidence interval)
- Robust alternatives: median difference, trimmed mean

## Permutation test
Randomly permute ON/OFF labels to obtain p-value without parametric assumptions.

## Drift-aware modeling
- regress sensor on confound proxies (temperature, humidity, time)
- analyze residuals
- confirm effect persists after removing confounds

## Multiple comparisons
If testing many sensors/bands, control false discovery:
- Bonferroni (conservative)
- Benjamini-Hochberg (FDR)

## Replication
One p-value is not enough. Require:
- consistent direction,
- comparable effect size,
- independent run.
