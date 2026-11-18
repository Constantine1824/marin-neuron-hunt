"""Re-nominate layer-57 neurons from the 64k SAE without the problems in the encoder-attribution pass.

Differences from nominate_enc (attribution_enc_L57.parquet):
  1. Only latents that fire on >= MIN_FIRE of tokens in the SAE's own census (census.parquet) are used,
     so a nomination never rests on 1-2 tokens.
  2. Weights only, no per-token attribution: a latent nominates neuron i when i is both its largest encoder
     weight |W_enc[j, i]| and its largest decoder weight |W_dec[j, i]|, i.e. the latent reads AND writes
     that neuron. (Scaling either side by the neuron's std was tried and does not work: dividing the decoder
     by std rewards near-silent neurons.)
  3. N3872 (massive activation, mean ~105) and N13777 (a shared offset read by most latents) are masked
     before taking the top neuron, since nearly every latent touches them.

    python nominate_fixed.py SAE_PATH CENSUS.parquet OUT.parquet

The result still needs checking on dense data (check_candidate.py): agreement in the weights is a
nomination, not evidence.
"""
import sys, numpy as np, pandas as pd
from sae_io import SAE

MIN_FIRE, MASK = 1e-4, [3872, 13777]

sae = SAE(sys.argv[1])
census = pd.read_parquet(sys.argv[2])
lat = np.sort(census[census.fire_frac >= MIN_FIRE].latent_id.to_numpy())
print(f'latents with fire_frac >= {MIN_FIRE}: {len(lat)} of {len(census)}')
rows = []
for s in range(0, len(lat), 2048):
    j = lat[s:s + 2048]
    E = np.abs(sae.get('encoder.weight', j)); E[:, MASK] = 0
    D = np.abs(sae.get('W_dec', j)); D[:, MASK] = 0
    for k, (e, d) in enumerate(zip(E, D)):
        oe = np.argsort(-e)[:2]; od = np.argsort(-d)[:2]
        rows.append(dict(latent=int(j[k]), enc_top=int(oe[0]), enc_ratio=float(e[oe[0]] / e[oe[1]]),
                         enc_share=float(e[oe[0]] / e.sum()), dec_top=int(od[0]),
                         dec_ratio=float(d[od[0]] / d[od[1]]), dec_share=float(d[od[0]] / d.sum()),
                         cos=float((e * d).sum() / np.sqrt((e ** 2).sum() * (d ** 2).sum()))))
    print(f'  {min(s + 2048, len(lat))}/{len(lat)}', flush=True)
r = pd.DataFrame(rows).merge(census[['latent_id', 'fire_frac', 'max_act']], left_on='latent', right_on='latent_id').drop(columns='latent_id')
r['agree'] = r.enc_top == r.dec_top
r['score'] = np.minimum(r.enc_ratio, r.dec_ratio)
r.to_parquet(sys.argv[3])
c = r[r.agree].sort_values('score', ascending=False)
print(f'\nlatents whose top encoder and decoder neuron agree: {len(c)} of {len(r)} ({r.agree.mean():.0%}; '
      f'chance ~{1 / 27646:.4%})')
print('neurons nominated by more than one latent:')
print(c.groupby('enc_top').latent.agg(['count', list]).sort_values('count', ascending=False).head(15).to_string())
print(c.head(25).round(3).to_string(index=False))
