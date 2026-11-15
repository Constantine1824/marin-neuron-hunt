# L10-N18895: Colab results (T4)

The prompts were measured on a Colab T4 with `scripts/colab/measure.py` (branch `colab-tools`). It loads only
layers 0–10 of `marin-32b-base@f19b3466` in bf16 (11.2 GiB) and reads `silu(gate)·up` at the target, using
`runner/prompts.py`'s tokenizer and target rules. These notes are reading material and will be removed before
the PR is marked ready.

**Check against the atlas:** ten exemplars (ranks 0/1/2/10/25 on each side), fed as the atlas's exact token ids,
reproduce the stored activations within 0.04.

Thresholds: + q99 0.130, q999 0.372, q9999 0.982; − q99 0.130, q999 0.343, q9999 0.770.

## Round 1: broad probes

| group | n | mean | range | read |
|---|---|---|---|---|
| putting off with "until" (can wait, put off, postpone, hold off, delay) | 6 | +4.02 | +2.17 … +6.91 | all past q9999 |
| countdown with "until" (days left, a month to go, two more sleeps) | 6 | −2.77 | −3.19 … −2.19 | all past q9999 |
| putting off **without** "wait" or "save" (deferred, pushed back, held off) | 5 | +2.18 | +0.87 … +2.70 | the meaning, not the word |
| "wait" meaning postponement ("That question will have to wait") | 3 | +5.18 | +4.66 … +5.56 | |
| "wait" meaning a person waits ("wait in line", "wait here") | 2 | +0.48 | +0.29, +0.67 | small |
| anticipation ("counting the days until", "how long until") | 3 | −1.75 | | negative |
| "I can't wait until Christmas" | 1 | +0.86 | | positive: the word "wait" wins over anticipation |
| plain end-time "until" (open until nine, lived in Paris until 1990) | 6 | −0.21 | −0.73 … +0.24 | near zero, leaning negative |
| both cues: "wait two more weeks until" / "decided to wait until" | 3 | | −0.73, +2.80, +5.94 | the phrase right before "until" wins |
| "for" putting off ("saved the cake for later") / other "for" | 3 / 3 | +1.52 / −0.30 | | |
| purpose "to get / to receive / to obtain" | 4 | −1.23 | −1.59 … −0.77 | the − side's second set of firings is real |
| plain "get" ("I always get tired", "the fridge doesn't get cold") | 4 | +0.48 | −0.26 … +1.32 | mixed |
| random | 6 | −0.01 | | |

## Round 2: the request files, as they would score

| request | type | question | result |
|---|---|---|---|
| `-001` | A, + | fresh putting-off sentences vs countdowns and plain end times | 12/12 (min +1.51), 10/10: **pass** |
| `-002` | A, − | fresh countdowns vs putting off and plain end times | 12/12 (max −1.74), 8/10: **pass, at the edge**. Misses: "The museum is open until six" −0.22, "He played the piano until his hands hurt" −0.29 |
| `-003` | D, + | putting-off verb swapped for a verb of carrying on, "until" fixed | 12/12 pairs, mean difference 3.85: **pass** |
| `-004` | D, − | countdown phrase swapped for a putting-off phrase | 11/12 pairs, mean difference 3.85: **pass**. Miss: "only one more delay until" stays −2.05 |
| `-005` | A, + (threshold q9999) | "wait" for a postponed task vs a person waiting | 10/10 (min +2.64), 9/10: **pass**. Miss: "Could you wait here a moment?" +1.98 |
| `-006` | A, − | purpose "to get / obtain / receive" vs the same verbs with no goal | 9/10, 9/10: **pass**. Misses: "Click here to obtain your certificate" −0.11, "I always get sleepy" −0.26 |
| `-007` | A, + | `-001`'s should-fire vs random sentences | 12/12, 10/10: **pass** |
| `-008` | A, − | `-002`'s should-fire vs random sentences | 12/12, 9/10 ("Please pass me the salt" −0.16): **pass** |

Side probes:

- **Amount plus "wait":** "three hours to wait until sunrise" −0.79 vs "three hours to go" −3.64, and "two weeks
  to wait until" −0.73 vs "two weeks left" −2.38. The remaining amount pulls negative, "wait" pulls positive,
  and the net is mildly negative.
- **Countdown with "to":** "Twelve weeks to a stronger back" −1.97, "Ten steps to a better garden" −1.38, "The
  road to recovery" −0.56. Plain "to" ("gave the book to", "moved to Boston") is about 0. The − side is about
  what is left before a target, not the word "until".
- **Anticipation alone isn't enough:** "I can't wait until the holidays" +0.86, "looking forward to" +0.07,
  "counting down to" −0.89.

## What's still open

- **Plain end-time "until" leans slightly negative** (−0.05 to −0.36, "walk on until you reach the church"
  −0.73). The more a sentence reads as moving toward an endpoint, the more negative it gets. That pulls `-002`
  to the edge.
- **"Could you wait here a moment?"** reads +1.98. A polite request to hold off may count as putting something
  off.
- **Plain "get" on the + side** ("the fridge doesn't get very cold" +1.32, "the roads get icy" +0.49) is
  unexplained.
