# L6-N9321: Colab results (T4)

The prompts were measured on a Colab T4 with `scripts/colab/measure.py` (branch `colab-tools`). It loads only
layers 0–6 of `marin-32b-base@f19b3466` in bf16 and reads `silu(gate)·up` at the target, using
`runner/prompts.py`'s tokenizer and target rules. These notes are reading material and will be removed before
the PR is marked ready.

**Check against the atlas:** ten exemplars (ranks 0/1/2/10/25 on each side), fed as the atlas's exact token ids,
reproduce the stored activations. Seven match exactly and the largest gap is 0.06.

Thresholds: + q99 0.074, q999 0.229, q9999 0.835; − q99 0.080, q999 0.269, q9999 0.982.

## Round 1: a first pass over many hypotheses

| group | n | mean | range | read |
|---|---|---|---|---|
| ways of saying "every" (each, on Saturdays, every other, once a week on, weekly on, most Fridays, taco Tuesday) | 11 | −1.92 | −3.39 … −0.90 | all past q9999 except 2 |
| repetition implied by context only ("airs Thursday nights", "New episodes drop on Fridays") | 7 | −0.76 | −1.45 … −0.16 | all negative, weaker |
| one-off weekday ("born on a Thursday", "Christmas fell on a Sunday") | 6 | +0.99 | +0.08 … +3.36 | all positive |
| **other periods, one-off** (last month, this morning, last year …) | 7 | +0.01 | −0.08 … +0.14 | **about zero** |
| **other periods, every** (every month, every morning …) | 7 | +0.00 | −0.10 … +0.07 | **about zero** |
| names (The Weeknd, girl Friday, Shark Week, Black Friday) | 10 | −0.02 | −0.27 … +0.35 | about zero |
| past habit ("we played poker every Friday night") | 4 | −1.50 | −2.50 … −0.49 | negative: repetition alone does it, even outside schedule-style text, for example a memory like "for years she visited his grave every Monday morning" |
| "This week …" after a weekly column or podcast opener | 3 | −1.59 | | |
| "This week …" after a one-off story | 3 | +0.58 | | the type of text flips it |
| rates ("twice per week", "40 hours a week") | 4 | +0.57 | +0.27 … +1.23 | positive, unexpectedly |
| random sentences | 5 | 0.00 | | |

## Round 2: surprises

- **"last + weekday" reads negative** ("met the neighbours last Tuesday" −1.61). Round 5 retested this across six
  sentences: "last Tuesday" reads −0.72 on average (five of six past −q999), while "on Tuesday" and "that
  Tuesday" in the same sentences sit near zero (+0.10, +0.06). The neighbours sentence is negative with every
  frame, so round 2's read that all plain narration leans negative came from that one sentence.
- **Weekday names go strongly positive when the sentence first sets up a dated event** and the weekday says when
  it fell: "Christmas fell on a Sunday" +3.36, "born on a Thursday" +1.48. The model only sees the words before the
  target, so it is the event before the weekday that matters, not a date after it.
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

## Round 4: rate vs slot

We assumed:
- "Pilgrims arrive each week" and "It snows every week" read positive because a frequency for a crowd or the weather
  reads as a rate ("how often"), while one person's "every week" reads as a slot ("when").
- If so, "twice a week" and "twice per week" should go positive for any subject, and "every week" should go
  negative for any subject.

We wrote six sentences (two each about one person, a crowd and the weather) and swapped only the frame at the end:

| frame | person | crowd | weather |
|---|---|---|---|
| every week | −1.17 | +0.82 | +0.72 (snow +1.67, rain −0.23) |
| each week | −1.29 | +0.96 | +0.65 |
| every Friday | −1.53 | −0.05 | −0.32 |
| once a week | −0.84 | +0.33 | +0.55 |
| twice a week | −0.28 | +0.91 | +1.17 |
| twice per week | +0.09 | +1.13 | +1.47 |

"40 hours a week", "600 dollars a week", "500 loaves a week", "30 miles a week": −0.27 on average (−0.55 … −0.07).

- **Who repeats matters more than the frame.** The same "every week" is −1.17 for one person and +0.82 for a crowd.
  A crowd or the weather doing something every week does not read as a repeating slot.
- **Within one person, the frame matters as a gradient:** every/each week −1.2 to −1.3, once a week −0.84, twice a
  week −0.28, twice per week +0.09. The more it reads as a count, the less negative.
- **A named day pulls the crowd and weather back to about zero** ("every Friday": −0.05 and −0.32), but not past −q99
  the way one person's "every Friday" does (−1.53).
- **Amounts per week are not positive:** "40 hours a week" and the like sit slightly below zero, so round 1's
  "rates read positive" holds for counts of events, not amounts.
- Two sentences per cell, so the per-cell means are rough; the person vs crowd split holds in every frame.

## Round 5: weekday vs week in the same one-off sentence

We assumed:
- A weekday name in a plain one-off story stays near zero or slightly negative, and needs a dated event before it to
  go positive.
- "week" in the same story goes positive with no dated event.

We wrote six one-off sentences and swapped only the time word:

| frame | mean | range |
|---|---|---|
| last Tuesday | −0.72 | −1.61 … −0.00 |
| on Tuesday | +0.10 | −0.34 … +0.46 |
| that Tuesday | +0.06 | −0.39 … +0.54 |
| on a Tuesday | −0.33 | −0.73 … +0.16 |
| last week | +0.30 | −0.35 … +0.81 |
| this week | +0.51 | −0.19 … +0.92 |
| that week | +0.73 | +0.26 … +1.09 |
| a dated event, then the weekday ("Christmas fell on a Tuesday", "born on a Tuesday") | +2.12 | +0.21 … +4.69 |

- **"week" goes positive in a plain one-off story; a weekday name does not.** "that week" is positive in all six
  sentences, "that Tuesday" averages zero.
- **"last + weekday" is negative on its own,** not only in the neighbours sentence. "last week" in the same sentences
  is positive, so this is specific to weekday names.
- **"on a Tuesday" without a dated event leans negative** (−0.33), maybe because "a Tuesday" can read as "some
  Tuesday or other". After "Christmas fell on a" or "born on a" it is strongly positive.
- **A dated event before the weekday is what makes it positive:** New Year's Day +4.69, Christmas +4.09, birthday
  +2.16, born +1.04, married +0.21.
- "We met the new neighbours …" is negative with every weekday frame and with "last week", so that sentence pulls
  negative for some other reason.

## Round 6: only the subject changes

Round 4 changed the verb along with the subject ("My brother drives over" vs "Hundreds of pilgrims arrive by bus").
We assumed the subject alone would flip the sign. We kept four predicates fixed and swapped only the subject:

| subject | every week | every Friday |
|---|---|---|
| My brother | −1.28 (−2.05 … −0.86) | −1.55 |
| We | −1.10 | |
| A few of my friends | −0.93 | |
| Pilgrims | +0.00 (−0.65 … +0.77) | |
| Hundreds of pilgrims | +0.42 (+0.26 … +0.74) | −0.21 |
| Thousands of tourists | +0.73 (+0.45 … +0.91) | |

- **The subject alone flips it.** "My brother arrives by bus every week" −0.86, "Hundreds of pilgrims arrive by bus
  every week" +0.74.
- **It is a gradient with group size:** one person, "we" and a few friends are all negative, bare "Pilgrims" is about
  zero, and "Hundreds of" / "Thousands of" are positive in all eight sentences. A counted crowd per week reads like a
  volume ("hundreds a week"), not a slot.
- **A named day pulls the crowd back to about zero** (−0.21), still well short of one person's −1.55.

## What's still open

- **Why "last + weekday" reads negative** (−0.72) while "last week" reads positive (+0.30) in the same sentences.
  Untested.
- **Why a counted crowd's "every week" reads positive.** Round 6 shows the subject alone does it and that it grows
  with the size of the crowd; why a volume per week lands on the + side is untested.
