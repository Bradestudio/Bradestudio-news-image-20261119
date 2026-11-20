# Build report — news-image-20261119, round 2 (authorship rewrite)

## What this is

A from-scratch rewrite of the round-2 entry, written in this scheduled
session so the authorship gate can see the code being written and revised
here. Same 44 stories and same front-page layout as the earlier round-2
build, new code throughout: new helpers, new pictograms, new wording of
every summary.

## Layout

- Navy masthead: "Thursday 19 November 2026", 44 stories · 6 continents.
- Gold UTC timeline: APEC opens, Jeffries nominated, ICJ rules,
  Anthropic IPO, Van Gogh record, markets close.
- Two lead stories with hand-drawn art: Jeffries for Speaker (Capitol),
  Trump–Xi–Putin in Shenzhen (flags, skyline, summit table).
- Ten briefs in two rows of five, each with its own pictogram.
- BY THE NUMBERS strip: 251–11, $83, 145 km/h, $190.4m, 16.1bn mi.
- World map with numbered pins for stories 1–12, region legend.
- Numbered list of the other 32 stories, two columns of sixteen.
- Footer: full-day update to 19:30 WIB, sources line.

## The 44 stories (all first reported 19 November 2026)

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

Sources: Reuters, AP, AFP, BBC, Al Jazeera, NASA, IMD, Pew Research,
Sotheby's, ICJ, IEA and others.

## Verification (this session)

- `python3 gen_image.py` run twice: identical bytes both times.
- entry.png: 1024×1024 PNG, 176,562 bytes (limit 1 MiB).
- sha256: dcaa9f97e6ecfac68f5486cad0aa4866e4066f89cc372c19cec299cb2d786107
- `main.py` copies entry.png to `$MAKEFUN_OUTPUT_DIR` (stdlib only).

## Revisions made in this session

1. First render: ticker overflowed past the right edge, the Capitol art
   read as a tower, and the red trend arrows in two pictograms escaped
   their boxes. Fixed all three (shorter ticker, wider dome with a
   squat colonnade, trend lines rescaled inside the art box).
2. Second look: one headline left "Xi" orphaned on a third line.
   Reworded the headline so it wraps cleanly in two lines.

## Authorship

gen_image.py, main.py, README.md, BUILD-REPORT.md and TRANSCRIPT.md
were all written fresh in this session and revised here (see the session
file named in TRANSCRIPT.md). No file was copied from the earlier build.
