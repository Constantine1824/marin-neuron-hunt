"""Run the L57 64k TopK SAE (sae_L57w64_final_s21000) on dense MLP activations, on CPU.

Forward pass follows sparsify's TopK SAE: pre = (x - b_dec) @ W_enc.T + b_enc, ReLU, keep the top k=32,
recon = z @ W_dec + b_dec. The encoder is processed in latent chunks so it fits in ~16 GB of RAM.

    python encode.py SAE_PATH ACTS.npy OUT.npz      # ACTS: (tokens, 27648) MLP activations, act = silu(gate) * up
"""
import sys, time, numpy as np
from sae_io import SAE

K, CHUNK = 32, 4096


def encode(sae, X):
    b_dec = sae.get('b_dec'); b_enc = sae.get('encoder.bias')
    Xc = (X - b_dec).astype(np.float32)
    n_lat = b_enc.shape[0]
    best_v = np.full((len(X), K), -np.inf, np.float32); best_i = np.zeros((len(X), K), np.int64)
    t0 = time.time()
    for s in range(0, n_lat, CHUNK):
        W = sae.get('encoder.weight', slice(s, s + CHUNK))
        pre = Xc @ W.T + b_enc[s:s + CHUNK]
        cat_v = np.concatenate([best_v, pre], 1)
        cat_i = np.concatenate([best_i, np.broadcast_to(np.arange(s, s + W.shape[0]), pre.shape)], 1)
        top = np.argpartition(-cat_v, K - 1, axis=1)[:, :K]
        best_v = np.take_along_axis(cat_v, top, 1); best_i = np.take_along_axis(cat_i, top, 1)
        print(f'  latents {s + W.shape[0]}/{n_lat}  {time.time() - t0:.0f}s', flush=True)
    best_v = np.maximum(best_v, 0)  # ReLU after top-k (same set: top-k of ReLU(pre))
    return best_i, best_v, b_dec


def decode(sae, idx, val, b_dec):
    used = np.unique(idx[val > 0])
    Wd = sae.get('W_dec', used)
    pos = np.searchsorted(used, idx)
    R = np.tile(b_dec, (len(idx), 1))
    for t in range(len(idx)):
        m = val[t] > 0
        R[t] += val[t, m] @ Wd[pos[t, m]]
    return R


if __name__ == '__main__':
    sae = SAE(sys.argv[1]); X = np.load(sys.argv[2]).astype(np.float32)
    idx, val, b_dec = encode(sae, X)
    R = decode(sae, idx, val, b_dec)
    np.savez_compressed(sys.argv[3], idx=idx.astype(np.int32), val=val.astype(np.float32), recon=R.astype(np.float16))
    print('saved', sys.argv[3])
