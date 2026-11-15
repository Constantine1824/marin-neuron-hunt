# L10-N18895: what's unclear, and experiments to narrow it down

Read `exemplars.md` first. This file is for choosing which hypotheses to test. The sentences below only show
the *shape* of each test. I'll write the real prompts after you approve a set, and none of them have been run
yet.

## Working picture

- **+ side, putting something off:** "that will have to[[ wait]]", "could perhaps wait[[ until]] he was settled
  in", "saved the best[[ until]] last", "put off packing[[ until]] the very last minute", "the deferral of …[[
  until]] after 2016". It fires on the verb ("wait") and on the word that links to the later point ("until",
  "till", "for").
- **− side, counting down:** "with a month to go[[ until]]", "30 more miles[[ till]] L.A.", "two weeks left[[
  until]]", "only one more day[[ until]]", "a matter of time[[ until]]". There is a remaining amount, then the
  event.
- **" until" is the top token on both sides:** 446 strong + firings at mean +1.00, and 503 strong − firings at
  mean −0.61. As with your L16 neuron, what comes before "until" sets the sign.

## What's unclear

| # | Question | Why it's unclear |
|---|---|---|
| U1 | Is the + side about **putting something off**, or just the phrase **"wait until"** / "save X for last"? | Almost every top exemplar contains "wait", "save" or "put off". We haven't seen putting off without those words ("postponed the vote[[ until]] May", "held off[[ until]]"). |
| U2 | What does **plain "until"** do, with no putting off and no countdown? | "The shop is open[[ until]] 9", "she lived there[[ until]] 1990", "toast the breadcrumbs[[ until]] golden" (−0.44 in the typical firings). We don't know if this is neutral or sits on one side. |
| U3 | Is the − side about the **remaining amount** ("a month to go", "30 more miles"), or about **counting down** in general? | "counted the hours[[ until]]" (−1.93) has no amount left, and "a matter of time[[ until]]" (−1.71) has no number. It may be about looking ahead to an event. |
| U4 | **"can't wait until"** combines "wait" with eager anticipation. | "I can't wait until Christmas" has the + side's word and the − side's meaning (looking forward to an event). This is the best single prompt for telling the word from the meaning. |
| U5 | What happens when **both cues appear together**? | "We still had to wait two more weeks[[ until]] the parts came" has both a delay and a remaining amount. Which one wins tells us how the two sides combine. |
| U6 | Are the − side's typical firings (**purpose phrases**: "to[[ get]]", "to[[ obtain]]", "redeem this code to[[ receive]]", "you[[ can]] see") the same job? | These are the bulk of the − side's mid-range firings (" for" 704, " to" 457, " get" 447). They are weaker than the countdown firings (about −0.5) and often in ad-like text. They may be a second job, so the − side might be `lumped`. |
| U7 | What are the + side's **"get" / "gets"** firings? | 308 + 210 strong firings at about +0.6: "Allergies will[[ get]] me", "the fridge doesn't[[ get]] very cold", "allow contaminants to[[ get]] inside". There is no obvious putting off. This may be a separate weak job. |
| U8 | Does **"for"** follow the same split? | "saved the best[[ for]] last" (+3.70) and "would have to wait[[ for]] her arrival" (+3.14) are +, but "$8 per month[[ for]] the whole" and "walk[[ for]] ten minutes" are −. |

## Hypotheses

- **H1, putting off (meaning):** + fires when an action or event is pushed to a later point, whatever the verb
  (wait, postpone, delay, hold off, save … for, defer).
- **H1′, the word "wait" (lexical):** + is mostly "wait" and its fixed phrases. Putting off without "wait" or
  "save" reads near zero.
- **H2, remaining amount:** − needs an amount still to go (N days/miles/weeks left, to go, more).
- **H2′, looking ahead to an event:** − fires whenever the text anticipates an upcoming event, with or without an
  amount ("counted the hours until", "can't wait until").
- **H3, the − side is lumped:** the purpose-phrase firings ("to get", "to obtain") are unrelated to counting down.
- **H4, plain "until" is neutral:** an "until" that only marks an end time ("open until 9") reads near zero on
  both sides.

H1 and H1′ compete for U1, H2 and H2′ compete for U3/U4, H3 is about U6, and H4 is about U2.

## Experiments

These follow the PR #23 setup: two summary files with fresh prompts, then one question per file, and random
baselines kept separate.

| id | type | Question | Shape of the prompts | What each hypothesis predicts |
|---|---|---|---|---|
| E1 | A, + side | Summary: does + carry over to fresh sentences about putting things off? | about 12 sentences like "The laundry can[[ wait]]", "We put off the trip[[ until]] spring". The should-not-fire group has "until" in countdowns. | + above q99 |
| E2 | A, − side | Summary: does − carry over to fresh countdown sentences? | about 11 sentences like "Only three days left[[ until]] the exam". The should-not-fire group has "until" after putting off. | − past q99 |
| E3 | D, contrast, exemplar edits | Does swapping the words before "until" flip the sign? | "with a month to go[[ until]] football season" ↔ "we decided to wait[[ until]] football season"; "saved the best[[ until]] last" ↔ "two songs to go[[ until]] the last". | Large flip under H1 and H2 |
| E4 | A, + side | Putting off without "wait" or "save". | "postponed the vote[[ until]] May", "held off[[ until]]", "delayed the launch[[ until]]", "deferred payment[[ until]]". | H1: +. H1′: near zero. |
| E5 | A, − side | Looking ahead without an amount, including "can't wait". | "I can't wait[[ until]] Christmas", "counting the days[[ until]] the wedding", "it's only a matter of time[[ until]]". | H2′: −. H2: near zero. "can't wait" + would point to the word, not the meaning. |
| E6 | A, mapping | Plain end-time "until". | "open[[ until]] 9 pm", "lived there[[ until]] 1990", "stir[[ until]] golden". | H4: near zero. If they fall on one side, the explanation has to widen. |
| E7 | D, contrast | Purpose "get" vs plain "get" (− side lumped or not). | "Redeem this code to[[ get]] a discount" ↔ "I[[ get]] tired after lunch". | H3: purpose −, plain about zero. This tells us whether to list a second job. |
| E8 | A | Random baselines for E1 and E2. | Everyday sentences with the target on the last word. | The side's q99 rarely gets crossed. |

**Suggested first batch:** E1, E2, E3 and E5. They settle the main explanation, and E5 also covers the
"can't wait" prompt. E4 and E6 are the next steps. E7 matters only if we want to state the − side's broader
firings.

## What would make me rewrite the explanation

- If E4 reads near zero, + is mostly the word "wait" (H1′), and the explanation narrows to "wait / save …
  for/until".
- If E5 reads − (including "can't wait until"), − is about looking ahead to an event, not about an amount. The
  label then becomes "putting off vs looking forward".
- If E7 shows purpose "to get" − while plain "get" is near zero, the − side becomes `lumped`, with two jobs.
