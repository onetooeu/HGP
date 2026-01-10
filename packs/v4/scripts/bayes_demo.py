"""Bayes demo for ON/OFF effect vs confounds-only model.

Creates:
- out/bayes_demo_data.csv
- out/bayes_demo_summary.json
- out/bayes_demo_residuals.png

Synthetic data only (illustrative).
"""
from pathlib import Path
import json, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "out"
OUT.mkdir(exist_ok=True)

rng = np.random.default_rng(2026)
n = 6000
block = 200
sched = np.repeat(rng.integers(0,2,size=n//block), block)[:n]
t = np.arange(n)
temp = 20 + 0.0015*t + rng.normal(0, 0.05, n)
true_effect = 0.0
sensor = 0.7*(temp-20) + true_effect*sched + rng.normal(0, 1.0, n)

pd.DataFrame({"t": t, "sched": sched, "temp": temp, "sensor": sensor}).to_csv(OUT/"bayes_demo_data.csv", index=False)

def log_marginal_likelihood(y, X, b0, V0, a0, d0):
    y = y.reshape(-1,1)
    n, p = X.shape
    V0inv = np.linalg.inv(V0)
    XtX = X.T@X
    Vn = np.linalg.inv(V0inv + XtX)
    bn = Vn@(V0inv@b0.reshape(-1,1) + X.T@y)
    an = a0 + n/2
    term = (y.T@y).item() + (b0.reshape(1,-1)@V0inv@b0.reshape(-1,1)).item() - (bn.T@np.linalg.inv(Vn)@bn).item()
    dn = d0 + 0.5*term
    from math import lgamma, log, pi
    sign0, logdetV0 = np.linalg.slogdet(V0)
    signn, logdetVn = np.linalg.slogdet(Vn)
    return (-n/2)*log(2*pi) + 0.5*(logdetVn - logdetV0) + a0*log(d0) - an*log(dn) + lgamma(an) - lgamma(a0)

y = sensor
X0 = np.column_stack([np.ones(n), temp, t])
X1 = np.column_stack([np.ones(n), temp, t, sched])

b0_0 = np.zeros(X0.shape[1]); b0_1 = np.zeros(X1.shape[1])
V0_0 = np.eye(X0.shape[1])*1e6
V0_1 = np.eye(X1.shape[1])*1e6
a0 = 1.0; d0 = 1.0

ll0 = log_marginal_likelihood(y, X0, b0_0, V0_0, a0, d0)
ll1 = log_marginal_likelihood(y, X1, b0_1, V0_1, a0, d0)
logBF10 = ll1 - ll0
BF10 = math.exp(min(700, logBF10))

summary = {
    "M0": "sensor ~ 1 + temp + time",
    "M1": "sensor ~ 1 + temp + time + sched",
    "log_BF10": logBF10,
    "BF10": BF10,
    "note": "Synthetic demo only."
}
(OUT/"bayes_demo_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

beta0 = np.linalg.lstsq(X0, y, rcond=None)[0]
beta1 = np.linalg.lstsq(X1, y, rcond=None)[0]
res0 = y - X0@beta0
res1 = y - X1@beta1

plt.figure(figsize=(7.2,4.5))
plt.hist(res0, bins=60, alpha=0.7, label="Residuals M0")
plt.hist(res1, bins=60, alpha=0.7, label="Residuals M1")
plt.xlabel("Residual (arb.)")
plt.ylabel("Count")
plt.title("Bayes demo: residual distributions (OLS fit) — illustrative")
plt.legend()
plt.tight_layout()
plt.savefig(OUT/"bayes_demo_residuals.png", dpi=220)
plt.close()

print("Done.")
