# L6-N9321: exemplars, negative side

Data: `pilot/fineweb-10m-sparse`. In each context the firing token is **[[bracketed]]**, newlines are shown as ⏎, and ⟨BOS⟩ marks a document start. Activation = silu(gate)·up, the input to `down_proj`.

This file is reading material for the draft PR, not an explanation. It will be removed before the PR is marked ready.

## Levels

| side | q99 | q999 | q9999 | extreme |
|---|---|---|---|---|
| + | 0.074 | 0.229 | 0.835 | +3.31 |
| − | 0.080 | 0.269 | 0.982 | -3.48 |

Fraction of tokens with a positive activation: 0.452.

**Logit lens** (what this neuron's output pushes the unembedding toward; at this early layer it is mostly noise):

- promotes: `' Sek'`, `' recreated'`, `'GW'`, `' Julian'`, `' Cho'`, `' Hog'`, `' Yaz'`, `' Sly'`, `' Thunder'`, `' yaz'`
- suppresses: `' minim'`, `' Movement'`, `'chat'`, `' =>\n'`, `' tide'`, `' Fridays'`, `' merc'`, `' Thurs'`, `' �'`, `'ц'`

## Negative side (−)

### Which tokens fire past q999 (4967 firings in 1089 documents)

This counts strong firings from the sparse tier, so it shows where the side fires, not where it stays quiet.

| token | firings | mean act |
|---|---|---|
| `' week'` | 551 | -0.73 |
| `' '` | 278 | -0.48 |
| `' Friday'` | 175 | -0.74 |
| `' weeks'` | 174 | -0.53 |
| `' weekly'` | 173 | -0.85 |
| `' Sunday'` | 127 | -0.64 |
| `' Saturday'` | 119 | -0.58 |
| `' night'` | 99 | -0.57 |
| `' meeting'` | 95 | -0.46 |
| `' Monday'` | 83 | -0.75 |
| `' meetings'` | 66 | -0.49 |
| `' Thursday'` | 61 | -0.70 |
| `' at'` | 60 | -0.46 |
| `' Tuesday'` | 56 | -0.75 |
| `' Week'` | 54 | -0.72 |
| `' Wednesday'` | 53 | -0.62 |
| `' weekend'` | 50 | -0.53 |
| `' of'` | 47 | -0.50 |
| `'days'` | 47 | -0.85 |
| `','` | 45 | -0.38 |
| `'.'` | 42 | -0.39 |
| `'7'` | 38 | -0.49 |
| `' on'` | 33 | -0.50 |
| `'’s'` | 31 | -0.54 |
| `' show'` | 30 | -0.48 |

### Top 32 exemplars

| rank | act | context |
|---|---|---|
| 0 | -3.48 | wed as Second Class Matter September 20,1902, at the Post Office at Dillon, Montana, Under the Act of Congress of March 3, 1879. Issued Wednesday of Every**[[ Week]]**. All letter« pertaining to |
| 1 | -3.44 | 1-2 PT on YouTube. You can ask questions on the live chat. Videos of the talks are available on YouTube afterward as well. Give the channel a follow here, and tune in every**[[ week]]** for an exciting discussion!⏎The |
| 2 | -3.42 | UCSB star Don Ford and Santa Barbara News-Press legend Mark Patton handle the color commentary.⏎• Talk'n Gauchos⏎UCSB Athletics' weekly radio show, Talk'n Gauchos, airs every**[[ Tuesday]]** from 6-7 p |
| 3 | -3.23 | One of the Top 100 Comedians of All Time. Here, he interviews celebrated actors, writers, directors, comedians, and masters of the tech universe. New episodes drop weekly on Tues**[[days]]**.⏎with David Koechner |
| 4 | -3.19 | as One of the Top 100 Comedians of All Time. Here, he interviews celebrated actors, writers, directors, comedians, and masters of the tech universe. New episodes drop weekly on**[[ Tues]]**days.⏎with David Koe |
| 5 | -2.88 | If doing it alone, it is best to do the meditation for 2 minutes when you wake in the morning and right before you go to sleep. The group meditation will be held once a week on**[[ Sunday]]** at 3:45pm |
| 6 | -2.80 | <\|begin_of_text\|>The SEC Bachstory will be a weekly SEC recap posted every**[[ Monday]]** morning breaking down all the big |
| 7 | -2.64 | and neutering program. NEW vets and MANY locations! For MORE info: www.baacs.org or 304-728-8330.⏎Intermediate Bridge players are invited to join an informal group meeting every**[[ Wednesday]]**, 10 a.m. |
| 8 | -2.62 | <\|begin_of_text\|>Welcome to this week’s gaming**[[ edition]]** of iPhone Gems. We’re |
| 9 | -2.59 | UlUkl⏎J. Foster Marshall, having returned⏎from his southern trip, is now ready to⏎attend to business. Uo can bo seen in⏎Mound City on Saturday of each**[[ week]]**,⏎and in Oregon tho remainder |
| 10 | -2.58 | <\|begin_of_text\|>Ask 411 Music 7.5.12: The Soundtrack⏎It’s that time of the**[[ week]]** again, kids, so sober |
| 11 | -2.56 | <\|begin_of_text\|>To download this complete release as a PDF, please click here.⏎• This Week⏎Game No. 6⏎**[[Tuesday]]**, December 3, |
| 12 | -2.52 | dry every Sabbath day. --- Pliny the Elder, Natural History, book 31, chapter 18⏎The legend was that this river would have water flowing very strongly, even carrying stones, every**[[ week]]** day but would get dry every |
| 13 | -2.52 | SOZI, we are going to take off every Wednesday for a look at the old steam/diesel navies of the 1859-1946 time period and will profile a different ship each**[[ week]]**. These ships have a life |
| 14 | -2.45 | our upstairs bedrooms. Current housemates are all in their mid-20s and are looking for other friendly and social housemates to share the house with that will enjoy group activities like our weekly taco t**[[uesday]]** nights at the house, but |
| 15 | -2.41 | <\|begin_of_text\|>In this week's recap, I introduce a new format for you. After two**[[ weeks]]** of the player of the year |
| 16 | -2.31 | But grassroots skating seems to be thriving. Skate Like a Girl S.F. has partnered with Bay Area Derby for Friday night all-ages lessons and skating in the Derby practice facility. Miles leads a weekly**[[ Friday]]** night Midnight Rollers skate around |
| 17 | -2.30 | would progress to the finals.⏎Regardless of the outcome on the exam, participation in Biology Olympiad is a great way for students to explore their interest in the life sciences.⏎The Chess Club meets on Thurs**[[days]]** following school. Students and faculty |
| 18 | -2.30 | on campus, while also educating the rest of the student body about this effort.⏎The Debate Club gives students a sense of how to properly organize and present arguments in a lucid, structured fashion. Each**[[ week]]** teams of students work on plans |
| 19 | -2.30 | <\|begin_of_text\|>Hello, gentle readers, and welcome to the RPG Reload, the**[[ weekly]]** feature where the healer never heals |
| 20 | -2.30 | <\|begin_of_text\|>Hello, gentle readers, and welcome to the RPG Reload, the weekly feature where the healer never heals quite as fast as we’d like. Each**[[ week]]**, we take a look at |
| 21 | -2.22 | cala is now hosting Sunday Services with Chaplain Edwin in The Chapel. The Sunday Services are 20 minutes long and open to all. Attendees can park by Barns E & F. See the**[[ weekly]]** Chapel Service schedule below.⏎7 |
| 22 | -2.22 | practices that help leaders show up at their best for their teams.⏎Sarah Noll Wilson 0:03⏎Hello, and welcome to this week’s episode of Conversations on Conversations, where each**[[ week]]** we explore a topic to help |
| 23 | -2.20 | previous weekend. In order to eliminate all confusion, the Bach in Bachstory is pronounced like back (Back to the Future, The Empire Strikes Back, Back in Black), you get the picture. This**[[ week]]** we take a look at a |
| 24 | -2.17 | Episcopal activities that take place in the classroom, on campus, or around the community. To include your news, please send a note to firstname.lastname@example.org⏎To ensure weekly publication requirements are met each**[[ Monday]]**, all content must be received |
| 25 | -2.17 | queer community.⏎ICandy's dance floor hops almost nightly, with DJs spinning various music genres. When it's warm, the rooftop deck offers a scenic view and fresh air. Their weekly Frat House**[[ Friday]]** is popular, as is their |
| 26 | -2.11 | know that Real Championship Wrestling is holding a show this Saturday night at the Du Burns Arena in Baltimore. Say hello to Frankenstorm Sandy’s worst nightmare, Chris Methods!⏎His opponent presents the TV List every**[[ Saturday]]** in the Movie Zone. Here |
| 27 | -2.09 | Peter’s, quite rightly sitting at the foot of the cross. If you come to Glendowie, and I’m assuming that is the case, it’s usually right here in front of you every**[[ week]]** in the form of this pul |
| 28 | -2.08 | this study revealed that the actual customer decision making process indicated the operational aspects of the property were more important. There’s no problem with registering from South Africa, there is a Party Poker Weekly Tournament held every**[[ Sunday]]**. As you travel deep into |
| 29 | -2.06 | ton. What a wonderful week of orange foods! I feel so healthy :) I can't help but feel energized and happy and excited about life when I have such yummy foods to look forward to!⏎**[[Sunday]]**, January 20, |
| 30 | -2.06 | <\|begin_of_text\|>This is my weekly**[[ summary]]** of news that the legacy media |
| 31 | -2.03 | <\|begin_of_text\|>In the fall of 2001, my graduate media theory seminar at MIT met every**[[ Tuesday]]** and Thursday at noon. Classes |

### Typical firings: 25 random ones between q999 and q9999 (|act| 0.27–0.98)

These show what the side does day to day, below the extremes.

| act | context |
|---|---|
| -0.73 | <\|begin_of_text\|>NEw YOGA Class in Ithaca⏎Thursdays**[[,]]** 9:30 |
| -0.64 | before its source fish can even be caught. Wayne Bacon, president of Hammersmith Marketing Pte wrote in his January 10, 2010**[[ weekly]]** report that, " |
| -0.45 | appropriate activities. Applicants wishing to receive credit for such experience must indicate clearly the nature of their duties and responsibilities in each position and the number of hours a**[[ week]]** spent in such employment |
| -0.27 | !!) I have a few more pictures I want to get scrapped from our weekend adventure, those should be coming soon.⏎Thanks for stopping by!!⏎Last**[[ Saturday]]** the family loaded up |
| -0.35 | to: firstname.lastname@example.org⏎RIO BLANCO Masonic Lodge #80 meets 2nd and 4th Thursday, 7:**[[00]]** p.m., at |
| -0.65 | mentioned, said dish appears on the calendar and head to their respective date.] "You've got Salisbury Steak Sundays, Meatball Mondays, Turkey Loaf**[[ Tues]]**days, Wieners |
| -0.35 | iskeys.⏎Sunday – Thursday, 11am-12am \| Friday – Saturday, 11am-1am⏎A blissful, freshly**[[ baked]]** array of authentic French |
| -0.41 | or gluten-free plans, Home Chef does not. But there’s no need to worry because it doesn’t mean you won’t have plenty of variety each**[[ week]]**.⏎How it works |
| -0.39 | Mike Kelley said he didn't set out to cause a fuss with "Swingtown," the provocative CBS drama that premieres 9 p.m.**[[ Thursday]]** on WBBM |
| -0.34 | \|\|*January 29 - February 4\|⏎\|The Passion Week\|⏎\|SABBATH AFTERNOON January 29\|⏎Read for This Week**[['s]]** Study:⏎\|Mark |
| -0.64 | <\|begin_of_text\|>Resurgent De Leon football ready for district championship matchup at undefeated San Saba⏎Yeagers cherishing last season together⏎Two**[[ weeks]]** into the football season |
| -0.60 | a.m. to 9 a.m. along with Business Insider’s Joe Weisenthal and Reuters’ Dan Colarusso. Tune in! As**[[ always]]**, send your tips |
| -0.64 | ⏎Eric Roberts' wife brings in some bling for Yossi \| Beverly Hills Pawn (1:01)⏎Saturdays 9ET/10**[[PT]]** on REELZ |
| -0.41 | For more information, contact 304-876-6244.⏎The Shepherdstown Museum, at the corner of German and Princess streets, is open on**[[ weekends]]** from April through October |
| -0.38 | . Aug. 4 in the Lawn Garden at the San Diego Botanic Garden, 230 Quail Gardens Drive, Encinitas. Children’s**[[ activities]]** 4:30 |
| -0.28 | communities.⏎Do not post your personal information in the group. This includes your address and/or phone number. This is for your protection.⏎Do not contact**[[ group]]** member via Private Message |
| -0.73 | 8⏎Sydney University has returned to form with a 40 to 12 victory over Southern Districts at University Oval.⏎Still stinging from last**[[ week]]**'s loss to East |
| -0.52 | and often manage to turn a losing week into a winning one.⏎To post on the plus side for the week, the Dow would need a rally on**[[ Friday]]** of 490 points |
| -0.48 | <\|begin_of_text\|>Here at LSOZI, we are going to take off every Wednesday for a look**[[ at]]** the old steam/d |
| -0.42 | after match with efforts on the pitch sparking off waves of c.ld has limited his attacking tendencies to construct a formidable shield in front of the defence.Mart**[[ono]]** came very close to |
| -0.41 | Conversations on Conversations, where each week we explore a topic to help us have better conversations with ourselves, and with each other. I’m your**[[ host]]**, Sarah Noll |
| -0.30 | members of the remuneration committee are Tim Bushell as chairman, Alison Baker, Keith Lough and John Summers. The board chairman is invited to**[[ meetings]]** with observer status.⏎ |
| -0.28 | answer your real-world money questions.⏎This week’s episode starts with a discussion about why you should scrutinize your bills.⏎Then we pivot to this week**[[’s]]** money question from a |
| -0.35 | from Christmas unused, and happily bought a copy for my (small–but growing!) cookbook shelf. I have already made two recipes over the past several**[[ weeks]]**, both of which |
| -0.28 | USA, UK, Australia, Canada and many other countries. 12 Sep 2013 About 2.2 million in the United States and **[[52]]**,500 in Canada |

