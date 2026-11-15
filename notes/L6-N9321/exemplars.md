# L6-N9321: exemplars

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

## Positive side (+)

### Which tokens fire past q999 (3578 firings in 1477 documents)

This counts strong firings from the sparse tier, so it shows where the side fires, not where it stays quiet.

| token | firings | mean act |
|---|---|---|
| `' week'` | 879 | +0.57 |
| `' '` | 208 | +0.31 |
| `' weekend'` | 176 | +0.44 |
| `' Sunday'` | 176 | +0.57 |
| `' Saturday'` | 150 | +0.53 |
| `' Monday'` | 130 | +0.58 |
| `' weeks'` | 114 | +0.42 |
| `' Tuesday'` | 111 | +0.59 |
| `' Thursday'` | 107 | +0.56 |
| `' Friday'` | 101 | +0.57 |
| `' Wednesday'` | 99 | +0.54 |
| `'Monday'` | 77 | +0.55 |
| `'Tuesday'` | 69 | +0.49 |
| `'Sunday'` | 63 | +0.46 |
| `'Wednesday'` | 58 | +0.48 |
| `'Thursday'` | 56 | +0.55 |
| `' days'` | 46 | +0.31 |
| `'Friday'` | 41 | +0.45 |
| `' Mon'` | 40 | +0.54 |
| `'Saturday'` | 35 | +0.47 |
| `' weekly'` | 35 | +0.52 |
| `' night'` | 31 | +0.30 |
| `' weekends'` | 23 | +0.51 |
| `' Tue'` | 22 | +0.56 |
| `'-week'` | 21 | +0.39 |

### Top 32 exemplars

| rank | act | context |
|---|---|---|
| 0 | +3.31 | Jesus, come!⏎We need Your Light and Your Love now more than ever.⏎And earthy religions celebrate the Winter Solstice, the beginning of the ascendancy of the sun in the northern hemisphere on**[[ Monday]]**, December 21 at |
| 1 | +2.55 | the Santa Fe ski resort, Ski Santa Fe, seven times daily until New Year’s Day.⏎Normally, the district’s Blue Buses drive to the Santa Fe ski area three times a day during the**[[ week]]**, beginning from the South Capitol |
| 2 | +2.52 | in your behaviour and when things don't go to plan, adjust the plan; and I expect there will be high fives rather than haunts by the time December arrives again.⏎Christmas is one little**[[ week]]** away and I find myself in |
| 3 | +2.45 | a shirt, slop on some sunscreen and slap on a hat and then you would be⏎ready to go out into the sun. It is working because Marvin has worn his hat⏎every day this**[[ week]]** whilst he has been in the |
| 4 | +2.41 | Atlanta Symphony Orchestra with a glorious rendition of Handel’s “And the Glory of the Lord. Click here. Be sure to turn up your speakers and enter full screen.⏎Advent Day 17 ~**[[ Thursday]]** of the third week of Advent |
| 5 | +2.30 | be changed to the 27th of April, which is the king's birthday. In 2014 however it will be on the 26th of April because the 27th falls on a**[[ Sunday]]**. On this day the streets |
| 6 | +2.25 | <\|begin_of_text\|>I woke up one morning last**[[ week]]** and realized I’m not living |
| 7 | +2.16 | the children.⏎After this our father married Miss Platt, of Saybrook, by whom he had one daughter, who died at the age of eighteen.⏎I was born on the first day of February,**[[ Sunday]]** morning, 1801, |
| 8 | +2.12 | by Taylor R Ware This essay proves my love for dance. [317 words]⏎Imagination And Children by Lawson - [600 words]⏎Dead-To-The-World Man Walking by James Snyder One morning this**[[ week]]**, I woke up with a |
| 9 | +2.09 | <\|begin_of_text\|>Daily News -**[[ Thursday]]** 15 January 2015 |
| 10 | +2.02 | <\|begin_of_text\|>December 11, 2020 at 19:10 #28769⏎Burke Electrical Supply usually held its Christmas party on December fifteenth, partly because the**[[ week]]** before Christmas tended to be busy |
| 11 | +1.95 | D’s trolley-esque transit bus… but did you know that the downtown area has an ACTUAL trolley that you can climb aboard? See for yourself!⏎Mardi Gras this year was,**[[ Tuesday]]**, February 28, and |
| 12 | +1.91 | otes) will be our announced as the official Award Winner on August 22nd on every platform!⏎Come by for promotions and deals! We'd love to see you!⏎Store hours for BC Day:⏎**[[Sunday]]** July 31 10am |
| 13 | +1.87 | , the San Joaquin Valley—the swath of agricultural land that runs through central California—was designated a disaster area. Record-low runoff and scant rainfall had created drought conditions. At the beginning of Christmas**[[ week]]**, the weather was normal in |
| 14 | +1.80 | again somewhat suddenly and following a phone call, J was told that she could wind up at the end of the day with the assurance that she would be paid for the few weeks leading up to the annual**[[ week]]** she was scheduled to take at |
| 15 | +1.80 | many home foreclosures as new jobs.⏎Ubuntu on Thinkpad X60s⏎September 17, 2007⏎September 17, 2007⏎The site provides a nice daily (**[[week]]**days) review of the US |
| 16 | +1.79 | this trend continues in 2018, Ireland is likely to experience the highest number of new HIV diagnoses on record.⏎The global theme for World AIDS Day 2018 is ‘Know Your Status’. On**[[ Wednesday]]** 28th November in Le |
| 17 | +1.79 | : You know Candace, this is the second time I've climbed up there. I'm already down half a dress size.⏎- Candace's birthday is July 11, which occurs on a**[[ Friday]]** in this episode.⏎- Cand |
| 18 | +1.73 | <\|begin_of_text\|>4th Annual Depressing Song Competition**[[ Tuesday]]** 8/4 @ |
| 19 | +1.70 | to 10 a.m. at the Capital News Centre Indoor Track. For more information call John Moxness at 250-762-5446 or firstname.lastname@example.org.⏎Birthdays of the**[[ week]]** – Steve Nicholson (May |
| 20 | +1.69 | -tweeting that flashes across our computer screens, especially about politics. But are we gorging on empty calories?⏎To give you just a snapshot, let's look at one random morning this past**[[ Monday]]**.⏎Politico's "44 |
| 21 | +1.69 | ried fruit. If I do say so myself (I think hubby agrees) everything was delicious. Plus we had lots of leftovers – great, no cooking for the next few days!⏎The next morning,**[[ Friday]]**, we went out to breakfast |
| 22 | +1.67 | of the SMART4SEA Awards! SAFETY4SEA is thrilled to announce the 8 winners across 8 smart categories who walked with a SMART4SEA Award at the prestigious ceremony which took place on**[[ Tuesday]]** 30rd at the Y |
| 23 | +1.65 | the last year my website (4 years old) has been getting busier by the day thanks to Google. I felt that I needed to add new content 5 to 6 times a day (**[[week]]**end too!) to my website |
| 24 | +1.64 | . She became blind a few years after her husband’s death and was granted a handicapped parking space for her and her caretaker. To honor Delphine’s 112th birthday, the whole**[[ week]]** was announced as “Delph |
| 25 | +1.63 | , the easier it becomes. The easier it is, it is time to increase the challenge (in exercise, it means more repetitions / more weight). After 30 days (6 days of effort per**[[ week]]**), there is almost always a |
| 26 | +1.61 | ’s a very nice touch. Special thanks to Sriram, Sayyed and Manikandan for co-ordinating the event throughout....See More⏎Dinesh 6 months, 1**[[ week]]**, 2 days, |
| 27 | +1.60 | host an evening reception from 5 to 8 p.m.⏎Castleton Corners: Adults and children will find plenty of holiday activities at the St. Teresa School and Parish's annual Christmas fair on**[[ Sunday]]**, 9 a.m. |
| 28 | +1.60 | some speakers for the upcoming annual Internet Radio event of the year – the RAIN Summit. This event takes place each year during the NAB Show in Las Vegas, this year the one day conference is**[[ Monday]]** April 20th at the |
| 29 | +1.59 | : Third Annual Thanksgiving Cruise⏎Overall Member Rating⏎Third Annual Thanksgiving Cruise⏎This is our "Third Annual Thanksgiving Cruise" for my little family of five. We selected this cruise because it fell during the**[[ week]]** that we all are off of |
| 30 | +1.58 | <\|begin_of_text\|>Greetings from 53.5° where overnight on**[[ Saturday]]** the ambient air temperature and the |
| 31 | +1.56 | : OKC ZOO AND BOB MOORE SUBARU CELEBRATE INTERNATIONAL FLAMINGO DAY⏎Think pink and flock to the Oklahoma City Zoo for International Flamingo Day on**[[ Saturday]]**, April 24, from |

### Typical firings: 25 random ones between q999 and q9999 (|act| 0.23–0.84)

These show what the side does day to day, below the extremes.

| act | context |
|---|---|
| +0.54 | south towards Moe and then swinging back up towards a small town called Erica where we stopped for a late lunch and tripled the towns GDP for the**[[ week]]**.⏎Images by Alan |
| +0.23 | the immense natural beauty of the area along with a feast of live music from some of the very best concert artists in the world. Last year’s June**[[ concert]]** at Rayado was |
| +0.29 | 9 is set for a U.S. theatrical release of December 26th, 2008.⏎Wednesday, January 23, 2008⏎**[[Tuesday]]**, January 22 |
| +0.48 | 2012 as a WR and return man.⏎Day Three Target:⏎Kevin Norwood – Alabama (77)⏎This kid could be one of the top draft**[[ weekend]]** |
| +0.49 | , and Marci Levine will produce the movie.⏎9 is set for a U.S. theatrical release of December 26th, 2008.⏎**[[Wednesday]]**, January 23 |
| +0.26 | their institutions: some extending the call, others placing a new date on their call and even striking indefinitely.⏎Prisoners have been staying strong throughout these**[[ weeks]]** of the prison strike |
| +0.27 | away from Srinagar after incessant rains and cloudburst left many cattle dead and changed course of water of tributaries in the last**[[ week]]** of August.⏎The |
| +0.34 | 2010 tax deal … and helping to pass the American Taxpayer Relief Act of 2012.”⏎DECENT JOBS NUMBER (FOR NOW) –**[[ Friday]]**’s jobs report showing |
| +0.23 | clear, compassionate, honest, and non-violent communication skills⏎· Experience steadiness of mind through heart-centered listening⏎· Embrace freedom⏎The**[[ weekend]]** will include:⏎· |
| +0.28 | of the A. Jean Brugger Project.⏎Over the four-day clinic period, we saw 2,530 patients broken down as follows:⏎Monday**[[ Tuesday]]** Wednesday Thursday Total⏎ |
| +0.64 | s. But the confidence established by our sunrise vigil on the edge of the ICW carried us through the rest of the day.⏎One might think that**[[ weekend]]** boat traffic would interfere |
| +0.53 | this month’s Doodle, but it was only the 29th. I still had two days left! And no idea what to say anyhow.⏎**[[Wednesday]]** began with more sweating |
| +0.82 | corseted waistline and prominent bosom. In July of 1908, Les Modes reported on the fashions worn during La Grande Sem**[[aine]]** – the week that |
| +0.29 | classrooms, campus and culture with fellowship and fun. It invites costumes, and creativity while building community. As Student Council began to flesh out the daily Spirit**[[ Week]]** themes, they stumbled |
| +0.37 | to the public on all federal government work days from 8:30 a.m. to 4:30 p.m.; generally, it is open**[[ Monday]]** through Friday, excluding |
| +0.24 | Sebastian Vizcaíno left Mexico City on March 7, 1602, and arrived in Acapulco on the 19**[[th]]**. His expedition sailed |
| +0.72 | high resolution photos of 15th and 16th century armor are available to download from the Tinguely Museum website.⏎Submitted by Milica on**[[ Tue]]**, 2009 |
| +0.49 | 47:47 CEST 2013⏎Now it works! For download&oter info, the small infopage here .⏎Codecrypt project —**[[ Sun]]** Dec 2 |
| +0.79 | : the first problem was that I didn’t have $2000. And the second problem was that it was a little after 4 am on a**[[ Saturday]]** morning, and the |
| +0.68 | this year, and they want to have a shared meal at the last class, and reconvene on Monday January 31, 2022 (**[[Monday]]** February 7th |
| +0.23 | ina-style, through our great oozy pans of eggs and cheese served at an ungodly hour.⏎bless you each and everyone. ’til**[[ tomorrow]]**…⏎nina’s |
| +0.64 | , and the guys who didn’t have a problem with it were predictably sleazy.⏎Eighteen months of living a double life went by. The**[[ week]]** before Christmas, I |
| +0.54 | astronaut Mark Kelly is joining the company as its Director of Flight Crew Operations. The company announced that it will also begin taking reservations for tis flights this**[[ week]]**.⏎NBC News.com |
| +0.28 | I know but all things I love.⏎I got a new sales job which involved 2 weeks away from home training, and now 3 days a**[[ week]]** based at home, |
| +0.53 | <\|begin_of_text\|>This Month's Stories⏎December 5, 2007⏎December 2007**[[ Newsletter]]**⏎SBE Chapter |

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

