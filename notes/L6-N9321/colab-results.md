# L6-N9321: Colab results (T4)

The prompts were measured on a Colab T4 with `scripts/colab/measure.py` (branch `colab-tools`). It loads only
layers 0–6 of `marin-32b-base@f19b3466` in bf16 and reads `silu(gate)·up` at the target, using
`runner/prompts.py`'s tokenizer and target rules. These notes are reading material and will be removed before
the PR is marked ready.

**Check against the atlas:** ten exemplars (ranks 0/1/2/10/25 on each side), fed as the atlas's exact token ids,
reproduce the stored activations. Seven match exactly and the largest gap is 0.06.

Thresholds: + q99 0.074, q999 0.229, q9999 0.835; − q99 0.080, q999 0.269, q9999 0.982.

## Round 1: broad probes

| group | n | mean | range | read |
|---|---|---|---|---|
| ways of saying "every" (each, on Saturdays, every other, once a week on, weekly on, most Fridays, taco Tuesday) | 11 | −1.92 | −3.39 … −0.90 | all past q9999 except 2 |
| repetition implied by context only ("airs Thursday nights", "New episodes drop on Fridays") | 7 | −0.76 | −1.45 … −0.16 | all negative, weaker |
| one-off weekday ("born on a Thursday", "Christmas fell on a Sunday") | 6 | +0.99 | +0.08 … +3.36 | all positive |
| **other periods, one-off** (last month, this morning, last year …) | 7 | +0.01 | −0.08 … +0.14 | **about zero** |
| **other periods, every** (every month, every morning …) | 7 | +0.00 | −0.10 … +0.07 | **about zero** |
| names (The Weeknd, girl Friday, Shark Week, Black Friday) | 10 | −0.02 | −0.27 … +0.35 | about zero |
| past habit ("we played poker every Friday night") | 4 | −1.50 | −2.50 … −0.49 | negative: the cue is repetition, not schedule register |
| "This week …" after a weekly column or podcast opener | 3 | −1.59 | | |
| "This week …" after a one-off story | 3 | +0.58 | | the type of text flips it |
| rates ("twice per week", "40 hours a week") | 4 | +0.57 | +0.27 … +1.23 | positive, unexpectedly |
| random sentences | 5 | 0.00 | | |

## Round 2: surprises

- **"last + weekday" reads negative** ("met the neighbours last Tuesday" −1.61). Round 3 shows this isn't about
  "last": "on Tuesday", "that Tuesday" and "this past Tuesday" in the same sentence read −0.34 to −0.54.
  Weekday names in plain past-tense narration lean slightly negative. The positive side on weekday names needs
  calendar placement ("born on Tuesday, March 3" +1.41, "fell on a Sunday" +3.36).
- **One located "week" is strongly positive:** "Christmas week" +2.64, "That week changed my life" +1.17, "the
  whole week of the wedding" +1.11.
- **"week" as a unit is mixed and small:** "a week ago" +0.29, "for a week" +0.49, "once a week" −0.23, "every
  week on food" −0.40.
- **Schedule format alone doesn't do it:** "Bin collection day: Thursday" +0.59 and "Tuesday to Sunday, 10am to
  6pm" −0.06. A repetition cue in the text does it.
- **Named weekly customs vs named one-off days:** Meatless Monday, Throwback Thursday, casual Friday and
  Tight-wad Tuesday read −0.76 to −0.94. Bloody Sunday, Black Tuesday and Ash Wednesday read −0.30 to +0.34.

## Round 3: the request files, as they would score

| request | type | question | result |
|---|---|---|---|
| `-001` | A, − | fresh repeating slots vs the same words for one occasion | should-fire 12/12 past −q99, should-not-fire 9/10 quiet: **pass** |
| `-002` | A, + | fresh one located occasion vs the same words repeating | 12/12, 8/10: **pass, at the edge**. Misses: "It snows every week here in January" +0.57, "Pilgrims arrive each week by bus" +1.55 |
| `-003` | D, − | exemplars with every/each/weekly swapped for this/one/special | 12/12 pairs in the predicted direction, mean difference 1.49 (0.04 needed): **pass** |
| `-004` | D, − | same second sentence after a weekly-series opener vs a one-off opener | 12/12, mean difference 2.04: **pass** |
| `-005` | A, − | "every week/Sunday" vs "every morning/month/year" in the same sentence | 10/10, 9/10 (other periods −0.10 … +0.06): **pass** |
| `-006` | A, − | named weekly customs vs named one-off days and names | 9/10 (Motivation Monday +0.02), 10/10: **pass** |
| `-007` | A, − | `-001`'s should-fire vs random sentences | 12/12, 10/10 (random within ±0.03): **pass** |
| `-008` | A, + | `-002`'s should-fire vs random sentences | 12/12, 10/10: **pass** |

## What's still open

- **Frequencies that read positive.** "Pilgrims arrive each week by bus" (+1.55), "It snows every week here in
  January" (+0.57) and "twice per week" (+1.23) read positive, while "Every week, I find a fox" reads −1.12. My
  guess is that a frequency describing how often a whole population or a weather pattern does something reads
  as a rate, not as one person's slot. It's untested.
- **Weekday names in plain past narration** lean slightly negative (−0.3 to −0.7) with no repetition cue. That
  would be a third behaviour, small but consistent.
