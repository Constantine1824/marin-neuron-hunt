"""Reconstruction diagnostics for the L57 64k SAE on dense samples.

    python diagnose.py ACTS.npy CODES.npz POLE_STATS.parquet NAME

Reports: overall FVU; FVU with the massive-activation neuron N3872 removed; how FVU spreads over neurons
(variance-weighted vs. per-neuron); and which latents fire densely.
"""
import sys, numpy as np, pandas as pd

X = np.load(sys.argv[1]).astype(np.float32)
c = np.load(sys.argv[2]); R = c['recon'].astype(np.float32); idx, val = c['idx'], c['val']
ps = pd.read_parquet(sys.argv[3], filters=[('layer', '=', 57)]).sort_values('neuron')
name = sys.argv[4]
std_atlas = ps['std'].to_numpy()
E = X - R
mu = X.mean(0)


def fvu(cols=slice(None)):
    return float((E[:, cols] ** 2).sum() / ((X[:, cols] - mu[cols]) ** 2).sum())


big = 3872
rest = np.ones(X.shape[1], bool); rest[big] = False
print(f'== {name}: {len(X)} tokens')
print(f'FVU (all neurons, variance-weighted): {fvu():.3f}')
print(f'FVU without N3872:                    {fvu(rest):.3f}')
print(f'share of total variance in N3872:     {((X[:, big] - mu[big]) ** 2).sum() / ((X - mu) ** 2).sum():.1%}')
print(f'FVU on N3872 alone:                   {fvu(np.arange(big, big + 1)):.3f}')
# per-neuron R^2: how well is a *typical* neuron reconstructed?
var_n = ((X - mu) ** 2).sum(0); err_n = (E ** 2).sum(0)
ok = var_n > 0
r2 = 1 - err_n[ok] / var_n[ok]
print(f'per-neuron R^2: median {np.median(r2):.3f}, 10th pct {np.percentile(r2, 10):.3f}, '
      f'fraction of neurons with R^2 < 0: {(r2 < 0).mean():.1%}')
# standardized error: each neuron in units of its atlas std (what a per-neuron-scaled SAE would optimize)
Z = E / std_atlas; Zx = (X - mu) / std_atlas
print(f'FVU in per-neuron standardized units: {float((Z ** 2).sum() / (Zx ** 2).sum()):.3f}')
# top-variance neurons vs the rest
order = np.argsort(-var_n)
for lo, hi in [(0, 10), (10, 100), (100, 1000), (1000, 27648)]:
    cols = order[lo:hi]
    print(f'  neurons ranked {lo + 1:>5}-{hi:<5} by variance: FVU {fvu(cols):.3f}')
# firing
fired = val > 0
lat, cnt = np.unique(idx[fired], return_counts=True)
f = cnt / len(X)
print(f'latents used: {len(lat)};  mean active per token {fired.sum(1).mean():.1f}')
top = np.argsort(-f)[:5]
print('densest latents (fire fraction):', ', '.join(f'{lat[i]}:{f[i]:.0%}' for i in top))
