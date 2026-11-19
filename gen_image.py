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

W = H = 1024
PAPER = (248, 243, 230)
INK = (17, 17, 17)
RED = (179, 38, 30)
GREY = (90, 86, 76)
RULE = (60, 56, 48)
NAVY = (20, 32, 54)
GOLD = (201, 162, 39)
CREAM = (244, 238, 222)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines fitting `width` px."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def clip_scene(scene_fn, x0, y0, x1, y1):
    """Draw a scene into a temp image so nothing spills past its panel."""
    w, h = x1 - x0, y1 - y0
    tmp = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(tmp)
    scene_fn(d, 0, 0, w, h)
    return tmp


# ------------------------------------------------------------------ lead scenes
# (reused from the v1 generator: detailed dusk bridge + tanker scenes)

def draw_lead_scene(draw, x0, y0, x1, y1):
    """Compact dusk bridge scene for a small box: broken span, fire,
    smoke, tilted section sliding into the water."""
    w, h = x1 - x0, y1 - y0
    horizon = y0 + int(h * 0.60)
    for y in range(y0, horizon):
        t = (y - y0) / max(1, horizon - y0)
        c = lerp((43, 52, 96), (214, 110, 52), t * t)
        draw.line([(x0, y), (x1, y)], fill=c)
    sx, sy = x0 + int(w * 0.28), horizon - 22
    for r in (16, 11, 6):
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 190, 90))
    for y in range(horizon, y1):
        t = (y - horizon) / max(1, y1 - horizon)
        c = lerp((38, 58, 88), (18, 28, 50), t)
        draw.line([(x0, y), (x1, y)], fill=c)
    deck_y = horizon - 30
    # Towers.
    for tx in (x0 + 18, x1 - 26):
        draw.rectangle([tx, deck_y - 52, tx + 8, deck_y + 2],
                       fill=(24, 26, 38))
    for tx in (x0 + 22, x1 - 22):
        draw.line([(tx, deck_y - 52), (tx - 34, deck_y)],
                  fill=(24, 26, 38), width=2)
        draw.line([(tx, deck_y - 52), (tx + 34, deck_y)],
                  fill=(24, 26, 38), width=2)
    # Deck with a gap in the middle.
    gap_l = x0 + int(w * 0.42)
    gap_r = x0 + int(w * 0.62)
    draw.rectangle([x0, deck_y, gap_l, deck_y + 6], fill=(24, 26, 38))
    draw.rectangle([gap_r, deck_y, x1, deck_y + 6], fill=(24, 26, 38))
    # Broken span tilted into the water.
    draw.polygon([(gap_l, deck_y), (gap_r - 8, deck_y + 3),
                  (gap_r + 2, deck_y + 34), (gap_l + 6, deck_y + 30)],
                 fill=(30, 32, 46))
    # Fire at the break.
    fx, fy = (gap_l + gap_r) // 2, deck_y - 3
    for r, col in ((16, (255, 120, 20)), (11, (255, 170, 40)),
                   (6, (255, 220, 90))):
        draw.ellipse([fx - r, fy - r, fx + r, fy + r], fill=col)
    # Smoke.
    for (cx, cy, r) in ((fx - 4, fy - 14, 7), (fx + 6, fy - 24, 9),
                        (fx - 2, fy - 34, 10)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 92, 96))


def draw_tanker(draw, x0, y0, x1, y1):
    """Compact tanker scene for a small box: tanker on a dark sea, a
    mine beside it, flames on deck."""
    w, h = x1 - x0, y1 - y0
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        draw.line([(x0, y), (x1, y)],
                  fill=lerp((64, 84, 110), (20, 30, 48), t))
    sea_y = y0 + int(h * 0.62)
    draw.rectangle([x0, sea_y, x1, y1], fill=(16, 28, 48))
    draw.polygon([(x0 + 8, sea_y - 16), (x1 - 8, sea_y - 16),
                  (x1 - 22, sea_y + 4), (x0 + 22, sea_y + 4)],
                 fill=(120, 30, 26))
    draw.rectangle([x0 + 14, sea_y - 42, x0 + 46, sea_y - 14],
                   fill=(200, 200, 200))
    draw.rectangle([x0 + 54, sea_y - 34, x0 + 66, sea_y - 14],
                   fill=(200, 200, 200))
    for (fx, r, col) in ((x0 + int(w * 0.62), 10, (255, 140, 30)),
                         (x0 + int(w * 0.74), 7, (255, 200, 60))):
        draw.ellipse([fx - r, sea_y - 26 - r, fx + r, sea_y - 26 + r],
                     fill=col)
    mx, my = x1 - 26, sea_y - 4
    draw.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=(30, 30, 34))
    for ang in range(0, 360, 45):
        dx = int(12 * math.cos(math.radians(ang)))
        dy = int(12 * math.sin(math.radians(ang)))
        draw.line([(mx, my), (mx + dx, my + dy)], fill=(30, 30, 34),
                  width=2)


def draw_capitol_scene(draw, x0, y0, x1, y1):
    """Compact US Capitol scene for a small box: dusk sky, dome with
    statue, columns, flag, crowd dots at the base."""
    w, h = x1 - x0, y1 - y0
    horizon = y0 + int(h * 0.72)
    for y in range(y0, horizon):
        t = (y - y0) / max(1, horizon - y0)
        c = lerp((38, 48, 88), (196, 120, 70), t * t)
        draw.line([(x0, y), (x1, y)], fill=c)
    draw.rectangle([x0, horizon, x1, y1], fill=(52, 58, 66))
    cx = (x0 + x1) // 2
    base = horizon - 6
    # Dome: drum, cupola, statue.
    draw.rectangle([cx - 34, base - 46, cx + 34, base], fill=(232, 228, 218))
    draw.pieslice([cx - 34, base - 78, cx + 34, base - 40], 180, 360,
                  fill=(240, 236, 226))
    draw.rectangle([cx - 12, base - 92, cx + 12, base - 74],
                   fill=(240, 236, 226))
    draw.rectangle([cx - 2, base - 102, cx + 2, base - 92],
                   fill=(240, 236, 226))
    # Wings and columns.
    draw.rectangle([x0 + 6, base - 30, cx - 36, base], fill=(222, 218, 208))
    draw.rectangle([cx + 36, base - 30, x1 - 6, base], fill=(222, 218, 208))
    for px in range(cx - 30, cx + 31, 12):
        draw.rectangle([px, base - 44, px + 4, base], fill=(200, 196, 186))
    # Flag.
    draw.line([(x1 - 14, y0 + 8), (x1 - 14, y0 + 44)], fill=(30, 30, 34),
              width=2)
    for i, col in enumerate(((178, 34, 52), (255, 255, 255),
                             (178, 34, 52), (255, 255, 255),
                             (178, 34, 52))):
        draw.rectangle([x1 - 14, y0 + 10 + i * 5, x1 + 8, y0 + 15 + i * 5],
                       fill=col)
    draw.rectangle([x1 - 14, y0 + 10, x1 - 2, y0 + 22], fill=(40, 60, 120))
    # Crowd dots at the base.
    for (px, col) in ((x0 + 16, (30, 30, 34)), (x0 + 30, (120, 40, 35)),
                      (x1 - 30, (30, 30, 34)), (x1 - 16, (120, 40, 35))):
        draw.ellipse([px - 4, horizon + 6, px + 4, horizon + 14], fill=col)


# ------------------------------------------------------------------ small icons
# Flat pictograms for the small panels: (draw, x0, y0, x1, y1).

def _sky(d, x0, y0, x1, y1, top, bot):
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        d.line([(x0, y), (x1, y)], fill=lerp(top, bot, t))


def icon_bridge(d, x0, y0, x1, y1):
    _sky(d, x0, y0, x1, y1, (150, 175, 205), (210, 200, 180))
    my = y0 + int((y1 - y0) * 0.62)
    d.rectangle([x0, my, x1, y1], fill=(70, 95, 125))
    dy = my - 18
    d.line([(x0, dy), (x1, dy)], fill=(30, 32, 44), width=3)
    for tx in (x0 + 30, x1 - 34):
        d.rectangle([tx, dy - 26, tx + 4, dy], fill=(30, 32, 44))
    d.line([(x0 + 32, dy - 26), ((x0 + x1) // 2, dy)], fill=(30, 32, 44),
           width=2)
    d.line([(x1 - 32, dy - 26), ((x0 + x1) // 2, dy)], fill=(30, 32, 44),
           width=2)
    fx = (x0 + x1) // 2
    for r, c in ((10, (255, 120, 20)), (6, (255, 200, 60))):
        d.ellipse([fx - r, dy - r - 4, fx + r, dy + r - 4], fill=c)


def icon_burst(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 213, 192))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        x2 = cx + int(30 * math.cos(a))
        y2 = cy + int(30 * math.sin(a))
        d.line([(cx, cy), (x2, y2)], fill=(255, 140, 30), width=5)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 200, 60))


def icon_virus(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(220, 234, 217))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        x2 = cx + int(26 * math.cos(a))
        y2 = cy + int(26 * math.sin(a))
        d.line([(cx, cy), (x2, y2)], fill=(60, 130, 70), width=4)
        d.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=(60, 130, 70))
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(90, 160, 95))
    d.ellipse([cx - 6, cy - 8, cx + 2, cy + 0], fill=(60, 130, 70))


def icon_flags(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(223, 228, 238))
    poles = [x0 + 22, (x0 + x1) // 2 - 12, x1 - 46]
    flags = [((178, 34, 52), (255, 255, 255), (60, 60, 120)),
             ((222, 41, 16), (255, 222, 0), None),
             ((255, 255, 255), (0, 57, 166), (213, 0, 50))]
    for px, (c1, c2, c3) in zip(poles, flags):
        d.rectangle([px - 2, y0 + 10, px + 2, y1 - 8], fill=(60, 52, 40))
        fy = y0 + 10
        if c3 is None:
            d.rectangle([px + 2, fy, px + 26, fy + 22], fill=c1)
            for (sx, sy) in ((px + 9, fy + 7), (px + 16, fy + 6),
                             (px + 20, fy + 12)):
                d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=c2)
        else:
            d.rectangle([px + 2, fy, px + 26, fy + 7], fill=c1)
            d.rectangle([px + 2, fy + 7, px + 26, fy + 14], fill=c2)
            d.rectangle([px + 2, fy + 14, px + 26, fy + 22], fill=c3)


def icon_gavel(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(236, 226, 217))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 26, cy - 16, cx + 6, cy - 2], fill=(120, 72, 32))
    d.rectangle([cx - 2, cy - 10, cx + 28, cy + 20], fill=(150, 100, 50))
    d.rectangle([cx - 22, cy + 14, cx + 22, cy + 22], fill=(90, 60, 30))


def icon_globe(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(223, 232, 216))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(90, 140, 190))
    for rx in (8, 18):
        d.ellipse([cx - rx, cy - 24, cx + rx, cy + 24],
                  outline=(240, 240, 220), width=2)
    d.line([(cx - 24, cy), (cx + 24, cy)], fill=(240, 240, 220), width=2)
    d.ellipse([cx - 14, cy - 16, cx - 2, cy - 4], fill=(110, 170, 90))
    d.ellipse([cx + 2, cy + 6, cx + 16, cy + 18], fill=(110, 170, 90))


def icon_bank(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 228, 220))
    cx = (x0 + x1) // 2
    d.polygon([(cx - 30, y0 + 14), (cx + 30, y0 + 14), (cx, y0 + 2)],
              fill=(80, 70, 60))
    for px in (cx - 24, cx - 8, cx + 8, cx + 20):
        d.rectangle([px, y0 + 18, px + 5, y1 - 12], fill=(80, 70, 60))
    d.rectangle([x0 + 8, y1 - 12, x1 - 8, y1 - 6], fill=(80, 70, 60))


def icon_crowd(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(234, 224, 213))
    for px, col in ((x0 + 34, (60, 60, 70)), ((x0 + x1) // 2, (140, 40, 35)),
                    (x1 - 34, (60, 60, 70))):
        d.ellipse([px - 8, y0 + 12, px + 8, y0 + 28], fill=col)
        d.pieslice([px - 14, y0 + 30, px + 14, y0 + 52], 180, 360, fill=col)


def icon_satellite(d, x0, y0, x1, y1):
    _sky(d, x0, y0, x1, y1, (12, 16, 38), (52, 40, 78))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for (sx, sy) in ((x0 + 16, y0 + 10), (x1 - 18, y0 + 16),
                     (x0 + 24, y1 - 12), (x1 - 12, y1 - 10)):
        d.point((sx, sy), fill=(220, 220, 240))
    d.rectangle([cx - 8, cy - 6, cx + 8, cy + 6], fill=(150, 160, 180))
    d.rectangle([cx - 26, cy - 3, cx - 8, cy + 3], fill=(40, 90, 180))
    d.rectangle([cx + 8, cy - 3, cx + 26, cy + 3], fill=(40, 90, 180))
    d.arc([cx + 16, cy - 18, cx + 40, cy + 6], -60, 60,
          fill=(255, 220, 90), width=2)


def icon_plane(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(223, 230, 238))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.polygon([(cx - 34, cy), (cx + 26, cy - 8), (cx + 34, cy),
               (cx + 26, cy + 8)], fill=(50, 55, 70))
    d.polygon([(cx - 6, cy - 4), (cx + 6, cy - 20), (cx + 12, cy - 4)],
              fill=(50, 55, 70))
    d.polygon([(cx - 6, cy + 4), (cx + 2, cy + 18), (cx + 8, cy + 4)],
              fill=(50, 55, 70))
    d.line([(x0 + 8, cy + 22), (x1 - 8, cy + 22)], fill=(150, 150, 160),
           width=2)


def icon_chart(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(227, 234, 217))
    base = y1 - 12
    for i, h in enumerate((14, 22, 16, 28)):
        bx = x0 + 14 + i * 20
        d.rectangle([bx, base - h, bx + 12, base], fill=(40, 120, 70))
    d.line([(x0 + 10, base - 34), (x1 - 12, base - 44)],
           fill=(179, 38, 30), width=3)
    d.polygon([(x1 - 12, base - 44), (x1 - 22, base - 44),
               (x1 - 14, base - 52)], fill=(179, 38, 30))


def icon_cyclone(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(217, 230, 234))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 2
    for r in (22, 16, 10):
        d.arc([cx - r, cy - r, cx + r, cy + r], -40, 200,
              fill=(40, 90, 130), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(40, 90, 130))
    for dx in (-18, 0, 18):
        d.line([(cx + dx, y1 - 14), (cx + dx - 3, y1 - 6)],
               fill=(40, 90, 130), width=3)


def icon_scales(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 228, 220))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 2, y0 + 8, cx + 2, y1 - 12], fill=(70, 60, 50))
    d.line([(cx - 26, y0 + 12), (cx + 26, y0 + 12)], fill=(70, 60, 50),
           width=3)
    for px in (cx - 26, cx + 26):
        d.line([(px, y0 + 12), (px, y0 + 26)], fill=(70, 60, 50), width=2)
        d.pieslice([px - 10, y0 + 24, px + 10, y0 + 36], 0, 180,
                   fill=(150, 120, 60))
    d.rectangle([cx - 16, y1 - 12, cx + 16, y1 - 6], fill=(70, 60, 50))


def icon_ship(d, x0, y0, x1, y1):
    _sky(d, x0, y0, x1, y1, (190, 205, 220), (220, 215, 195))
    my = y0 + int((y1 - y0) * 0.6)
    d.rectangle([x0, my, x1, y1], fill=(90, 130, 160))
    d.polygon([(x0 + 10, my - 8), (x1 - 10, my - 8), (x1 - 26, my + 10),
               (x0 + 26, my + 10)], fill=(60, 60, 70))
    for i, col in enumerate(((200, 60, 40), (40, 110, 70), (220, 170, 40))):
        bx = x0 + 20 + i * 20
        d.rectangle([bx, my - 26, bx + 16, my - 8], fill=col)


def icon_trophy(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 226, 213))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 4
    d.pieslice([cx - 16, cy - 14, cx + 16, cy + 14], 180, 360,
               fill=(200, 160, 40))
    d.rectangle([cx - 4, cy + 6, cx + 4, cy + 16], fill=(200, 160, 40))
    d.rectangle([cx - 12, cy + 16, cx + 12, cy + 20], fill=(200, 160, 40))
    d.arc([cx - 24, cy - 12, cx - 8, cy + 4], 90, 270,
          fill=(200, 160, 40), width=3)
    d.arc([cx + 8, cy - 12, cx + 24, cy + 4], -90, 90,
          fill=(200, 160, 40), width=3)


ICONS = {
    "bridge": icon_bridge, "burst": icon_burst, "virus": icon_virus,
    "flags": icon_flags, "gavel": icon_gavel, "globe": icon_globe,
    "bank": icon_bank, "crowd": icon_crowd, "satellite": icon_satellite,
    "plane": icon_plane, "chart": icon_chart, "cyclone": icon_cyclone,
    "scales": icon_scales, "ship": icon_ship, "trophy": icon_trophy,
}


# ------------------------------------------------------------------ world map

NA = [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 73), (-100, 73),
      (-90, 74), (-85, 70), (-80, 73), (-75, 72), (-65, 62), (-60, 55),
      (-55, 47), (-60, 45), (-70, 42), (-75, 35), (-80, 32), (-81, 26),
      (-84, 30), (-90, 21), (-94, 17), (-97, 16), (-100, 18), (-105, 20),
      (-110, 23), (-115, 29), (-120, 34), (-125, 40), (-124, 48),
      (-130, 55), (-140, 60), (-150, 60), (-158, 58), (-165, 60)]
GREENLAND = [(-55, 60), (-45, 60), (-35, 64), (-25, 70), (-20, 74),
             (-30, 76), (-45, 76), (-58, 70), (-58, 64)]
SA = [(-79, 9), (-77, 4), (-75, 0), (-70, -5), (-60, -8), (-50, -5),
      (-40, -5), (-35, -8), (-38, -15), (-40, -22), (-48, -27), (-55, -34),
      (-60, -38), (-65, -42), (-68, -50), (-70, -54), (-73, -48),
      (-73, -38), (-72, -28), (-70, -18), (-75, -15), (-80, -8),
      (-81, -4), (-80, 2)]
AFRICA = [(-17, 15), (-16, 20), (-10, 28), (-5, 35), (0, 36), (10, 37),
          (15, 32), (20, 32), (25, 31), (30, 31), (32, 31), (35, 28),
          (38, 22), (40, 15), (43, 12), (48, 11), (51, 12), (48, 5),
          (45, 0), (40, -5), (40, -12), (36, -18), (33, -25), (28, -32),
          (20, -35), (15, -32), (12, -25), (12, -18), (10, -12), (9, -2),
          (8, 4), (0, 5), (-8, 5), (-13, 8), (-17, 12)]
EURASIA = [(-10, 36), (-9, 38), (-2, 37), (0, 39), (3, 42), (7, 44),
           (10, 44), (12, 42), (15, 40), (18, 40), (20, 38), (23, 36),
           (26, 38), (28, 40), (30, 36), (33, 36), (36, 36), (38, 38),
           (40, 41), (43, 41), (46, 44), (48, 46), (50, 46), (52, 47),
           (54, 50), (56, 52), (58, 55), (60, 58), (62, 62), (65, 65),
           (68, 68), (70, 70), (72, 72), (75, 74), (78, 75), (82, 76),
           (86, 76), (90, 76), (95, 76), (100, 77), (105, 77), (110, 76),
           (115, 73), (120, 72), (125, 71), (130, 71), (135, 72),
           (140, 72), (145, 72), (150, 71), (155, 70), (158, 68),
           (160, 66), (162, 64), (162, 60), (160, 56), (158, 52),
           (155, 55), (150, 59), (145, 59), (142, 55), (140, 52),
           (138, 48), (136, 44), (134, 42), (130, 42), (128, 38),
           (126, 38), (124, 38), (122, 37), (120, 34), (120, 30),
           (118, 28), (115, 25), (112, 22), (110, 20), (108, 18),
           (106, 14), (105, 10), (103, 8), (101, 6), (99, 8), (98, 12),
           (97, 15), (95, 18), (93, 20), (91, 22), (89, 22), (87, 21),
           (85, 19), (82, 17), (80, 14), (78, 8), (76, 10), (74, 14),
           (72, 18), (70, 20), (68, 22), (66, 24), (64, 25), (62, 25),
           (60, 25), (58, 26), (56, 27), (54, 27), (52, 28), (50, 29),
           (48, 29), (46, 29), (44, 29), (42, 28), (40, 30), (38, 32),
           (36, 36), (33, 36), (30, 36), (27, 37), (24, 36), (21, 37),
           (18, 38), (15, 38), (12, 44), (8, 44), (5, 43), (2, 42),
           (0, 40), (-2, 37), (-5, 36), (-8, 36)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (-1, 51)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 36), (140, 38),
         (141, 40), (142, 42), (141, 44), (140, 42), (138, 38), (136, 36),
         (133, 34), (131, 32)]
SUMATRA = [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (103, -5),
           (100, -2), (97, 2)]
BORNEO = [(109, 1), (113, 4), (117, 2), (118, -2), (116, -4), (112, -3),
          (110, 0)]
NEWGUINEA = [(131, -1), (136, -2), (141, -4), (146, -6), (148, -8),
             (144, -8), (139, -7), (134, -4)]
PHILIPPINES = [(120, 18), (122, 16), (121, 13), (122, 10), (124, 8),
               (122, 11), (120, 14)]
AUSTRALIA = [(113, -22), (114, -28), (115, -33), (118, -35), (122, -34),
             (126, -32), (129, -32), (132, -32), (135, -35), (138, -35),
             (140, -38), (144, -38), (147, -39), (150, -37), (153, -32),
             (153, -27), (151, -24), (148, -20), (146, -19), (143, -17),
             (142, -14), (142, -11), (140, -13), (137, -12), (135, -14),
             (133, -12), (131, -12), (129, -14), (126, -14), (124, -16),
             (122, -17), (120, -19), (117, -20), (114, -21)]
NZ = [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38),
      (175, -40), (172, -42), (168, -46)]
MADAGASCAR = [(44, -16), (47, -15), (50, -17), (48, -22), (45, -25),
              (43, -21), (44, -18)]
CONTINENTS = [NA, GREENLAND, SA, AFRICA, EURASIA, UK, JAPAN, SUMATRA,
              BORNEO, NEWGUINEA, PHILIPPINES, AUSTRALIA, NZ, MADAGASCAR]


# ------------------------------------------------------------------ stories
# (n, tag, headline, summary, icon, lon, lat) — lon/lat None = no pin.

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
     "Ottawa seeks the right deal with Beijing — and with Washington — after years of frost.",
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

LEAD_SCENES = {1: draw_capitol_scene}

# (big figure, label) for the BY THE NUMBERS strip — the data angle
# the top-1 entries do not have: the day's key figures at a glance.
NUMBERS = [
    ("251–11", "Jeffries Speaker vote"),
    ("9 seats", "Democrats' Senate flips"),
    ("145 km/h", "Cyclone Akvan gusts"),
    ("16.1bn mi", "Voyager 1 from Earth"),
    ("2.57bn", "Muslims projected 2035"),
]


# ------------------------------------------------------------------ page

def draw_badge(draw, cx, cy, n, r=12):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    f = font(SANS_B, 13 if n < 10 else 11)
    draw.text((cx, cy), str(n), font=f, fill=(255, 255, 255), anchor="mm")


def draw_lead(img, draw, x, y, w, h, story):
    n, tag, head, summ, icon, _lon, _lat = story
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    ix0, iy0, ix1, iy1 = x + 8, y + 8, x + 196, y + h - 8
    scene = LEAD_SCENES.get(n)
    if scene is not None:
        img.paste(clip_scene(scene, ix0, iy0, ix1, iy1), (ix0, iy0))
    else:
        ICONS[icon](draw, ix0, iy0, ix1, iy1)
    draw.rectangle([ix0, iy0, ix1, iy1], outline=INK, width=1)
    tx = x + 208
    tw = w - 208 - 10
    draw_badge(draw, tx + 8, y + 16, n)
    draw.text((tx + 26, y + 9), tag, font=font(SANS_B, 11), fill=RED)
    f_head = font(SERIF_B, 23)
    lines = wrap(draw, head, f_head, tw)[:3]
    yy = y + 34
    for line in lines:
        draw.text((tx, yy), line, font=f_head, fill=INK)
        yy += 27
    f_summ = font(SANS, 13)
    yy += 4
    for line in wrap(draw, summ, f_summ, tw)[:3]:
        draw.text((tx, yy), line, font=f_summ, fill=(40, 38, 32))
        yy += 17


def draw_small(draw, x, y, w, h, story):
    n, tag, head, summ, icon, _lon, _lat = story
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    ix0, iy0, ix1, iy1 = x + 6, y + 6, x + w - 6, y + 58
    ICONS[icon](draw, ix0, iy0, ix1, iy1)
    draw.rectangle([ix0, iy0, ix1, iy1], outline=INK, width=1)
    draw_badge(draw, x + 16, y + 70, n, r=10)
    draw.text((x + 30, y + 64), tag, font=font(SANS_B, 9), fill=RED)
    f_head = font(SANS_B, 14)
    yy = y + 80
    for line in wrap(draw, head, f_head, w - 12)[:3]:
        draw.text((x + 6, yy), line, font=f_head, fill=INK)
        yy += 16
    f_summ = font(SANS, 11)
    yy += 3
    for line in wrap(draw, summ, f_summ, w - 12)[:2]:
        draw.text((x + 6, yy), line, font=f_summ, fill=(40, 38, 32))
        yy += 13


def project(lon, lat, mx0, my0, mw, mh):
    px = mx0 + (lon + 180.0) / 360.0 * mw
    py = my0 + (84.0 - lat) / 142.0 * mh
    return px, py


REGION_COLORS = [
    ("Europe", (40, 90, 160)),
    ("Middle East", (200, 110, 30)),
    ("Asia", (180, 40, 35)),
    ("Africa", (60, 140, 70)),
    ("Americas", (120, 70, 150)),
    ("Oceania", (30, 140, 140)),
]


def region_color(lon, lat):
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


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    draw.text((x + 8, y + 8), "WHERE IT HAPPENED",
              font=font(SANS_B, 13), fill=INK)
    draw.line([(x + 8, y + 28), (x + w - 8, y + 28)], fill=RULE, width=1)
    mx0, my0, mw, mh = x + 8, y + 36, w - 16, h - 80
    draw.rectangle([mx0, my0, mx0 + mw, my0 + mh],
                   fill=(233, 228, 213))
    for poly in CONTINENTS:
        pts = [project(lon, lat, mx0, my0, mw, mh) for lon, lat in poly]
        draw.polygon(pts, fill=(199, 186, 148), outline=(120, 110, 90))
    for item in LISTED:
        _n, _t, lon, lat = item
        if lon is None:
            continue
        px, py = project(lon, lat, mx0, my0, mw, mh)
        col = region_color(lon, lat)
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=col)
    for story in MAIN:
        n, _tag, _head, _summ, _icon, lon, lat = story
        if lon is None:
            continue
        px, py = project(lon, lat, mx0, my0, mw, mh)
        # Nudge the crowded Washington / Shenzhen / Beijing pins apart.
        px += {1: 12, 2: -12, 5: -14, 9: 12, 10: -12}.get(n, 0)
        py += {1: -10, 2: -8, 5: 8, 9: -8, 10: 10}.get(n, 0)
        draw.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                     outline=(255, 255, 255), width=1)
        f = font(SANS_B, 10)
        draw.text((px, py), str(n), font=f, fill=(255, 255, 255),
                  anchor="mm")
    draw.text((x + 8, y + h - 34), "Numbered dots mark stories 1–12.",
              font=font(SANS, 10), fill=GREY)
    lx = x + 8
    ly = y + h - 20
    f_leg = font(SANS_B, 9)
    for name, col in REGION_COLORS:
        draw.ellipse([lx, ly, lx + 7, ly + 7], fill=col)
        lx += 11
        tw = draw.textlength(name, font=f_leg)
        draw.text((lx, ly - 1), name, font=f_leg, fill=GREY)
        lx += tw + 12


def draw_list(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    draw.text((x + 8, y + 8), "ALSO ON THURSDAY 19 NOVEMBER — 24 MORE STORIES",
              font=font(SANS_B, 13), fill=INK)
    draw.line([(x + 8, y + 28), (x + w - 8, y + 28)], fill=RULE, width=1)
    f_num = font(SANS_B, 10)
    f_txt = font(SANS, 10)
    col_w = (w - 16) // 2
    per_col = (len(LISTED) + 1) // 2
    for ci in range(2):
        cx = x + 8 + ci * col_w
        yy = y + 36
        for item in LISTED[ci * per_col:(ci + 1) * per_col]:
            n, text, _lon, _lat = item
            draw.text((cx, yy), str(n), font=f_num, fill=RED)
            draw.text((cx + 20, yy), text, font=f_txt, fill=INK)
            yy += 18


def draw_numbers(draw, x, y, w, h):
    """BY THE NUMBERS strip: the day's key figures at a glance."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    bw = w // len(NUMBERS)
    f_big = font(SERIF_B, 19)
    f_lab = font(SANS, 9)
    for i, (big, label) in enumerate(NUMBERS):
        cx = x + i * bw + bw // 2
        if i:
            draw.line([(x + i * bw, y + 6), (x + i * bw, y + h - 6)],
                      fill=(90, 105, 130), width=1)
        draw.text((cx, y + 3), big, font=f_big, fill=GOLD, anchor="ma")
        lines = wrap(draw, label, f_lab, bw - 12)[:1]
        for line in lines:
            draw.text((cx, y + h - 13), line, font=f_lab, fill=CREAM,
                      anchor="ma")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead ----
    draw.rectangle([0, 0, W, 102], fill=NAVY)
    draw.text((24, 12), "THE DAY IN WORLD NEWS",
              font=font(SANS_B, 13), fill=GOLD)
    draw.text((W - 24, 12), "36 STORIES · 6 CONTINENTS · ONE DAY",
              font=font(SANS_B, 13), fill=GOLD, anchor="ra")
    draw.text((W // 2, 30), "Thursday 19 November 2026",
              font=font(SERIF_B, 52), fill=CREAM, anchor="ma")
    draw.rectangle([0, 102, W, 106], fill=GOLD)

    # ---- Lead row: stories 1-2 ----
    draw_lead(img, draw, 8, 110, 500, 182, MAIN[0])
    draw_lead(img, draw, 516, 110, 500, 182, MAIN[1])

    # ---- Two rows of five: stories 3-12 ----
    for i, story in enumerate(MAIN[2:]):
        row, col = divmod(i, 5)
        draw_small(draw, 8 + col * 203, 300 + row * 166, 195, 158, story)

    # ---- BY THE NUMBERS strip ----
    draw_numbers(draw, 8, 632, 1008, 38)

    # ---- Bottom: map + list ----
    draw_map(draw, 8, 678, 500, 312)
    draw_list(draw, 516, 678, 500, 312)

    # ---- Footer ----
    draw.text((W // 2, 997),
              "Stories leading Thursday 19 November 2026's news; disputed claims are attributed.",
              font=font(SANS, 10), fill=GREY, anchor="ma")
    draw.text((W // 2, 1009),
              "Sources: Reuters, AP, AFP, BBC, Al Jazeera, NASA, IMD, Pew Research and others. Original drawings.",
              font=font(SANS, 10), fill=GREY, anchor="ma")
    return img


def main():
    out = os.environ.get("ENTRY_OUT", "entry.png")
    img = build()
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size,
          os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
