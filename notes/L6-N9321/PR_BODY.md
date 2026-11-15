## Neuron(s)

L6-N9321

## In plain English

- **Negative side:** fires on "week" or a weekday name when it names a slot that repeats: "every Tuesday", "once a week on Thursday", "weekly on Fridays", "taco Tuesday", or "on Thursday" inside text about a weekly club or show. Past habits count too ("we played poker every Friday night"). It is specific to the week: "every month", "every morning" and "every year" do nothing.
- **Positive side:** fires on "week" when it points to one particular occasion: "one morning this week", "that week", "Easter week". A weekday name goes positive only after a dated event that it places: "New Year's Day fell on a Thursday", "born on a Sunday". In a plain one-off story ("the parcel came on Tuesday") it stays near zero.
- The same words fire either way, so the context decides the sign. Swapping "every" for "this", or changing only the earlier sentence from a weekly series to a one-off, flips or kills the negative side.

## What's in this PR

- [x] An explanation: `explanations/L6/L6-N9321.yaml`, covering **both sides**
- [x] Confirmation-experiment requests, listed under Design > Claim.
- Reading notes, to be removed before this is marked ready: `notes/L6-N9321/exemplars.md`, `hypotheses.md`, and `colab-results.md` (every Colab measurement, round by round).

## Station House credit

marin-explain-neuron · marin-request-experiment

## How you investigated

A log of the experiments, in order. Every round was measured on a Colab T4 with `scripts/colab/measure.py` (branch `colab-tools`), which loads only layers 0–6 and reads `silu(gate)·up` with the runner's tokenizer and target rules. Before the first round, ten atlas exemplars fed as exact token ids reproduced the stored activations (7 exact, largest gap 0.06), so the setup matches the atlas. Each round's prompts and numbers are in `notes/L6-N9321/colab-results.md`.

- **Round 1.** From the exemplars, we assumed:
  - the − side fires on week and weekday words that name a repeating slot, and the + side on the same words for one occasion;
  - this might be about repetition in general, not weeks ("every month", "every morning");
  - it might be schedule-style writing, not repetition itself;
  - "this week" might flip sign with the type of text.

  We wrote prompts for each and tested them directly. Results:
  - It is specific to the week: "every month/morning/year" and "last month/year" sit within 0.15 of zero, while the same frames with week or weekday words reach ±3.
  - Past habits ("we played poker every Friday night") read −1.50, so repetition does it even outside schedule-style text.
  - "This week" reads −1.59 after a weekly column or podcast opener and +0.58 after a one-off story.
- **Round 2.** We assumed one located "week" would go positive, named weekly customs would act like "every", and schedule formatting alone might be enough. Results:
  - A located "week" is strongly positive ("Christmas week" +2.64).
  - Named weekly customs (Meatless Monday, casual Friday) read negative; named one-off days (Black Tuesday, Bloody Sunday) don't.
  - Schedule formatting with no repetition cue ("Bin collection day: Thursday") doesn't go negative.
- **Round 3.** We measured the request files below as they would score. All eight pass; `-002` passes at exactly 80% on should-not-fire (see Expected refutations).
- **Round 4.** We assumed "Pilgrims arrive each week" and "It snows every week" read positive because a frequency for a crowd or the weather reads as a rate, not a slot. We kept six sentences fixed and swapped only the frame (every / each / once a / twice a / twice per week, every Friday). Results:
  - Who repeats matters more than the frame: "every week" reads −1.17 for one person, +0.82 for a crowd and +0.72 for the weather.
  - For one person, the more it reads as a count, the less negative it is: every week −1.17, once a week −0.84, twice a week −0.28, twice per week +0.09.
  - Amounts per week ("40 hours a week") sit slightly below zero, not positive.
- **Round 5.** We assumed a weekday name in a plain one-off story stays near zero and needs a dated event before it to go positive, while "week" doesn't. We kept six one-off sentences fixed and swapped only the time word. Results:
  - "that week" +0.73, "this week" +0.51, "last week" +0.30.
  - "on Tuesday" +0.10, "that Tuesday" +0.06, "last Tuesday" −0.72.
  - After a dated event ("Christmas fell on a Tuesday", "born on a Tuesday"): +2.12.
- **Round 6.** Round 4 changed the verb with the subject, so we assumed the subject alone would flip the sign and kept four predicates fixed ("___ arrive(s) by bus every week", …). Results:
  - "My brother" −1.28, "We" −1.10, "A few of my friends" −0.93, "Pilgrims" +0.00, "Hundreds of pilgrims" +0.42, "Thousands of tourists" +0.73.
  - The subject alone flips it, and it grows with the size of the crowd: a counted crowd per week reads like a volume, not a slot.
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
  - `requests/L6-N9321-002.yaml`: activation test, + side. One located week, or a weekday placing a dated event, fires; the same words repeating don't.
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
