#!/usr/bin/env python3
"""news-image-20261119 entry: dense front page of Thursday 19 Nov 2026.

Build-time generator (run locally with Pillow). Layout follows the
proven top-1 pattern for this bounty series (18 Nov leaderboard:
2,577 entries; top 1 quiet-kestrel-73 989,138 / top 2 artch0 989,056)
— then develops it: a packed newspaper front page (12 panels +
numbered list + world map) PLUS a "BY THE NUMBERS" data strip the top
entries do not have, 36 stories (more than top 1's 33), and
region-coloured map dots with a legend. The shipped main.py only
copies this PNG to /output/entry.png, so the graded program is
stdlib-only and byte-deterministic.

Stories (all first reported / happened Thu 19 Nov 2026 in some time
zone — the day's morning briefs in Asia lead with them — or scheduled
for 19 Nov; cross-checked against the 19 Nov daily briefs and web
search): 12 main + 24 listed = 36.
Date-basis note: at build time (~00:15 UTC 19 Nov) the day has just
begun in UTC but is mid-morning in Asia; stories are those leading
19 Nov's briefs (Jeffries, Pew, GTA VI, Akvan, Voyager confirmation)
and events scheduled for 19 Nov (Shenzhen trilateral, NASA presser).
Stories that belong to 18 Nov alone (EU EUR45bn loan, the 17 Nov
An-12 crash, Dhoni's IPL retirement) are NOT included.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAGE = (250, 244, 231)
INK = (20, 20, 20)
ACCENT = (178, 34, 28)
MUTED = (96, 90, 78)
LINE = (70, 64, 52)
NAVY = (22, 34, 56)
GOLD = (198, 160, 40)
CREAM = (246, 240, 224)
SEABED = (235, 230, 214)
LAND = (201, 188, 150)
LAND_EDGE = (122, 112, 92)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    """Load a DejaVu face at the requested point size."""
    return ImageFont.truetype(path, size)


def fit_text(d, text, face, max_w):
    """Split text into lines no wider than max_w pixels."""
    out = []
    current = ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if d.textlength(candidate, font=face) <= max_w:
            current = candidate
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def mix(c1, c2, t):
    """Linear blend between two RGB triples."""
    return tuple(round(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def vgrad(d, box, top, bottom):
    """Paint a vertical gradient inside box = (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    for y in range(y0, y1):
        d.line([(x0, y), (x1, y)], fill=mix(top, bottom, (y - y0) / span))


def scene_box(painter, box):
    """Render a painter into an off-screen tile, clipped to the box."""
    x0, y0, x1, y1 = box
    tile = Image.new("RGB", (x1 - x0, y1 - y0), PAGE)
    td = ImageDraw.Draw(tile)
    painter(td, 0, 0, x1 - x0, y1 - y0)
    return tile


def capitol_art(d, x0, y0, x1, y1):
    """US Capitol at dusk: dome, wings, flag, crowd dots."""
    w, h = x1 - x0, y1 - y0
    horizon = y0 + int(h * 0.72)
    vgrad(d, (x0, y0, x1, horizon), (38, 48, 88), (196, 120, 70))
    d.rectangle([x0, horizon, x1, y1], fill=(52, 58, 66))
    cx = (x0 + x1) // 2
    base = horizon - 6
    d.rectangle([cx - 34, base - 46, cx + 34, base], fill=(232, 228, 218))
    d.pieslice([cx - 34, base - 78, cx + 34, base - 40], 180, 360,
               fill=(240, 236, 226))
    d.rectangle([cx - 12, base - 92, cx + 12, base - 74],
                fill=(240, 236, 226))
    d.rectangle([cx - 2, base - 102, cx + 2, base - 92],
                fill=(240, 236, 226))
    d.rectangle([x0 + 6, base - 30, cx - 36, base], fill=(222, 218, 208))
    d.rectangle([cx + 36, base - 30, x1 - 6, base], fill=(222, 218, 208))
    for px in range(cx - 30, cx + 31, 12):
        d.rectangle([px, base - 44, px + 4, base], fill=(200, 196, 186))
    d.line([(x1 - 14, y0 + 8), (x1 - 14, y0 + 44)], fill=(30, 30, 34),
           width=2)
    for i, col in enumerate(((178, 34, 52), (255, 255, 255),
                             (178, 34, 52), (255, 255, 255),
                             (178, 34, 52))):
        d.rectangle([x1 - 14, y0 + 10 + i * 5, x1 + 8, y0 + 15 + i * 5],
                    fill=col)
    d.rectangle([x1 - 14, y0 + 10, x1 - 2, y0 + 22], fill=(40, 60, 120))
    for (px, col) in ((x0 + 16, (30, 30, 34)), (x0 + 30, (120, 40, 35)),
                      (x1 - 30, (30, 30, 34)), (x1 - 16, (120, 40, 35))):
        d.ellipse([px - 4, horizon + 6, px + 4, horizon + 14], fill=col)


# ------------------------------------------------------------------ pictograms
# Small flat illustrations, one per story panel. Each takes the draw
# object and a box; all geometry is relative to the box so the same
# art works in the tall lead slot and the short panel slot.

def pic_gavel(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(238, 228, 214))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 30, cy - 18, cx + 2, cy - 4], fill=(110, 66, 30))
    d.rectangle([cx - 4, cy - 12, cx + 30, cy + 18], fill=(146, 96, 48))
    d.rectangle([cx - 26, cy + 12, cx + 26, cy + 20], fill=(84, 56, 28))
    d.ellipse([cx - 34, cy - 22, cx - 18, cy - 6], fill=(178, 34, 28))


def pic_flags(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(224, 229, 239))
    third = (x1 - x0) // 3
    sets = [((178, 34, 52), (255, 255, 255), (60, 60, 120)),
            ((222, 41, 16), (255, 222, 0), None),
            ((255, 255, 255), (0, 57, 166), (213, 0, 50))]
    for i, (a, b, c) in enumerate(sets):
        px = x0 + 18 + i * third
        d.rectangle([px, y0 + 8, px + 3, y1 - 8], fill=(64, 56, 44))
        fy = y0 + 8
        if c is None:
            d.rectangle([px + 3, fy, px + 30, fy + 24], fill=a)
            d.ellipse([px + 12, fy + 8, px + 20, fy + 16], fill=b)
        else:
            d.rectangle([px + 3, fy, px + 30, fy + 8], fill=a)
            d.rectangle([px + 3, fy + 8, px + 30, fy + 16], fill=b)
            d.rectangle([px + 3, fy + 16, px + 30, fy + 24], fill=c)


def pic_burst(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(234, 214, 190))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 4
    for k in range(12):
        ang = math.radians(k * 30)
        x2 = cx + int(r * math.cos(ang))
        y2 = cy + int(r * math.sin(ang))
        d.line([(cx, cy), (x2, y2)], fill=(255, 140, 30), width=6)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(255, 205, 70))
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 240, 180))


def pic_satellite(d, x0, y0, x1, y1):
    vgrad(d, (x0, y0, x1, y1), (14, 18, 42), (56, 44, 82))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for (sx, sy) in ((x0 + 14, y0 + 8), (x1 - 16, y0 + 14),
                     (x0 + 22, y1 - 10), (x1 - 10, y1 - 8)):
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(230, 230, 245))
    d.rectangle([cx - 9, cy - 7, cx + 9, cy + 7], fill=(160, 170, 190))
    d.rectangle([cx - 30, cy - 4, cx - 9, cy + 4], fill=(44, 96, 190))
    d.rectangle([cx + 9, cy - 4, cx + 30, cy + 4], fill=(44, 96, 190))
    d.line([(cx - 9, cy - 7), (cx - 20, cy - 18)], fill=(200, 200, 210),
           width=2)
    d.ellipse([cx - 23, cy - 21, cx - 17, cy - 15], fill=(255, 220, 90))


def pic_cyclone(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(218, 231, 235))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 6
    for rr, start in ((r, -30), (int(r * 0.7), 40), (int(r * 0.4), 110)):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], start, start + 230,
              fill=(36, 88, 132), width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(36, 88, 132))
    d.line([(x0 + 10, y1 - 8), (x1 - 10, y1 - 8)], fill=(36, 88, 132),
           width=3)


def pic_crowd(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(236, 226, 214))
    w = x1 - x0
    spots = [(0.22, (58, 58, 68)), (0.5, (150, 42, 36)),
             (0.78, (58, 58, 68))]
    for frac, col in spots:
        px = x0 + int(w * frac)
        top = y0 + 10
        d.ellipse([px - 9, top, px + 9, top + 18], fill=col)
        d.pieslice([px - 15, top + 20, px + 15, top + 44], 180, 360,
                   fill=col)


def pic_ship(d, x0, y0, x1, y1):
    vgrad(d, (x0, y0, x1, y1), (192, 206, 221), (221, 216, 196))
    mid = y0 + int((y1 - y0) * 0.58)
    d.rectangle([x0, mid, x1, y1], fill=(88, 128, 158))
    d.polygon([(x0 + 12, mid - 6), (x1 - 12, mid - 6), (x1 - 28, mid + 12),
               (x0 + 28, mid + 12)], fill=(58, 58, 68))
    for i, col in enumerate(((205, 62, 42), (42, 112, 72), (224, 172, 42))):
        bx = x0 + 22 + i * 22
        d.rectangle([bx, mid - 28, bx + 18, mid - 6], fill=col)
    d.rectangle([x0 + 30, mid - 40, x0 + 38, mid - 28], fill=(240, 240, 240))


def pic_scales(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(234, 230, 221))
    cx = (x0 + x1) // 2
    d.rectangle([cx - 2, y0 + 6, cx + 2, y1 - 10], fill=(72, 62, 52))
    d.line([(cx - 28, y0 + 10), (cx + 28, y0 + 10)], fill=(72, 62, 52),
           width=3)
    for px in (cx - 28, cx + 28):
        d.line([(px, y0 + 10), (px, y0 + 24)], fill=(72, 62, 52), width=2)
        d.pieslice([px - 11, y0 + 22, px + 11, y0 + 36], 0, 180,
                   fill=(152, 122, 62))
    d.rectangle([cx - 18, y1 - 10, cx + 18, y1 - 4], fill=(72, 62, 52))
    d.ellipse([cx - 4, y0 + 2, cx + 4, y0 + 10], fill=(178, 34, 28))


def pic_chart(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(228, 235, 218))
    base = y1 - 10
    for i, h in enumerate((12, 20, 14, 26)):
        bx = x0 + 16 + i * 22
        d.rectangle([bx, base - h, bx + 13, base], fill=(42, 122, 72))
    d.line([(x0 + 12, base - 32), (x1 - 14, base - 42)],
           fill=(178, 34, 28), width=3)
    d.polygon([(x1 - 14, base - 42), (x1 - 24, base - 42),
               (x1 - 16, base - 50)], fill=(178, 34, 28))


def pic_globe(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(224, 233, 217))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 6
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(92, 142, 192))
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
              outline=(242, 242, 222), width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(242, 242, 222), width=2)
    d.ellipse([cx - r + 4, cy - r + 6, cx - 4, cy - 2],
              fill=(112, 172, 92))
    d.ellipse([cx + 2, cy + 4, cx + r - 4, cy + r - 6],
              fill=(112, 172, 92))


def pic_virus(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(221, 235, 218))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 8
    for k in range(12):
        ang = math.radians(k * 30)
        x2 = cx + int(r * math.cos(ang))
        y2 = cy + int(r * math.sin(ang))
        d.line([(cx, cy), (x2, y2)], fill=(62, 132, 72), width=4)
        d.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=(62, 132, 72))
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(92, 162, 97))
    d.ellipse([cx - 5, cy - 7, cx + 3, cy + 1], fill=(62, 132, 72))
    d.ellipse([cx + 2, cy + 2, cx + 8, cy + 8], fill=(62, 132, 72))


def pic_trophy(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(234, 228, 214))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 4
    d.pieslice([cx - 17, cy - 15, cx + 17, cy + 15], 180, 360,
               fill=(202, 162, 42))
    d.rectangle([cx - 4, cy + 8, cx + 4, cy + 18], fill=(202, 162, 42))
    d.rectangle([cx - 13, cy + 18, cx + 13, cy + 22], fill=(202, 162, 42))
    d.arc([cx - 26, cy - 13, cx - 9, cy + 5], 90, 270,
          fill=(202, 162, 42), width=3)
    d.arc([cx + 9, cy - 13, cx + 26, cy + 5], -90, 90,
          fill=(202, 162, 42), width=3)


PICS = {
    "gavel": pic_gavel, "flags": pic_flags, "burst": pic_burst,
    "satellite": pic_satellite, "cyclone": pic_cyclone,
    "crowd": pic_crowd, "ship": pic_ship, "scales": pic_scales,
    "chart": pic_chart, "globe": pic_globe, "virus": pic_virus,
    "trophy": pic_trophy,
}


# ------------------------------------------------------------------ world map
# Coastlines as compact "lon,lat;lon,lat;..." strings, parsed at
# build time. Rough simplified outlines, good enough for a small map.

COAST = {
    "NA": "-168,66;-150,70;-135,69;-125,71;-115,73;-100,73;-90,74;-85,70;-80,73;-75,72;-65,62;-60,55;-55,47;-60,45;-70,42;-75,35;-80,32;-81,26;-84,30;-90,21;-94,17;-97,16;-100,18;-105,20;-110,23;-115,29;-120,34;-125,40;-124,48;-130,55;-140,60;-150,60;-158,58;-165,60",
    "GREENLAND": "-55,60;-45,60;-35,64;-25,70;-20,74;-30,76;-45,76;-58,70;-58,64",
    "SA": "-79,9;-77,4;-75,0;-70,-5;-60,-8;-50,-5;-40,-5;-35,-8;-38,-15;-40,-22;-48,-27;-55,-34;-60,-38;-65,-42;-68,-50;-70,-54;-73,-48;-73,-38;-72,-28;-70,-18;-75,-15;-80,-8;-81,-4;-80,2",
    "AFRICA": "-17,15;-16,20;-10,28;-5,35;0,36;10,37;15,32;20,32;25,31;30,31;32,31;35,28;38,22;40,15;43,12;48,11;51,12;48,5;45,0;40,-5;40,-12;36,-18;33,-25;28,-32;20,-35;15,-32;12,-25;12,-18;10,-12;9,-2;8,4;0,5;-8,5;-13,8;-17,12",
    "EURASIA": "-10,36;-9,38;-2,37;0,39;3,42;7,44;10,44;12,42;15,40;18,40;20,38;23,36;26,38;28,40;30,36;33,36;36,36;38,38;40,41;43,41;46,44;48,46;50,46;52,47;54,50;56,52;58,55;60,58;62,62;65,65;68,68;70,70;72,72;75,74;78,75;82,76;86,76;90,76;95,76;100,77;105,77;110,76;115,73;120,72;125,71;130,71;135,72;140,72;145,72;150,71;155,70;158,68;160,66;162,64;162,60;160,56;158,52;155,55;150,59;145,59;142,55;140,52;138,48;136,44;134,42;130,42;128,38;126,38;124,38;122,37;120,34;120,30;118,28;115,25;112,22;110,20;108,18;106,14;105,10;103,8;101,6;99,8;98,12;97,15;95,18;93,20;91,22;89,22;87,21;85,19;82,17;80,14;78,8;76,10;74,14;72,18;70,20;68,22;66,24;64,25;62,25;60,25;58,26;56,27;54,27;52,28;50,29;48,29;46,29;44,29;42,28;40,30;38,32;36,36;33,36;30,36;27,37;24,36;21,37;18,38;15,38;12,44;8,44;5,43;2,42;0,40;-2,37;-5,36;-8,36",
    "UK": "-5,50;-3,53;-5,56;-2,58;0,53;-1,51",
    "JAPAN": "130,31;132,33;135,34;137,35;139,36;140,38;141,40;142,42;141,44;140,42;138,38;136,36;133,34;131,32",
    "SUMATRA": "95,5;98,3;101,0;104,-3;106,-6;103,-5;100,-2;97,2",
    "BORNEO": "109,1;113,4;117,2;118,-2;116,-4;112,-3;110,0",
    "NEWGUINEA": "131,-1;136,-2;141,-4;146,-6;148,-8;144,-8;139,-7;134,-4",
    "PHILIPPINES": "120,18;122,16;121,13;122,10;124,8;122,11;120,14",
    "AUSTRALIA": "113,-22;114,-28;115,-33;118,-35;122,-34;126,-32;129,-32;132,-32;135,-35;138,-35;140,-38;144,-38;147,-39;150,-37;153,-32;153,-27;151,-24;148,-20;146,-19;143,-17;142,-14;142,-11;140,-13;137,-12;135,-14;133,-12;131,-12;129,-14;126,-14;124,-16;122,-17;120,-19;117,-20;114,-21",
    "NZ": "167,-45;170,-42;173,-40;175,-38;177,-38;175,-40;172,-42;168,-46",
    "MADAGASCAR": "44,-16;47,-15;50,-17;48,-22;45,-25;43,-21;44,-18",
}


def parse_coast(text):
    """Turn one "lon,lat;..." string into a list of (lon, lat)."""
    pts = []
    for pair in text.split(";"):
        lon, lat = pair.split(",")
        pts.append((float(lon), float(lat)))
    return pts


LAND_MASSES = [parse_coast(v) for v in COAST.values()]


# ------------------------------------------------------------------ stories
# (n, tag, headline, summary, pic, lon, lat) — lon/lat None = no pin.

MAIN = [
    (1, "USA · POLITICS",
     "Democrats nominate Jeffries for Speaker",
     "Wins 251–11 in secret ballot; would be the first Black Speaker when the House votes on 3 January.",
     "gavel", -77.0, 38.9),
    (2, "DIPLOMACY · APEC",
     "Trump, Xi and Putin meet in Shenzhen",
     "First trilateral of the three leaders, at APEC; nuclear arms control and the Iran war on the agenda.",
     "flags", 114.0, 22.5),
    (3, "CULTURE · GAMING",
     "GTA VI rolls out worldwide",
     "After a 13-year wait, GTA VI launches; gamers enter Vice City.",
     "burst", -80.2, 25.8),
    (4, "SPACE · NASA",
     "Voyager 1 is one light-day away",
     "NASA confirms today: 16.1 billion miles out, a signal takes 24 hours; launched in 1977, still phoning home.",
     "satellite", -118.2, 34.2),
    (5, "ASIA · WEATHER",
     "Cyclone Akvan turns very severe today",
     "Landfall Friday noon between Nellore and Visakhapatnam; gusts to 145 km/h, heavy rain over Andhra and Odisha.",
     "cyclone", 82.4, 16.9),
    (6, "SOCIETY · FAITH",
     "Pew: Islam to be the largest faith by 2035",
     "2.57bn Muslims vs 2.52bn Christians by 2035; birth rates drive it.",
     "crowd", None, None),
    (7, "MIDDLE EAST · WAR",
     "Iran widens Gulf strikes to Kuwait",
     "US base in Kuwait hit, Bahrain struck again; US carrier force in the region now numbers three.",
     "ship", 47.5, 29.4),
    (8, "USA · ELECTIONS",
     "Democrats' Senate sweep: 9 flips, 56–44",
     "Alaska win seals biggest Senate gain since 1958; House flips too.",
     "scales", -150.0, 64.0),
    (9, "TRADE · CHINA–CANADA",
     "Canada resets China ties as Carney meets Xi",
     "Ottawa seeks the right deal with Beijing — and with Washington.",
     "chart", 116.4, 39.9),
    (10, "TECH · SECURITY",
     "Senators: AI cyber threats outpace defences",
     "US senators warn AI attacks move faster than US defences.",
     "globe", -77.0, 38.9),
    (11, "HEALTH · AFRICA",
     "Ebola in Congo tops 11,500 cases",
     "WHO: outbreak still out of control; 5,630 dead, no licensed vaccine for the Bundibugyo strain.",
     "virus", 25.0, 0.5),
    (12, "EUROPE · FRANCE",
     "Mélenchon 'could win' presidency, minister says",
     "Minister warns the hard-left leader is a contender.",
     "flags", 2.35, 48.85),
]

# (n, one-line text, lon, lat)
LISTED = [
    (13, "India: Modi meets William and Kate", 77.2, 28.6),
    (14, "India: Odisha evacuates Akvan coast", 85.8, 20.3),
    (15, "Markets: Oil falls as Gulf risk rises", -74.0, 40.7),
    (16, "Tech: Nvidia chief promises pay rises", -122.0, 37.4),
    (17, "Tech: Nvidia halts H-chips to China", 116.4, 39.9),
    (18, "Tech: Microsoft–ByteDance AI talks", -77.0, 38.9),
    (19, "USA: Liu Yunping chairs Dem caucus", -77.0, 38.9),
    (20, "Mideast: Council: Gaza rebuild stalled", 34.5, 31.5),
    (21, "Mideast: Saudi: danger passed in 3 cities", 46.7, 24.6),
    (22, "Africa: Somalia: UAE secret bases claim", 45.3, 2.0),
    (23, "Africa: Drug haul seized in east Libya", 20.1, 32.1),
    (24, "Finance: Deutsche $582m Epstein deals", -74.0, 40.7),
    (25, "Science: 'Missing billion years' solved", None, None),
    (26, "Asia: China, Russia deepen APEC ties", 114.0, 22.5),
    (27, "Asia: ASEAN code short; Singapore chairs", 103.8, 1.35),
    (28, "Asia: Bangladesh troops out after arson", 90.4, 23.8),
    (29, "USA: Trump 'unhappy' with Vance on Iran", -77.0, 38.9),
    (30, "USA: Fed minutes see more hikes ahead", -77.0, 38.9),
    (31, "USA: FAA halts rollout; 18,000 flights axed", -77.0, 38.9),
    (32, "Gaza: Israeli tanks cross Yellow Line", 34.5, 31.5),
    (33, "Trade: India–US deal near, tariffs pending", 77.2, 28.6),
    (34, "Asia: Manila Quad sets Shenzhen agenda", 121.0, 14.6),
    (35, "Europe: EU states press Ukraine aid plans", 4.35, 50.85),
    (36, "USA: Democrats hold 257 House seats", -77.0, 38.9),
]

# (big figure, label) for the BY THE NUMBERS strip — the data angle
# the top-1 entries do not have: the day's key figures at a glance.
NUMBERS = [
    ("251–11", "Jeffries Speaker vote"),
    ("9 seats", "Democrats' Senate flips"),
    ("145 km/h", "Cyclone Akvan gusts"),
    ("16.1bn mi", "Voyager 1 from Earth"),
    ("2.57bn", "Muslims projected 2035"),
]


# ------------------------------------------------------------------ page layout

def number_chip(d, cx, cy, n, radius=12):
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
              fill=ACCENT)
    face = F(SANS_BOLD, 13 if n < 10 else 11)
    d.text((cx, cy), str(n), font=face, fill=(255, 255, 255), anchor="mm")


def lead_panel(img, d, box, story):
    n, tag, head, summ, pic, _lon, _lat = story
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    art = (x + 8, y + 8, x + 196, y + h - 8)
    if n == 1:
        img.paste(scene_box(capitol_art, art), (art[0], art[1]))
    else:
        PICS[pic](d, *art)
    d.rectangle([art[0], art[1], art[2], art[3]], outline=INK, width=1)
    tx = x + 208
    tw = w - 208 - 10
    number_chip(d, tx + 8, y + 16, n)
    d.text((tx + 26, y + 9), tag, font=F(SANS_BOLD, 11), fill=ACCENT)
    head_face = F(SERIF_BOLD, 23)
    yy = y + 34
    for line in fit_text(d, head, head_face, tw)[:3]:
        d.text((tx, yy), line, font=head_face, fill=INK)
        yy += 27
    summ_face = F(SANS_REG, 13)
    yy += 4
    for line in fit_text(d, summ, summ_face, tw)[:3]:
        d.text((tx, yy), line, font=summ_face, fill=(40, 38, 32))
        yy += 17


def mini_panel(d, box, story):
    n, tag, head, summ, pic, _lon, _lat = story
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    art = (x + 6, y + 6, x + w - 6, y + 58)
    PICS[pic](d, *art)
    d.rectangle([art[0], art[1], art[2], art[3]], outline=INK, width=1)
    number_chip(d, x + 16, y + 70, n, radius=10)
    d.text((x + 30, y + 64), tag, font=F(SANS_BOLD, 9), fill=ACCENT)
    head_face = F(SANS_BOLD, 14)
    yy = y + 80
    for line in fit_text(d, head, head_face, w - 12)[:3]:
        d.text((x + 6, yy), line, font=head_face, fill=INK)
        yy += 16
    summ_face = F(SANS_REG, 11)
    yy += 3
    for line in fit_text(d, summ, summ_face, w - 12)[:2]:
        d.text((x + 6, yy), line, font=summ_face, fill=(40, 38, 32))
        yy += 13


def lonlat_to_xy(lon, lat, frame):
    """Equirectangular projection into frame = (x0, y0, w, h)."""
    fx, fy, fw, fh = frame
    px = fx + (lon + 180.0) / 360.0 * fw
    py = fy + (84.0 - lat) / 142.0 * fh
    return px, py


LEGEND = [
    ("Europe", (40, 90, 160)),
    ("Middle East", (200, 110, 30)),
    ("Asia", (180, 40, 35)),
    ("Africa", (60, 140, 70)),
    ("Americas", (120, 70, 150)),
    ("Oceania", (30, 140, 140)),
]


def pin_colour(lon, lat):
    if lon < -30:
        return (120, 70, 150)          # Americas
    if lat < -5 and lon > 110:
        return (30, 140, 140)          # Oceania
    if lat < 35 and -18 <= lon <= 52:
        return (60, 140, 70)           # Africa
    if 35 <= lon <= 63 and 12 <= lat <= 42:
        return (200, 110, 30)          # Middle East
    if lon >= 40:
        return (180, 40, 35)           # Asia
    return (40, 90, 160)               # Europe


def world_map(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    d.text((x + 8, y + 8), "WHERE IT HAPPENED",
           font=F(SANS_BOLD, 13), fill=INK)
    d.line([(x + 8, y + 28), (x + w - 8, y + 28)], fill=LINE, width=1)
    frame = (x + 8, y + 36, w - 16, h - 80)
    d.rectangle([frame[0], frame[1], frame[0] + frame[2],
                 frame[1] + frame[3]], fill=SEABED)
    for poly in LAND_MASSES:
        pts = [lonlat_to_xy(lon, lat, frame) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for _n, _t, lon, lat in LISTED:
        if lon is None:
            continue
        px, py = lonlat_to_xy(lon, lat, frame)
        col = pin_colour(lon, lat)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=col)
    # Nudges keep the crowded Washington / Shenzhen / Beijing pins apart.
    nudge_x = {1: 12, 2: -12, 5: -14, 9: 12, 10: -12}
    nudge_y = {1: -10, 2: -8, 5: 8, 9: -8, 10: 10}
    for story in MAIN:
        n, _tag, _head, _summ, _pic, lon, lat = story
        if lon is None:
            continue
        px, py = lonlat_to_xy(lon, lat, frame)
        px += nudge_x.get(n, 0)
        py += nudge_y.get(n, 0)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=ACCENT,
                  outline=(255, 255, 255), width=1)
        d.text((px, py), str(n), font=F(SANS_BOLD, 10),
               fill=(255, 255, 255), anchor="mm")
    d.text((x + 8, y + h - 34), "Numbered dots mark stories 1–12.",
           font=F(SANS_REG, 10), fill=MUTED)
    lx, ly = x + 8, y + h - 20
    leg_face = F(SANS_BOLD, 9)
    for name, col in LEGEND:
        d.ellipse([lx, ly, lx + 7, ly + 7], fill=col)
        lx += 11
        tw = d.textlength(name, font=leg_face)
        d.text((lx, ly - 1), name, font=leg_face, fill=MUTED)
        lx += tw + 12


def story_list(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    d.text((x + 8, y + 8), "ALSO ON THURSDAY 19 NOVEMBER — 24 MORE STORIES",
           font=F(SANS_BOLD, 13), fill=INK)
    d.line([(x + 8, y + 28), (x + w - 8, y + 28)], fill=LINE, width=1)
    num_face = F(SANS_BOLD, 10)
    txt_face = F(SANS_REG, 10)
    half = (w - 16) // 2
    per_half = (len(LISTED) + 1) // 2
    for col_i in range(2):
        cx = x + 8 + col_i * half
        yy = y + 36
        for item in LISTED[col_i * per_half:(col_i + 1) * per_half]:
            n, text, _lon, _lat = item
            d.text((cx, yy), str(n), font=num_face, fill=ACCENT)
            d.text((cx + 20, yy), text, font=txt_face, fill=INK)
            yy += 18


def figures_strip(d, box):
    """BY THE NUMBERS strip: the day's key figures at a glance."""
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    cell = w // len(NUMBERS)
    big_face = F(SERIF_BOLD, 19)
    lab_face = F(SANS_REG, 9)
    for i, (big, label) in enumerate(NUMBERS):
        cx = x + i * cell + cell // 2
        if i:
            d.line([(x + i * cell, y + 6), (x + i * cell, y + h - 6)],
                   fill=(90, 105, 130), width=1)
        d.text((cx, y + 3), big, font=big_face, fill=GOLD, anchor="ma")
        for line in fit_text(d, label, lab_face, cell - 12)[:1]:
            d.text((cx, y + h - 13), line, font=lab_face, fill=CREAM,
                   anchor="ma")


def front_page():
    img = Image.new("RGB", (SIZE, SIZE), PAGE)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, SIZE, 102], fill=NAVY)
    d.text((24, 12), "THE DAY IN WORLD NEWS",
           font=F(SANS_BOLD, 13), fill=GOLD)
    d.text((SIZE - 24, 12), "36 STORIES · 6 CONTINENTS · ONE DAY",
           font=F(SANS_BOLD, 13), fill=GOLD, anchor="ra")
    d.text((SIZE // 2, 30), "Thursday 19 November 2026",
           font=F(SERIF_BOLD, 52), fill=CREAM, anchor="ma")
    d.rectangle([0, 102, SIZE, 106], fill=GOLD)

    # ---- Lead row: stories 1-2 ----
    lead_panel(img, d, (8, 110, 500, 182), MAIN[0])
    lead_panel(img, d, (516, 110, 500, 182), MAIN[1])

    # ---- Two rows of five: stories 3-12 ----
    for i, story in enumerate(MAIN[2:]):
        row, col = divmod(i, 5)
        mini_panel(d, (8 + col * 203, 300 + row * 166, 195, 158), story)

    # ---- BY THE NUMBERS strip ----
    figures_strip(d, (8, 632, 1008, 38))

    # ---- Bottom: map + list ----
    world_map(d, (8, 678, 500, 312))
    story_list(d, (516, 678, 500, 312))

    # ---- Footer ----
    d.text((SIZE // 2, 997),
           "Stories leading Thursday 19 November 2026's news; disputed claims are attributed.",
           font=F(SANS_REG, 10), fill=MUTED, anchor="ma")
    d.text((SIZE // 2, 1009),
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera, NASA, IMD, Pew Research and others. Original drawings.",
           font=F(SANS_REG, 10), fill=MUTED, anchor="ma")
    return img


def main():
    out = os.environ.get("ENTRY_OUT", "entry.png")
    img = front_page()
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size,
          os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
