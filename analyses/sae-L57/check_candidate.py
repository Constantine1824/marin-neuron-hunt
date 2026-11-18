"""Check a nominated (latent, neuron) pair on dense activations: does the latent's activation track the neuron?

    python check_candidate.py NEURON ACTS.npy CODES.npz [ACTS2.npy CODES2.npz ...]

For every latent in the codes that fires on >= 20 tokens, prints the correlation between the latent's
activation (0 when it doesn't fire) and the neuron, plus the neuron's mean when the latent fires vs not.
CODES come from encode.py on the same ACTS.
"""
import sys, numpy as np

n = int(sys.argv[1])
x, Z = [], []
for a, c in zip(sys.argv[2::2], sys.argv[3::2]):
    X = np.load(a, mmap_mode='r'); x.append(np.asarray(X[:, n], np.float32))
    d = np.load(c); Z.append((d['idx'], d['val']))
x = np.concatenate(x)
idx = np.concatenate([i for i, _ in Z]); val = np.concatenate([v for _, v in Z])
lat, cnt = np.unique(idx[val > 0], return_counts=True)
out = []
for j in lat[cnt >= 20]:
    z = np.where(idx == j, val, 0).sum(1); on = z > 0
    out.append((np.corrcoef(z, x)[0, 1], j, on.sum(), x[on].mean(), x[~on].mean()))
print(f'N{n}: {len(x)} tokens, mean {x.mean():.2f}, std {x.std():.2f}')
print(' corr  latent  fired  neuron|fires  neuron|else')
for r, j, k, m1, m0 in sorted(out, key=lambda t: -abs(t[0]))[:10]:
    print(f'{r:+.3f}  {j:>6}  {k:>5}  {m1:>11.2f}  {m0:>11.2f}')
