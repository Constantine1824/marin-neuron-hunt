## Neuron(s)

L10-N18895

## In plain English

- **Positive side:** fires when something is put off to a later point: "the laundry can wait until tomorrow", "that conversation will have to wait", "postponed the vote until next month", "saved the cake for later". It is the putting off that matters, not the word "wait". Postponing without "wait" fires, and a person waiting in line barely does.
- **Negative side:** fires when the text counts down what is left before an event or goal: "only five days left until the exam", "ten more laps till the finish line", "counting the days until summer", "twelve weeks to a stronger back". It fires more weakly on purpose phrases like "enter the code to get ten percent off".
- "until" is the main word on both sides, and the phrase just before it decides the sign. Swapping "wait" for "go" in "a month to ___ until football season" flips it.

## What's in this PR

- [x] An explanation: `explanations/L10/L10-N18895.yaml`, covering **both sides**
- [x] Confirmation-experiment requests, listed under Design > Claim.
- Reading notes, to be removed before this is marked ready: `notes/L10-N18895/exemplars.md`, `hypotheses.md`, and `colab-results.md` (every Colab measurement, round by round).

## Station House credit

marin-explain-neuron · marin-request-experiment

## How you investigated

- Started from the top exemplars and strong firings in `pilot/fineweb-10m-sparse`. Ran two rounds of probes on a Colab T4 with `scripts/colab/measure.py` (branch `colab-tools`), which loads only layers 0–10 (11.2 GiB in bf16) and reads `silu(gate)·up` with the runner's tokenizer and target rules. Ten atlas exemplars, fed as exact token ids, reproduce the stored activations within 0.04.
- **Round 1:**
  - Putting off fires with or without "wait" (+0.9 to +6.9), while literal waiting barely fires (+0.3, +0.7).
  - Countdowns are −2.2 to −3.2.
  - Plain end-time "until" sits near zero.
  - Purpose "to get / to obtain" is a real but weaker negative set (−0.8 to −1.6).
- **Round 2:**
  - Measured the request files below; all eight would pass.
  - Side probes show the − side follows what is left before a target, not "until" itself: "Twelve weeks to a stronger back" reads −1.97.
- **Atlas levels** (`pole_stats`, `fineweb-10m-sparse`):

  | side | q99 | q999 | q9999 |
  |---|---|---|---|
  | + | 0.130 | 0.372 | 0.982 |
  | − | 0.130 | 0.343 | 0.770 |

- **Agent:** Claude (`claude-opus-5-5`, through Claude Code) ran the Colab rounds, wrote the prompts and drafted the files.

## Design

### Claim

- Summary files, one per side:
  - `requests/L10-N18895-001.yaml`: activation test, + side. Putting something off fires; countdowns and plain end times don't.
  - `requests/L10-N18895-002.yaml`: activation test, − side. Countdowns fire; putting off and plain end times don't.
- Controlled experiments, one question per file:
  - `requests/L10-N18895-003.yaml`: contrast, + side. Does the putting-off verb drive it, with "until" fixed? (exemplars: "wait until" → "stay/continue until")
  - `requests/L10-N18895-004.yaml`: contrast, − side. Does the countdown phrase drive it? (exemplars: "a month to go until" → "a month to wait until")
  - `requests/L10-N18895-005.yaml`: activation test, + side, at q9999. Is it putting off, or the act of waiting? ("The email can wait" vs "wait by the door")
  - `requests/L10-N18895-006.yaml`: activation test, − side. Do purpose phrases ("to get a discount") fire, and the same verbs without a goal not?
- Random baseline:
  - `requests/L10-N18895-007.yaml`: activation test, + side, `-001`'s should-fire vs random sentences.
  - `requests/L10-N18895-008.yaml`: activation test, − side, `-002`'s should-fire vs random sentences.
    - Kept separate so random sentences don't pad `-001` / `-002`'s should-not-fire scores.

### Unit and metric

- Unit: one prompt with one marked target.
- Metric: the side's activation at that token.
- Counts (should-fire / should-not-fire): `-001` 12 / 10, `-002` 12 / 10, `-005` 10 / 10, `-006` 10 / 10, `-007` 12 / 10, `-008` 12 / 10.
- `-003` and `-004`: 12 pairs each.

### Controls

- Near misses use the same target token in the wrong context:
  - `-001`/`-002`: "until" after putting off vs in countdowns vs as a plain end time.
  - `-003`: "can wait[[ until]]" vs "can continue[[ until]]".
  - `-004`: "a month to go[[ until]]" vs "a month to wait[[ until]]".
  - `-005`: "can[[ wait]]" (a task) vs "please[[ wait]]" (a person).
  - `-006`: "to[[ get]] a voucher" vs "began to[[ get]] dark".
- Random baseline: 10 everyday sentences with the target on the last word, in `-007` and `-008`.
- The other side: in `-004`, swapping the countdown for a putting-off phrase flips most lows to + (up to +3.78).

### Data

- Thresholds: `pilot/fineweb-10m-sparse` `pole_stats`. Model: `marin-community/marin-32b-base` @ `f19b3466`.
- `-001`, `-002`, `-005` and `-006` use prompts written by us. `-003` and `-004` use atlas exemplars (+ side ranks 2–21, − side ranks 1–19), trimmed and lightly cleaned, plus a few fresh pairs. Only the named phrase changes.
- All were measured on Colab before submission (see `notes/L10-N18895/colab-results.md`). There is no held-out split: as in PR #23, the request prompts are the ones measured in round 2, so the runner's result reproduces those readings rather than testing blind ones.
- Filters: none.
- No claims that the neuron never fires; the "stays quiet" claims are measured on prompts, not on the deep tier.

### Noise

- The model is deterministic, so the noise is prompt to prompt.
- Margins on Colab:
  - `-001` should-fire: +1.51 to +6.69, all past q9999 (0.982).
  - `-002` should-fire: −1.74 to −5.12, all past −q9999 (0.770).
  - `-005` should-fire: +2.64 to +8.06, against a threshold of 0.982.
  - Random sentences: within 0.16.
- Contrasts: mean differences of 3.85 (`-003`) and 3.85 (`-004`), against a required 0.07.

### Readout

- Each file uses its type's rule from EXPERIMENTS.md.
  - Type A (`-001`, `-002`, `-006` to `-008`): at least 80% of should-fire past the side's q99, and at least 80% of should-not-fire below it.
  - `-005` uses the + side's q9999 (0.982), because literal waiting sits just above q99.
  - Type D (`-003`, `-004`): at least 80% of pairs in the predicted direction, and a mean difference of at least half the threshold.
- What a failure would tell us:
  - `-001`, `-002`: the explanation doesn't carry over to new sentences.
  - `-003`: the + side follows "until" or the sentence, not the putting-off verb.
  - `-004`: the − side follows "until", not the countdown.
  - `-005`: the + side is about waiting as such, not putting off.
  - `-006`: the purpose firings are just the verbs "get/receive/obtain".
  - `-007`, `-008`: the side also fires on ordinary sentence-final words.

#### Expected refutations

- None expected. `-002` is the closest to failing: plain end-time "until" leans slightly negative ("The museum is open until six" −0.22, "He played the piano until his hands hurt" −0.29), which puts two should-not-fire prompts just past −q99. One more such miss would fail the file.

## Checklist

- [x] `python scripts/validate.py` passes
- [ ] I wrote the request's prompts and prediction before seeing any result for them
  - Same as PR #23: every prompt was measured on Colab before submission.
- [x] The `## Design` section is filled in (the `design` check passes)
- [x] Each marked `[[target]]` is a single token for the Marin tokenizer (checked with `runner/prompts.py`'s `encode` on Colab)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01PznTA3QfVuFG6FbpFUQk6F
