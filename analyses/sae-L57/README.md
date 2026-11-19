# The layer-57 64k SAE: what's wrong with it, and a better way to nominate neurons from it

Task: marin-sae-find-neurons. SAE: `alxcspr/stationhouse`, `sae-64k`, layer 57, checkpoint
`sae_L57w64_final_s21000` (TopK, k = 32, 65,536 latents, trained on the 27,648 MLP neuron activations,
act = silu(gate) * up). Everything here runs on CPU from cached atlas data. No new forward passes.

**Short version.** The five L57 neurons nominated from this SAE so far (N10940, N17606, N2462, N25368,
N5873) each rest on a latent that fired on 1 or 2 of 200,704 tokens, and three of their follow-up tests were
refuted. The SAE itself barely reconstructs typical neurons on fresh dense data. Its loss is dominated by
two huge neurons, because a label-parse bug meant it trained on raw activations rather than per-neuron
scaled ones. A stricter, weights-only nomination (a latent has to *read and write* the same neuron) still
finds real neurons. Its top dense-data check, L57-N8972, is an " at" neuron, explained in
`explanations/L57/L57-N8972.yaml` and tested by `requests/L57-N8972-001.yaml`.

## What's wrong

### 1. The published nominations rest on one or two tokens

The encoder-attribution pass (`nominate_enc/attribution_enc_L57.parquet`) ranks latents by how much
of |W_enc[j, i] · x_i| one neuron i takes, summed over the tokens where latent j fires, on 200,704 tokens.
The five nominated latents (1316→N10940, 42429→N17606, 6600→N2462, 23576→N25368, 33792→N5873) fired on
**1 to 2 tokens** each. On a token or two, one large input dominates by chance. Across all latents, a
high top-1 share mostly means "fired rarely and read a high-variance neuron": of the 40 latents with
top1_share ≥ 0.5, 75% have one of the 100 highest-variance neurons on top (median variance rank 1).
Their median firing count is 2.5 tokens.

### 2. Two neurons dominate the SAE

- **N3872 is a massive-activation neuron.** Atlas mean 104.7, std 26.7, positive on every token. It is
  the top input of 1,196 of the 8,000 tracked latents. The decoder bias doesn't absorb its offset
  (b_dec[3872] = 0.076), so latents spend capacity reconstructing it.
- **N13777 acts as a shared offset.** It has the second-highest variance (std 19.6). It is the largest
  std-scaled input for 3,429 of 4,487 active latents, with a negative weight in 88% of encoder rows
  (median about 3× the row's mean |w|).

Both follow from training on **raw** activations. A label-parse bug skipped the intended per-neuron
scaling, so the MSE loss is dominated by whichever few neurons have the largest raw variance.

### 3. On fresh dense data it barely reconstructs a typical neuron

`encode.py` runs the checkpoint on dense layer-57 activations. `diagnose.py` scores it.

| data | tokens | FVU | FVU without N3872 | median per-neuron R² | neurons with R² < 0 |
|---|---|---|---|---|---|
| `pilot/fineweb-1m/deep` | 6,141 | 0.949 | 0.997 | −0.023 | 92.7% |
| `probes/capybara-v1` | 3,455 | 0.967 | | | |

The reported validation FVU is 0.377 (0.315 in `stats.json`). By neuron variance rank (fineweb-1m deep),
FVU is 0.28 for ranks 1–10, 0.70 for 11–100, 0.96 for 101–1000 and **1.06 for the remaining 26,648**. In
other words, the SAE reconstructs the top ten neurons and does worse than predicting the mean for
almost every other neuron. Raw act is the input convention that fits best. Scaled act, `up` and
`gate_pre` all give FVU > 1.

I checked the CPU implementation against the SAE's own census, since a bug there would explain the
same numbers. My firing frequencies match `census.parquet` (Spearman ρ 0.72, same dense latents: 9090,
56872, 35686 and 18337, which fire on more than 90% of tokens here and about 62% in the census). They don't
match `census_uniform.parquet` (ρ −0.02). That file is internally inconsistent anyway: max_act 26,
top-100 share 28.4, FVU 1.60.

### 4. Training was short and erratic

The run trained on 21.5M tokens. Training FVU fell to 0.138 at step 7,600, spiked to 0.76 at step 12,000
and ended at 0.317. Only 24% of latents are alive (fire_frac ≥ 1e-4 in the census: 4,487 of
65,536). There's no aux-k loss for dead latents and no input normalization or centering.

### 5. Latents aren't neuron-aligned, so "top neuron" is a weak signal

The median cosine between a latent's encoder and decoder rows is 0.134. Even for the best latents, the
top neuron holds only about 0.05% of the encoder row's L1 mass, and its weight is at most 2.4× the second
neuron's. A latent is a direction over many neurons, and naming one neuron for it is only a nomination.

## Fixes

For **training** the next L57 SAE:

1. **Scale each neuron** by its atlas std (the intended convention; fix the label parse), or standardize
   the inputs. This alone should stop N3872 and N13777 from dominating the loss.
2. **Center the inputs** (subtract the atlas mean, or initialize b_dec to it), and consider dropping or
   separately modelling massive-activation neurons such as N3872.
3. **Add an aux-k loss** (or resample dead latents) and train longer than 21.5M tokens, with a lower or
   decayed learning rate around the step-12,000 spike.
4. **Validate on a uniform split** of the corpus and on the dense tiers. Report median per-neuron R² and
   FVU by variance band, not only overall FVU, which the top ten neurons can carry.

For **nominating neurons** from any SAE (`nominate_fixed.py`):

1. Use only latents that fire on at least 1e-4 of census tokens, so no nomination rests on 1–2 tokens.
2. Nominate neuron i from latent j only when i is **both** j's largest encoder weight and its largest
   decoder weight, so the latent reads and writes it. Mask N3872 and N13777 first. (Dividing the decoder
   by neuron std doesn't work: it rewards near-silent neurons.)
3. Treat that as a nomination and **check it on dense data** (`check_candidate.py`): the latent's
   activation should track the neuron across tokens.

Result: 724 of the 4,487 live latents (16%) have the same top neuron on both sides, against a chance rate
of about 0.004%. So the SAE does carry neuron-level structure, but it's buried under the problems above.

## The candidate it found: L57-N8972

Latents 14972, 29083 and 49374 each have N8972 as their top encoder and top decoder neuron. On 9,596
dense tokens (fineweb-1m deep and the capybara probe), ten latents correlate +0.70 to +0.85 with it.
When those latents fire the neuron averages +16 to +40; otherwise −0.17. That looks like the SAE splitting
one neuron's job into several latents.

```
python check_candidate.py 8972 act_L57.npy codes_web.npz probe_act_L57.npy codes_probe.npz
```

N8972+ fires on the token " at". On the dense web sample, none of the 6,125 non-"at" tokens exceeds its
pos_q99 (21.3). The top atlas exemplars are idioms: at present, at last, at the same time, at all times.
The full explanation is in `explanations/L57/L57-N8972.yaml`. `requests/L57-N8972-001.yaml` tests whether
the neuron is specific to " at" or fires on any preposition before a place (" at" vs " in"/" on" in
otherwise identical sentences).

A backup candidate, not taken further here: latent 17545 correlates −0.92 with N17889 (pos_q99 2.81,
neg_q99 25.03).

## Files

| file | what it does |
|---|---|
| `sae_io.py` | reads safetensors tensors by row, with bf16, via memmap (no torch) |
| `encode.py` | CPU forward pass of the TopK SAE in latent chunks; saves top-32 codes and reconstructions |
| `diagnose.py` | FVU, FVU without N3872, per-neuron R², FVU by variance band, dense latents |
| `nominate_fixed.py` | weights-only read-and-write nomination from live latents |
| `check_candidate.py` | does a nominated neuron track its latents on dense data? |

Data: `Station-house/marin-32b-neuron-atlas` (`pilot/fineweb-1m/deep` site=gate_pre and up for layer 57,
giving act = silu(gate_pre) * up; `probes/capybara-v1`; `pilot/fineweb-10m-sparse/summaries/pole_stats.parquet`).
SAE files from `alxcspr/stationhouse` (sha256 of the checkpoint `cc63369e…`).
