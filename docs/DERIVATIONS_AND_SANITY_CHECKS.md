# Derivations & Sanity Checks

## 1) Landauer bound
Irreversible erasure of 1 bit at temperature \(T\) requires at least:
\[
E_{bit} \ge k_B T \ln 2
\]
For an erasure rate \(R\) (bits/s), the minimum power is:
\[
P_{min} \ge k_B T \ln 2 \cdot R
\]
Use this as a hard lower bound sanity check on any narrative involving net information erasure.

## 2) ON/OFF mean-difference estimator
Given blinded schedule \(s_i\in\{0,1\}\) and sensor \(x_i\):
\[
\hat{\delta} = \bar{x}_{on} - \bar{x}_{off}
\]
This estimator is vulnerable to drift and correlated noise unless properly randomized and modeled.

## 3) Drift + 1/f: why false positives happen
If \(x_i = a t_i + \epsilon_i\) and the schedule correlates with time blocks, \(\hat{\delta}\) can be non-zero without a true effect.
Hence: randomization, Allan deviation, regression on confounds, and permutation testing.

## 4) Bayesian model comparison (overview)
Compare M0 (confounds-only) vs M1 (confounds + sched). Compute:
\[
BF_{10} = \frac{p(data\mid M_1)}{p(data\mid M_0)}
\]
Then run prior sensitivity to ensure robustness.
