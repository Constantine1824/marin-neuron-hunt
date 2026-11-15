# L6-N9321, negative side: what was unclear, and experiments to narrow it down

Read `exemplars.md` first. This file is for choosing which hypotheses to test. The sentences below only show
the *shape* of each test. I'll write the real prompts after you approve a set, and none of them have been run
yet.

## Working picture

- **+ side:** a week or weekday word that refers to **one occasion**: "one morning last week", "on Monday,
  December 21", "the week before Christmas", "the 27th falls on a Sunday".
- **− side:** the same words when they name a **repeating slot**: "every week", "airs every Tuesday", "once a week
  on Sunday", "each week". It also fires in **serial content** (weekly columns, shows, recaps), including on
  words that aren't about time ("edition", "host", "meeting").
- Both sides fire on the same tokens. " week" is the top token on both sides: 879 strong + firings and 551
  strong − firings. The context decides the sign, not the word.

**One thing the exemplars can't tell us:** the model only sees text up to the target. In "on[[ Monday]], December
21", the date comes after the target, so it can't be what drives the + reading. Whatever drives the sign has to
come before the target.

## What's unclear

| # | Question | Why it's unclear |
|---|---|---|
| U1 | Is the − side driven by a **nearby repetition word** ("every", "each", "weekly", "once a week"), or by the **text being a series** (a weekly column, show or schedule)? | Some strong − firings have no nearby repetition word: "This[[ week]] we take a look at…" (−2.20) in a weekly column, and "[[Tuesday]], December 3" (−2.56) under "This Week ⏎ Game No. 6". |
| U2 | Does **"this week"** flip with the type of text? | It reads + in narratives ("One morning this[[ week]], I woke", +2.12) and − in serial content ("This[[ week]] we take a look", −2.20). This is the cleanest contrast we have. |
| U3 | Is **repetition** what matters, or **announcement / schedule register**? | Almost every − exemplar is in the present tense or announces something ("airs every Tuesday", "meets on Thursdays"). We haven't seen habitual repetition in a past-tense story ("we went to church every Sunday as kids"). |
| U4 | Where do **rates** go ("3 days a week", "per week")? | "6 days of effort per[[ week]]" is +1.63, but "hours a[[ week]] spent" is −0.45, and "3 days a[[ week]]" is +0.28. These are mixed and fairly common. |
| U5 | Is it about **weeks**, or about repetition vs one occasion **in general**? | The top tokens are almost all week or weekday words, plus some " night". We don't know if "every month", "every morning" or "last year" behave the same way. |
| U6 | Is the − side's spread onto non-time words ("meeting", "host", "edition") the same feature or noise? | They are weak (about −0.3 to −0.5) and always inside schedule or serial text. This matters less, but it decides whether the − side is a token-level or text-level feature. |

## Hypotheses

- **H1, local quantifier:** the sign is set by the few words just before the target. "every/each/weekly/once a"
  gives −, and "last/this/on/the … before X" gives +. The type of text barely matters.
- **H2, text type:** the sign is set by whether the text is part of a series or schedule (column, show, club
  listing, publication note). A nearby "every" is one strong signal of that, but not the only one.
- **H3, repetition meaning:** − means the event recurs in any register, including a past-tense story. + means a
  single event.
- **H4, register:** − is announcement or schedule language (present tense, "airs", "meets", "is held"), not
  repetition as such. A past-tense habit would read + or near zero.
- **H5, weeks only:** the neuron is about the week cycle. Other periods (month, year, morning) read near zero on
  both sides.

H1 and H2 compete for U1/U2, H3 and H4 compete for U3, and H5 is about scope (U5).

## Experiments

These follow the PR #23 setup: two summary files with fresh prompts, then one question per file, and random
baselines kept separate so they don't pad the summary files.

| id | type | Question | Shape of the prompts | What each hypothesis predicts |
|---|---|---|---|---|
| E2 | A, − side | Summary: does − carry over to fresh repeating-slot sentences? | about 11 fresh sentences like "The market is open every[[ Saturday]]". The should-not-fire group uses the same tokens for one occasion. | All hypotheses: − past q99. |
| E3 | D, contrast, exemplar edits | Does swapping the word before the target flip the sign? | Pairs edited from exemplars: "airs every[[ Tuesday]]" ↔ "aired last[[ Tuesday]]", "tune in every[[ week]]" ↔ "tuned in last[[ week]]". | H1: big flip. H2: smaller flip, because the text is still serial. |
| E4 | D, contrast | Does the text type flip "this week" with the local words held fixed? | The same sentence "This[[ week]] we look at …", once after a weekly-column opener and once after a one-off diary opener. | H2: flips. H1: about the same both times. |
| E5 | A, − side | Repetition in a past-tense story. | "When I was a kid we went to church every[[ Sunday]]." vs present-tense schedules. | H3: −. H4: near zero or +. |
| E6 | A, mapping | Where do rates go? | "three days a[[ week]]", "twice per[[ week]]", "40 hours a[[ week]]", "once a[[ week]]". | No firm prediction, so this one is exploratory. If you approve it, I'd submit it as a refutable claim once we pick a side. |
| E7 | A, + and − | Scope beyond weeks. | "every[[ month]]" / "last[[ month]]", "every[[ morning]]" / "that[[ morning]]", "every[[ year]]" / "last[[ year]]". | H5: about zero on both. Otherwise the same split as for weeks. |
| E8 | A | Random baselines for E1 and E2. | Everyday sentences with the target on the last word. | The side's q99 rarely gets crossed. |

**Suggested first batch:** E1, E2, E3 and E4. They settle the main explanation (U1, U2). E5 and E7 are good
next steps if E4 comes out in favour of text type.

## What would make me rewrite the explanation

- If E3 flips strongly but E4 doesn't, the − side is local (H1), and I'd remove "serial content" from the
  explanation.
- If E5 reads −, the − side is about repetition itself (H3), and the register framing goes.
- If E7 shows the same split for months and mornings, the label becomes "single occasion vs recurring time
  slot", without "weekly".
