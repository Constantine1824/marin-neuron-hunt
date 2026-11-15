## Neuron(s)

L6-N9321

## In plain English

- **Negative side:** fires on "week" or a weekday name when it names a slot that repeats: "every Tuesday", "once a week on Thursday", "weekly on Fridays", "taco Tuesday", or "on Thursday" inside text about a weekly club or show. Past habits count too ("we played poker every Friday night"). It is specific to the week: "every month", "every morning" and "every year" do nothing.
- **Positive side:** fires on "week" (and on a weekday name placed on the calendar) when it points to one particular occasion: "one morning this week", "that week", "Easter week", "New Year's Day fell on a Thursday".
- The same words fire either way, so the context decides the sign. Swapping "every" for "this", or changing only the earlier sentence from a weekly series to a one-off, flips or kills the negative side.

## What's in this PR

- [x] An explanation: `explanations/L6/L6-N9321.yaml`, covering **both sides**
- [x] Confirmation-experiment requests, listed under Design > Claim.
- Reading notes, to be removed before this is marked ready: `notes/L6-N9321/exemplars.md`, `hypotheses.md`, and `colab-results.md` (every Colab measurement, round by round).

## Station House credit

marin-explain-neuron · marin-request-experiment

## How you investigated

- Started from the top exemplars and strong firings in `pilot/fineweb-10m-sparse`. Ran three rounds of probes on a Colab T4 with `scripts/colab/measure.py` (branch `colab-tools`), which loads only layers 0–6 and reads `silu(gate)·up` with the runner's tokenizer and target rules. Ten atlas exemplars, fed as exact token ids, reproduce the stored activations (7 exact, largest gap 0.06).
- **Round 1:** the neuron is specific to the week. "every month/morning/year" and "last month/year" all sit within 0.15 of zero, while the same frames with week or weekday words reach ±3. Past habits fire negative, so the cue is repetition, not schedule language. "This week" flips sign with the type of text.
- **Round 2:** one located "week" is strongly positive. Weekday names need calendar placement to go positive. Named weekly customs (Meatless Monday, casual Friday) are negative, while named one-off days (Black Tuesday, Bloody Sunday) are not.
- **Round 3:** measured the request files below; all eight would pass. `-002` passes at exactly 80% on should-not-fire (see Expected refutations).
- **Atlas levels** (`pole_stats`, `fineweb-10m-sparse`):

  | side | q99 | q999 | q9999 |
  |---|---|---|---|
  | + | 0.074 | 0.229 | 0.835 |
  | − | 0.080 | 0.269 | 0.982 |

- **Agent:** Claude (`claude-opus-5-5`, through Claude Code) ran the Colab rounds, wrote the prompts and drafted the files. Reads on the exemplars came from Hariom.

## Design

### Claim

- Summary files, one per side:
  - `requests/L6-N9321-001.yaml`: activation test, − side. Repeating week/weekday slots fire; the same words for one occasion don't.
  - `requests/L6-N9321-002.yaml`: activation test, + side. One located week or calendar-placed weekday fires; the same words repeating don't.
- Controlled experiments, one question per file:
  - `requests/L6-N9321-003.yaml`: contrast, − side. Does the repetition word right before the target drive it? (atlas exemplars, "every" → "this")
  - `requests/L6-N9321-004.yaml`: contrast, − side. Does a weekly series set up in the earlier sentence drive it, with the target sentence identical?
  - `requests/L6-N9321-005.yaml`: activation test, − side. Is it specific to the week? ("every week" vs "every month/morning/year")
  - `requests/L6-N9321-006.yaml`: activation test, − side. Do named weekly customs fire with no "every", and named one-off days not?
- Random baseline:
  - `requests/L6-N9321-007.yaml`: activation test, − side, `-001`'s should-fire vs random sentences.
  - `requests/L6-N9321-008.yaml`: activation test, + side, `-002`'s should-fire vs random sentences.
    - Kept separate so random sentences don't pad `-001` / `-002`'s should-not-fire scores.

### Unit and metric

- Unit: one prompt with one marked target.
- Metric: the side's activation at that token.
- Counts (should-fire / should-not-fire): `-001` 12 / 10, `-002` 12 / 10, `-005` 10 / 10, `-006` 10 / 10, `-007` 12 / 10, `-008` 12 / 10.
- `-003` and `-004`: 12 pairs each.

### Controls

- Near misses use the same target token in the wrong context:
  - `-001`/`-002`: the same week and weekday words, repeating vs one occasion.
  - `-003`: "tune in every[[ week]]" vs "tune in this[[ week]]".
  - `-004`: the same "The meeting is on[[ Thursday]]." after "meets weekly" vs after "a one-off reunion".
  - `-005`: "every[[ week]]" vs "every[[ month]]", same sentence.
- Random baseline: 10 everyday sentences with the target on the last word, in `-007` and `-008`.
- The other side: removing the repetition cue often flips the sign. In `-004`, lows go up to +1.07 ("Dinner is on Sunday" after a birthday). In `-001`, one-occasion near misses read up to +2.97.

### Data

- Thresholds: `pilot/fineweb-10m-sparse` `pole_stats`. Model: `marin-community/marin-32b-base` @ `f19b3466`.
- `-001`, `-002`, `-004`, `-005` and `-006` use prompts written by us. `-003` uses atlas exemplars (− side, ranks 1–28) trimmed to their sentence, with only the repetition word changed.
- All were measured on Colab before submission (see `notes/L6-N9321/colab-results.md`). There is no held-out split: as in PR #23, the request prompts are the ones measured in round 3, so the runner's result reproduces those readings rather than testing blind ones.
- Filters: none.
- No claims that the neuron never fires. The "other periods stay quiet" claim in `-005` is measured on prompts, not on the deep tier.

### Noise

- The model is deterministic, so the noise is prompt to prompt.
- Margins on Colab:
  - `-001` should-fire: −0.42 to −3.77, all past −q99 (0.080), 11 of 12 past −q999.
  - `-002` should-fire: +0.37 to +4.12, all past +q999 (0.229).
  - `-005` other periods: within ±0.10.
  - Random sentences: within ±0.03.
- Contrasts: mean differences of 1.49 (`-003`) and 2.04 (`-004`), against a required 0.04.

### Readout

- Each file uses its type's rule from EXPERIMENTS.md, with the threshold at the side's q99:
  - Type A (`-001`, `-002`, `-005` to `-008`): at least 80% of should-fire past the threshold, and at least 80% of should-not-fire below it.
  - Type D (`-003`, `-004`): at least 80% of pairs in the predicted direction, and a mean difference of at least half the threshold.
- What a failure would tell us:
  - `-001`, `-002`: the explanation doesn't carry over to new sentences.
  - `-003`: the repetition word doesn't drive the − side; the surrounding exemplar text does.
  - `-004`: the − side is local only; the earlier sentence doesn't matter.
  - `-005`: the − side is about repetition in general, not the week.
  - `-006`: weekday names in named customs aren't read as repeating slots.
  - `-007`, `-008`: the side also fires on ordinary sentence-final words.

#### Expected refutations

- None expected. `-002` is the closest to failing: two of its should-not-fire prompts ("It snows every week here in January" +0.57, "Pilgrims arrive each week by bus" +1.55) read positive. This is a frequency-as-rate reading that the explanation flags as open. One more such miss would fail the file.

## Checklist

- [x] `python scripts/validate.py` passes
- [ ] I wrote the request's prompts and prediction before seeing any result for them
  - Same as PR #23: every prompt was measured on Colab before submission.
- [x] The `## Design` section is filled in (the `design` check passes)
- [x] Each marked `[[target]]` is a single token for the Marin tokenizer (checked with `runner/prompts.py`'s `encode` on Colab)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01PznTA3QfVuFG6FbpFUQk6F
