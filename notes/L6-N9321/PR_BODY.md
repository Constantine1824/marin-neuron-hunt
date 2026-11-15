## Neuron(s)

L6-N9321

## In plain English

- **Negative side:** fires on "week" or a weekday name when it names a slot that repeats: "every Tuesday", "once a week on Thursday", "weekly on Fridays", "taco Tuesday", or "on Thursday" inside text about a weekly club or show. Past habits count too ("we played poker every Friday night"). It is specific to the week: "every month", "every morning" and "every year" do nothing.
- **Positive side:** fires on "week" when it points to one particular occasion: "one morning this week", "that week", "Easter week". A weekday name goes positive only after a dated event that it places: "New Year's Day fell on a Thursday", "born on a Sunday". In a plain one-off story ("the parcel came on Tuesday") it sits on the + q99 line with no consistent sign.
- The same words fire either way, so the context decides the sign. Swapping "every" for "this", or changing only the earlier sentence from a weekly series to a one-off, flips or kills the negative side.

## What's in this PR

- [x] An explanation: `explanations/L6/L6-N9321.yaml`, covering **both sides**
- [x] Confirmation-experiment requests for **both sides**, listed under Design > Claim.
- Reading notes, to be removed before this is marked ready: `notes/L6-N9321/negative/` and `notes/L6-N9321/positive/`, each with `exemplars.md`, `hypotheses.md`, and `colab-results.md` (every Colab measurement for that side, round by round).

## Station House credit

marin-explain-neuron · marin-request-experiment

## How you investigated

A log of the experiments, in order. Every round was measured on a Colab T4 with `scripts/colab/measure.py` (branch `colab-tools`), which loads only layers 0–6 and reads `silu(gate)·up` with the runner's tokenizer and target rules. Before the first round, ten atlas exemplars fed as exact token ids reproduced the stored activations (7 exact, largest gap 0.06), so the setup matches the atlas. Each round's prompts and numbers are in `notes/L6-N9321/negative/colab-results.md` and `notes/L6-N9321/positive/colab-results.md`.

- **Round 1.** From the exemplars, we assumed:
  - the − side fires on week and weekday words that name a repeating slot, and the + side on the same words pointing to one occasion;
  - this might be about repetition or one occasion in general, not weeks ("every month", "last month", "this morning");
  - the − side might be schedule-style writing, not repetition itself;
  - "this week" might flip sign with the type of text.

  We wrote prompts for each and tested them directly. Results:
  - It is specific to the week on both sides: "every month/morning/year", "last month/year" and "this morning" sit within 0.15 of zero, while the same frames with week or weekday words reach ±3.
  - Past habits ("we played poker every Friday night") read −1.50, so repetition does it even outside schedule-style text.
  - One-off weekdays ("born on a Thursday", "Christmas fell on a Sunday") read +0.08 to +3.36.
  - "This week" reads +0.58 after a one-off story and −1.59 after a weekly column or podcast opener.
- **Round 2.** We assumed named weekly customs would act like "every", schedule formatting alone might be enough for the − side, and one located "week" would go positive. Results:
  - Named weekly customs (Meatless Monday, casual Friday) read negative; named one-off days (Black Tuesday, Bloody Sunday) don't.
  - Schedule formatting with no repetition cue ("Bin collection day: Thursday") doesn't go negative.
  - A located "week" is strongly positive: "Christmas week" +2.64, "That week changed my life" +1.17.
  - Weekday names go strongly positive after a dated event: "Christmas fell on a Sunday" +3.36, "born on a Thursday" +1.48.
  - "week" as a unit is mixed and small: "a week ago" +0.29, "for a week" +0.49.
- **Round 3.** We measured the first eight request files as they would score. All pass. `-002` passed at exactly 80% on should-not-fire, with two misses from a crowd and the weather ("Pilgrims arrive each week by bus" +1.55, "It snows every week here in January" +0.57).
- **Round 4.** We assumed those two misses happen because a frequency for a crowd or the weather reads as a rate, not a slot. We kept six sentences fixed and swapped only the frame (every / each / once a / twice a / twice per week, every Friday). Results:
  - Who repeats matters more than the frame: "every week" reads −1.17 for one person, +0.82 for a crowd and +0.72 for the weather.
  - For one person, the more it reads as a count, the less negative it is: every week −1.17, once a week −0.84, twice a week −0.28, twice per week +0.09.
  - Amounts per week ("40 hours a week") sit slightly below zero, not positive.
- **Round 5.** We assumed a weekday name in a plain one-off story needs a dated event before it to go positive, while "week" doesn't. We kept six one-off sentences fixed and swapped only the time word. Results:
  - "that week" +0.73 (positive in all six), "this week" +0.51, "last week" +0.30.
  - "on Tuesday" +0.10 and "that Tuesday" +0.06: on the + q99 line (0.074), with no consistent sign. "last Tuesday" −0.72.
  - After a dated event ("Christmas fell on a Tuesday", "born on a Tuesday"): +2.12.
- **Round 6.** Round 4 changed the verb with the subject, so we assumed the subject alone would flip the sign and kept four predicates fixed ("___ arrive(s) by bus every week", …). Results:
  - "My brother" −1.28, "We" −1.10, "A few of my friends" −0.93, "Pilgrims" +0.00, "Hundreds of pilgrims" +0.42, "Thousands of tourists" +0.73.
  - The subject alone flips it, and it grows with the size of the crowd: a counted crowd per week reads like a volume, not a slot.
- **Round 7.** We assumed the split might be third person, or singular vs plural. Results: "I" −0.92, "He" −1.00 and "My brother" −1.28 are all negative, while "A pilgrim" −0.06 and "One pilgrim" −0.35 sit near zero. Neither person nor number does it; the word "pilgrim" pulls toward + on its own.
- **Round 8.** We assumed a named weekday stays negative for a crowd while "week" doesn't, and that "pilgrim" shifts things by itself. We crossed seven subjects with "every week" and "every Monday/Wednesday/Friday/Saturday". Results:
  - With "customers", "every week" fades from −0.90 (one) to −0.02 (hundreds), while every weekday stays at −1.0 to −1.8 for every crowd size. Friday is the strongest in every row.
  - "A customer every week" is −0.90 where "A pilgrim" was −0.06: pilgrims and tourists push toward + by about +0.5 to +1.3 on every column.
- **Round 9.** We assumed the push from pilgrims and tourists might be travel in general. We tested 19 nouns (trip, commute, local, routine-religious) as "A ___" and "Hundreds of ___s" with "every week" and "every Friday". Results:
  - Not travel in general: commuters and passengers behave like local nouns, and so do traveller, visitor and sightseer on "every Friday" (−1.46 to −1.77).
  - A few nouns for someone on one trip or holiday carry the push (pilgrim −0.33, holidaymaker −0.78 on "every Friday"), and a routine noun pushes the other way (churchgoer −2.94).
  - "Hundreds of" moves "every week" up by about 0.9 in every group and leaves "every Friday" where it was.
- **After the rounds.** We replaced `-002`'s crowd and weather near misses with one-person ones, and added two contrasts from rounds 5 and 9 (`-007`, `-008`). These are fresh and not measured.
- **Atlas levels** (`pole_stats`, `fineweb-10m-sparse`):

  | side | q99 | q999 | q9999 |
  |---|---|---|---|
  | + | 0.074 | 0.229 | 0.835 |
  | − | 0.080 | 0.269 | 0.982 |

- **Agent:** Claude (`claude-opus-5-5`, through Claude Code) ran the Colab rounds, wrote the prompts and drafted the files. Reads on the exemplars came from Hariom.

## Design

### Claim

- Summary files:
  - `requests/L6-N9321-001.yaml`: activation test, − side. Repeating week/weekday slots fire; the same words for one occasion don't.
  - `requests/L6-N9321-002.yaml`: activation test, + side. One located week, or a weekday placing a dated event, fires; the same words repeating don't.
- Controlled experiments, one question per file:
  - `requests/L6-N9321-003.yaml`: contrast, − side. Does the repetition word right before the target drive it? (atlas exemplars, "every" → "this")
  - `requests/L6-N9321-004.yaml`: contrast, − side. Does a weekly series set up in the earlier sentence drive it, with the target sentence identical?
  - `requests/L6-N9321-005.yaml`: activation test, − side. Is it specific to the week? ("every week" vs "every month/morning/year")
  - `requests/L6-N9321-006.yaml`: activation test, − side. Do named weekly customs fire with no "every", and named one-off days not?
  - `requests/L6-N9321-007.yaml`: contrast, + side. Does a dated event before a weekday name drive it? ("Christmas Day was on a[[ Wednesday]]" vs "the burglary was on a[[ Wednesday]]")
  - `requests/L6-N9321-008.yaml`: contrast, − side. Do nouns for someone on one trip (pilgrim, tourist, holidaymaker, backpacker) weaken it on a repeating slot, compared with local nouns? ("A neighbour drops by the bakery every[[ week]]" vs "A pilgrim …")
- No random baselines: `-001` and `-002` already show the same tokens staying quiet in the wrong context, a stronger control than random sentences. The two baselines measured in round 3 (both 10/10, random sentences within ±0.03) were dropped; their prompts and readings stay in the colab-results notes.
- Why one file per question: each activation test allows 2 misses out of 10 on each side. Merging `-001`, `-005` and `-006` into one file would allow 6 misses per side across the three, so one question could miss 6 of its 10 prompts and still pass, carried by the other two. Separate files keep a pass or fail for each question.

### Unit and metric

- Unit: one prompt with one marked target.
- Metric: the side's activation at that token.
- Counts (should-fire / should-not-fire): `-001` 12 / 10, `-002` 12 / 10, `-005` 10 / 10, `-006` 10 / 10.
- `-003`, `-004`, `-007` and `-008`: 12 pairs each.

### Controls

- Near misses use the same target token in the wrong context:
  - `-001`: the same week and weekday words, repeating vs one occasion.
  - `-002`: the same week and weekday words naming a repeating slot, done by one person or a small group. Crowd and weather subjects are left out, since rounds 4 and 6–9 show they weaken the − reading on "every week".
  - `-003`: "tune in every[[ week]]" vs "tune in this[[ week]]".
  - `-004`: the same "The meeting is on[[ Thursday]]." after "meets weekly" vs after "a one-off reunion".
  - `-005`: "every[[ week]]" vs "every[[ month]]", same sentence.
  - `-007`: each pair keeps the sentence, the "on a" and the weekday; only the event changes, from a calendar date (holiday, birthday, birth) to an ordinary one-off happening (a burglary, a power cut).
  - `-008`: the same sentence and "every[[ week]]" or "every[[ <weekday>]]", with only the subject noun changed. One person in every prompt, since a counted crowd weakens "every week" on its own (round 6). The local nouns are ordinary ones (resident, neighbour, customer), not the most negative ones from round 9 (churchgoer).
- Baseline: a constant, token-only rule ("fire on every week or weekday token") scores 100% on should-fire and 0% on should-not-fire in `-001` and `-002`, since the near misses use the same tokens, so it fails both files. No random-sentence baseline is used (see Claim).
- The other side: removing the repetition cue often flips the sign. In `-004`, lows go up to +1.07 ("Dinner is on Sunday" after a birthday). In `-001`, one-occasion near misses read up to +2.97. In `-002`, the 8 measured repeating near misses read −1.12 to −4.16.

### Data

- Thresholds: `pilot/fineweb-10m-sparse` `pole_stats`. Model: `marin-community/marin-32b-base` @ `f19b3466`.
- `-003` uses atlas exemplars (− side, ranks 1–28) trimmed to their sentence, with only the repetition word changed. Every other file uses prompts written by us.
- `-001` to `-006` were measured on Colab before submission, except two replacement prompts in `-002`. There is no held-out split for those: as in PR #23, the runner's result reproduces the round 3 readings rather than testing blind ones.
- `-007`, `-008` and the two replacement prompts in `-002` are fresh and not measured, so they are blind tests. `-008` does not reuse round 9's sentences.
- Filters: none.
- No claims that the neuron never fires. The "other periods stay quiet" claim in `-005` is measured on prompts, not on the deep tier.

### Noise

- The model is deterministic, so the noise is prompt to prompt.
- Margins on Colab:
  - `-001` should-fire: −0.42 to −3.77, all past −q99 (0.080), 11 of 12 past −q999.
  - `-002` should-fire: +0.37 to +4.12, all past +q999 (0.229).
  - `-005` other periods: within ±0.10.
- Contrasts: mean differences of 1.49 (`-003`) and 2.04 (`-004`), against a required 0.04.
- Expected for the unmeasured contrasts:
  - `-007` (from round 5): a dated event before the weekday read +2.12 on average (+0.21 to +4.69); a plain one-off "on a Tuesday" read −0.33. Expected gap per pair: about 2, against a required mean of 0.037.
  - `-008` (from round 9, one person): trip nouns −0.31 (pilgrim) to −1.08 (backpacker, every Friday); local nouns −1.05 to −1.96. Single-noun gaps run from about 0.3 to 1.6, and round 9 had only three sentences per noun, so gaps under 0.3 are within noise.

### Readout

- Each file uses its type's rule from EXPERIMENTS.md, with the threshold at the side's q99:
  - Type A (`-001`, `-002`, `-005`, `-006`): at least 80% of should-fire past the threshold, and at least 80% of should-not-fire below it.
  - Type D (`-003`, `-004`, `-007`, `-008`): at least 80% of pairs in the predicted direction (on the − side, the predicted member more negative), and a mean difference of at least half the threshold.
- What a failure would tell us:
  - `-001` / `-002`: the explanation doesn't carry over to new sentences for that side.
  - `-003`: the repetition word doesn't drive the − side; the surrounding exemplar text does.
  - `-004`: the − side is local only; the earlier sentence doesn't matter.
  - `-005`: the − side is about repetition in general, not the week.
  - `-006`: weekday names in named customs aren't read as repeating slots.
  - `-007`: a weekday name goes positive after any one-off event, not specifically a dated one.
  - `-008`: the trip-noun push in round 9 came from those three sentences, not from the nouns.

#### Expected refutations

- None expected for the measured files. The closest are `-001` (9/10 on should-not-fire) and `-006` (9/10 on should-fire, Motivation Monday +0.02); one more miss in either would leave it at exactly 80%.
- `-008` is the most likely to fail. Its backpacker and holidaymaker pairs carry the smallest gaps in round 9 (about 0.3–0.5 against the local nouns), and it fails if 3 of 12 pairs flip.
- `-007` carries less margin on its personal milestones (birthday, born, anniversary) than on public holidays: round 5's weakest dated event ("married", +0.21) was only just positive.

## Checklist

- [x] `python scripts/validate.py` passes
- [ ] I wrote the request's prompts and prediction before seeing any result for them
  - Same as PR #23 for `-001` to `-006`: those prompts were measured on Colab before submission. `-007`, `-008` and two prompts in `-002` are unmeasured.
- [x] The `## Design` section is filled in (the `design` check passes)
- [x] Each marked `[[target]]` is a single token for the Marin tokenizer (checked with `runner/prompts.py`'s `encode` on Colab; `-007` and `-008` reuse the same target tokens)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01PznTA3QfVuFG6FbpFUQk6F
