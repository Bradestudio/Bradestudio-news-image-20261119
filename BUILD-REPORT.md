# Build report — news-image-20261119, round 3

## What this is

Round 3 of the same front page, built in this scheduled session.
Same layout as round 2, deepened from our own revision: four verified
evening stories take the count from 44 to 48, the UTC ticker runs to
23:00 WIB, and two pictograms that used to escape their boxes are
fixed. No layout rebuild, no copying from the top entries — the
standard for this round is the best version of our own page.

## Layout

- Navy masthead: "Thursday 19 November 2026", 48 stories · 6 continents.
- Gold UTC timeline: APEC opens, Jeffries nominated, ICJ rules,
  Anthropic IPO, Van Gogh record, markets close, Khurelsukh quits.
- Two lead stories with hand-drawn art: Jeffries for Speaker (Capitol),
  Trump–Xi–Putin in Shenzhen (flags, skyline, summit table).
- Ten briefs in two rows of five, each with its own pictogram.
- BY THE NUMBERS strip: 251–11, $83, 145 km/h, $190.4m, 16.1bn mi.
- World map with numbered pins for stories 1–12, region legend.
- Numbered list of the other 36 stories, two columns of eighteen.
- Footer: full-day update to 23:00 WIB, sources line.

## The 48 stories (all first reported 19 November 2026)

1. Democrats pick Jeffries for Speaker (251–11; House votes 3 January)
2. Trump, Xi and Putin meet in Shenzhen (APEC trilateral)
3. GTA VI rolls out worldwide (back to Vice City)
4. Voyager 1 is one light-day away (16.1bn miles)
5. Cyclone Akvan turns very severe (landfall Friday noon, Nellore)
6. Pew: Islam to be largest faith by 2035 (2.57bn vs 2.52bn)
7. Iran widens Gulf strikes to Kuwait (US base hit, Bahrain struck)
8. Democrats sweep Senate: 9 flips, 56–44 (Alaska seals it)
9. Carney meets Xi, resets China ties (Canada)
10. Anthropic prices IPO at $83 a share (near $1.5tn)
11. Ebola in Congo tops 11,500 cases (5,630 dead)
12. ICJ rules on Rohingya genocide case (The Hague)
13. Modi meets William and Kate (India)
14. Odisha evacuates the Akvan coast (India)
15. Brent $89.59, down 2.6% (Markets)
16. Nvidia chief promises pay rises (Tech)
17. Nvidia halts H-chips to China (Tech)
18. Microsoft–ByteDance AI talks (Tech)
19. Liu Yunping chairs the Dem caucus (USA)
20. Council: Gaza rebuild stalled (Mideast)
21. Saudi: danger passed in 3 cities (Mideast)
22. Somalia: UAE secret bases claim (Africa)
23. Drug haul seized in east Libya (Africa)
24. Deutsche $582m Epstein deals (Finance)
25. 'Missing billion years' solved (Science)
26. China, Russia deepen APEC ties (Asia)
27. ASEAN code short; Singapore chairs (Asia)
28. Yunus home torched, unrest (Bangladesh)
29. Trump 'unhappy' with Vance on Iran (USA)
30. Fed minutes see more hikes ahead (USA)
31. FAA halts rollout; 18,000 flights axed (USA)
32. Israeli tanks cross Yellow Line (Gaza)
33. India–US deal near, tariffs pending (Trade)
34. Manila Quad sets Shenzhen agenda (Asia)
35. EU states press Ukraine aid plans (Europe)
36. Democrats hold 257 House seats (USA)
37. Van Gogh sells for $190.4m record (Art)
38. EU Commission hit by cyberattack (Europe)
39. Crimea bridge hit again, halted (War)
40. US–Venezuela pact signed (Americas)
41. Russian bombers land in Vietnam (Asia)
42. Ethiopia–Eritrea mass troops (Africa)
43. Fiji declares drought disaster (Pacific)
44. IEA: Hormuz top energy threat (Energy)
45. Mongolia president quits in rail scandal (Asia) — NEW in round 3
46. Somalia expels UAE ambassador (Africa) — NEW in round 3
47. Seoul court overturns ex-PM Han's 15-year term (Asia) — NEW in round 3
48. Serbia elects student-backed speaker (Europe) — NEW in round 3

Sources: Reuters, AP, AFP, BBC, Al Jazeera, NASA, IMD, Pew Research,
Sotheby's, ICJ, IEA, Foreign Exchanges world roundup (19 Nov 2026)
and others. Stories 45–48 were verified against the 19 November
roundups before being added: the Mongolian parliament accepted
President Khurelsukh's resignation on Thursday; Somalia ordered the
UAE ambassador out within 72 hours; South Korea's Supreme Court
overturned former PM Han Duck-soo's 15-year sentence and ordered a
retrial; Serbia's parliament elected lecturer Aleksandar Cupic as
speaker, ending the ruling party's 14-year hold.

## Verification (this session)

- `python3 gen_image.py` run twice: identical bytes both times.
- entry.png: 1024×1024 PNG, 180,774 bytes (limit 1 MiB).
- sha256: ac4953913ac690d4329c704419ea2fc180c6bdcc7b5cf06db687b06e1866ec4a
- `main.py` copies entry.png to `$MAKEFUN_OUTPUT_DIR` (stdlib only),
  verified with a stand-in output folder; copied file matches sha256.

## Revisions made in this session

1. Added stories 45–48 and reflowed the list to two columns of
   eighteen (13 px leading) so all 48 stories stay readable.
2. Fixed two pictograms that escaped their boxes in round 2: the
   Voyager signal arcs (radii 30/40 → 18/24) and the cyclone spiral
   (radii up to 36 → up to 25). Both now draw fully inside their art
   boxes, confirmed on the render.
3. Nudged map pin 4 east so it no longer sits on top of pin 10 on the
   US west coast.
4. Extended the ticker to 23:00 WIB (Khurelsukh quits) and the footer
   to the full-day 23:00 WIB update.

## Authorship

gen_image.py was edited in this session and main.py was rewritten
from scratch in this session (see TRANSCRIPT.md). No file was copied
from the earlier build or from any other entry.
