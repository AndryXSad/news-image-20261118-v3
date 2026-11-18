#!/usr/bin/env python3
"""The Daily Globe — Wednesday 18 November 2026 (v3).

Renders the make.fun news-image-20261118 entry: a 1024x1024 newspaper
front page summing up the world's news of 18 November 2026 — 33 stories
across 6 continents, a real Natural Earth world map keyed to the day's
eight biggest stories, a drawn illustration of the Kerch bridge attack,
and three illustrated secondary stories.

Run:  python3 main.py            (writes entry.png next to this file)
      MAKEFUN_OUTPUT_DIR=out python3 main.py   (also writes out/entry.png)

Python 3, Pillow only, no network, fully deterministic.
"""

import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MX = 30                      # side margin
CW = W - 2 * MX              # content width: 964

# ---------------------------------------------------------------- palette
PAPER   = (247, 242, 231)    # warm newsprint
INK     = (26, 23, 18)
SOFTINK = (58, 54, 46)
GREY    = (110, 104, 92)
RED     = (176, 32, 44)
NAVY    = (29, 58, 95)
OCEAN   = (216, 230, 236)
LAND    = (233, 220, 192)
LANDLN  = (198, 180, 140)
GOLD    = (214, 158, 46)
TEAL    = (16, 110, 104)
NIGHT   = (18, 34, 60)
NIGHT2  = (12, 24, 44)

# ---------------------------------------------------------------- fonts
FDIR = "/usr/share/fonts/truetype"
SERIF_B = f"{FDIR}/liberation/LiberationSerif-Bold.ttf"
SERIF_R = f"{FDIR}/liberation/LiberationSerif-Regular.ttf"
SERIF_I = f"{FDIR}/liberation/LiberationSerif-Italic.ttf"
SANS_B  = f"{FDIR}/dejavu/DejaVuSans-Bold.ttf"
SANS_R  = f"{FDIR}/dejavu/DejaVuSans.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- text helpers
def wrap_text(draw, text, font, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, width, fill=INK, leading=4, max_lines=None):
    """Draw a wrapped paragraph; return the y just below its last line."""
    lines = wrap_text(draw, text, font, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += font.size + leading
    return y


def rule(draw, y, x0=MX, x1=W - MX, width=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def double_rule(draw, y):
    rule(draw, y, width=3)
    rule(draw, y + 5, width=1)
    return y + 9


# ---------------------------------------------------------------- the day's stories
LEAD_KICK = "UKRAINE WAR  —  1"
LEAD_HEAD = "Ukraine destroys a span of Putin's Crimea bridge"
LEAD_DECK = ("Kyiv calls the overnight attack 'unprecedented'; Moscow "
             "answers by pounding bridges in the capital.")
LEAD_BYLINE = "From our correspondents in Kyiv and Moscow"

SECONDARIES = [
    dict(kick="MANILA  —  3",
         head="Trump lands in Manila for Quad talks ahead of China visit",
         stand="Quad leaders open the Manila summit before APEC.",
         kind="quad"),
    dict(kick="SHENZHEN  —  4",
         head="APEC opens in Shenzhen; first Trump–Xi–Putin summit tomorrow",
         stand="Three leaders meet on APEC's sidelines.",
         kind="apec"),
    dict(kick="WALL STREET",
         head="Nvidia revenue doubles to $115.8bn; board won't bring back Huang",
         stand="Trump backs calls to bring Huang back.",
         kind="nvda"),
]

GRID = [
    (2, "EUROPE", "Russia hits Kyiv bridges in reply; UN counts 372 dead in October"),
    (5, "MIDDLE EAST", "Iran drones hit a US radar site in Bahrain; Kuwait reports attacks"),
    (6, "ASIA", "US presses UN aviation body over Taiwan curbs; China hits back"),
    (7, "ASIA", "North Korea fires a ballistic missile into the Sea of Japan"),
    (8, "ASIA", "Modi presses Indo-Pacific vision at East Asia Summit; e-visas open"),
    (None, "ASIA", "Cyclone Akvan bears down on Andhra Pradesh; landfall due 20 Nov"),
    (None, "SPORT", "Dhoni bids farewell to the IPL"),
    (None, "MARKETS", "Dow plunges 1,000 points as Wall Street reels"),
    (None, "BUSINESS", "Anthropic prices its long-awaited IPO"),
    (None, "EUROPE", "Britain sanctions eight firms over illegal West Bank settlements"),
    (None, "EUROPE", "UK pledges £240m for Ukraine's air defences"),
    (None, "EUROPE", "Estonia to shut its border with Russia from December"),
    (None, "EUROPE", "Hundreds of thousands march in Prague for media freedom"),
    (None, "AFRICA", "Rival DR Congo peace efforts fail as eastern violence flares"),
    (None, "MIDDLE EAST", "Gaza ceasefire 'faces imminent collapse', Board of Peace warns"),
    (None, "MIDDLE EAST", "Israel's parliament elects Matan Kahana as speaker"),
    (None, "AMERICAS", "Pakistani man jailed 27½ years in the US over a plot to kill Trump"),
    (None, "ASIA", "Xi meets Carney as Canada and China extend trade deals"),
]

TICKER = [
    "Latvia approves new Kulbergs cabinet",
    "Germany warns of hybrid, cyber threats",
    "Strikes halt Spain; walkouts hit France",
    "Ecuador fishermen sue Trump over drone strike",
    "EU agrees €45bn loan for Ukraine",
    "Cape Town baboon move sparks protests",
    "Deutsche Bank ignored client warnings",
    "Trump gets until 22 Jan in $10bn BBC suit",
    "NZ takes blame for Penrhyn port blowout",
    "One Nation vows 90% refugee-intake cut",
    "Voyager 1 reaches one light-day from Earth",
]


# ---------------------------------------------------------------- masthead
def draw_masthead(d):
    y = 16
    d.text((W // 2, y), "THE DAILY GLOBE", font=fnt(SERIF_B, 56),
           fill=INK, anchor="ma")
    y = 84
    rule(d, y, width=1)
    y = 92
    d.text((MX, y), "WEDNESDAY 18 NOVEMBER 2026", font=fnt(SANS_B, 15), fill=RED)
    d.text((W // 2, y), "33 STORIES  ·  6 CONTINENTS  ·  ONE DAY",
           font=fnt(SANS_R, 12), fill=SOFTINK, anchor="ma")
    d.text((W - MX, y), "WORLD EDITION", font=fnt(SANS_B, 15), fill=INK, anchor="ra")
    return double_rule(d, 114)


# ---------------------------------------------------------------- world map
# (num, lon, lat, dx, dy) — dx/dy fan the badge away from its true point
# so the crowded East Asia / Black Sea clusters stay readable.
MARKERS = [
    (1, 35.4, 45.3, 20, 14),      # Crimea bridge
    (2, 30.5, 50.45, -28, -20),   # Kyiv
    (3, 121.0, 14.6, 10, 22),     # Manila
    (4, 114.1, 22.5, -24, -6),    # Shenzhen
    (5, 50.6, 26.2, 0, 20),       # Bahrain
    (6, 121.6, 25.0, 22, -14),    # Taipei
    (7, 125.75, 39.0, 12, -22),   # Pyongyang
    (8, 77.2, 28.6, -6, -22),     # New Delhi
]


def draw_map(img, y0, height):
    d = ImageDraw.Draw(img)
    x0, x1 = MX, W - MX
    y1 = y0 + height
    lat_top, lat_bot = 82.0, -58.0
    mw, mh = x1 - x0, height

    # Draw the map on its own layer so land that runs past the frame
    # (Antarctica below lat_bot) is clipped instead of spilling over
    # the caption underneath.
    layer = Image.new("RGB", (mw, mh), OCEAN)
    ld = ImageDraw.Draw(layer)

    def project(lon, lat):
        x = (lon + 180.0) / 360.0 * mw
        yy = (lat_top - lat) / (lat_top - lat_bot) * mh
        return x, yy

    for lon in range(-150, 181, 30):
        x, _ = project(lon, 0)
        ld.line([(x, 0), (x, mh)], fill=(198, 212, 220), width=1)
    for lat in range(-30, 91, 30):
        _, yy = project(0, lat)
        ld.line([(0, yy), (mw, yy)], fill=(198, 212, 220), width=1)

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "data", "land.json")) as fh:
        geo = json.load(fh)
    for ring in geo["land"]:
        pts, prev = [], None
        for lon, lat in ring:
            if prev is not None and abs(lon - prev) > 180:
                if len(pts) >= 3:
                    ld.polygon(pts, fill=LAND, outline=LANDLN)
                pts = []
            pts.append(project(lon, lat))
            prev = lon
        if len(pts) >= 3:
            ld.polygon(pts, fill=LAND, outline=LANDLN)
    for ring in geo["holes"]:  # lakes / inland seas punch back to ocean
        pts = [project(lon, lat) for lon, lat in ring]
        if len(pts) >= 3:
            ld.polygon(pts, fill=OCEAN, outline=LANDLN)

    lab = fnt(SANS_B, 10)
    for txt, lon, lat in [("NORTH AMERICA", -100, 56), ("SOUTH AMERICA", -60, -14),
                          ("EUROPE", 4, 52), ("AFRICA", 18, 6),
                          ("ASIA", 92, 56), ("AUSTRALIA", 134, -25)]:
        x, yy = project(lon, lat)
        ld.text((x, yy), txt, font=lab, fill=(120, 108, 84), anchor="ma")
    ocn = fnt(SERIF_I, 12)
    for txt, lon, lat in [("PACIFIC", -150, 2), ("PACIFIC", 158, -38),
                          ("ATLANTIC", -32, 22), ("INDIAN", 82, -32)]:
        x, yy = project(lon, lat)
        ld.text((x, yy), txt, font=ocn, fill=(96, 120, 140), anchor="ma")

    numf = fnt(SANS_B, 11)
    for num, lon, lat, dx, dy in MARKERS:
        x, yy = project(lon, lat)
        bx, by = x + dx, yy + dy
        ld.ellipse([x - 3, yy - 3, x + 3, yy + 3], fill=RED)
        if dx or dy:
            ld.line([(x, yy), (bx, by)], fill=RED, width=1)
        ld.ellipse([bx - 11, by - 11, bx + 11, by + 11], fill=RED,
                   outline=(255, 255, 255), width=2)
        ld.text((bx, by - 1), str(num), font=numf, fill=(255, 255, 255), anchor="mm")

    img.paste(layer, (x0, y0))
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    d.text((MX, y1 + 7),
           "THE WORLD AT A GLANCE — the numbered places are the day's biggest stories, keyed below.",
           font=fnt(SANS_R, 11), fill=GREY)
    return y1 + 26


# ---------------------------------------------------------------- lead story + Kerch illustration
def draw_kerch(d, x0, y0, w, h):
    """Night scene: the Kerch bridge with a span blown out.

    Two suspension towers, sagging main cables, a deck with a missing
    middle span, one deck segment tipping into the strait, a fireball
    and smoke plume above the gap, stars overhead, water below.
    """
    x1, y1 = x0 + w, y0 + h
    # night sky in soft horizontal bands
    bands = [(26, 48, 84), (22, 42, 74), (18, 36, 64), (16, 32, 58)]
    bh = (h - 52) // len(bands)
    for i, col in enumerate(bands):
        d.rectangle([x0, y0 + i * bh, x1, y0 + (i + 1) * bh], fill=col)
    # stars (fixed pseudo-random pattern, deterministic; kept below the title)
    for i in range(26):
        sx = x0 + 12 + int((math.sin(i * 12.9898) * 43758.5453 % 1.0) * (w - 24))
        sy = y0 + 28 + int((math.sin(i * 78.233) * 12543.1234 % 1.0) * 34)
        r = 1 if i % 3 else 2
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 228, 240))
    # moon glow, upper right
    d.ellipse([x1 - 52, y0 + 12, x1 - 22, y0 + 42], fill=(232, 226, 196))
    d.ellipse([x1 - 48, y0 + 16, x1 - 26, y0 + 38], fill=(244, 240, 214))

    water_y = y0 + h - 52
    d.rectangle([x0, water_y, x1, y1], fill=NIGHT2)
    # water shimmer
    for i in range(9):
        wx = x0 + 14 + int((math.sin(i * 39.346) * 24634.6345 % 1.0) * (w - 60))
        wy = water_y + 8 + i * 4
        d.line([(wx, wy), (wx + 26, wy)], fill=(70, 100, 140), width=1)

    mid = x0 + w // 2
    deck_y = water_y - 12
    # suspension towers: slim verticals with a cap, no cross-beams
    for tx in (x0 + 58, x1 - 66):
        d.rectangle([tx, y0 + 44, tx + 8, deck_y], fill=(160, 168, 178))
        d.rectangle([tx - 3, y0 + 40, tx + 11, y0 + 46], fill=(160, 168, 178))
    # main cables: sagging curves tower-to-tower and to the edges
    def cable(p0, p1, sag):
        pts = []
        for t in range(21):
            tt = t / 20.0
            bx = p0[0] + (p1[0] - p0[0]) * tt
            by = p0[1] + (p1[1] - p0[1]) * tt + sag * 4 * tt * (1 - tt)
            pts.append((bx, by))
        d.line(pts, fill=(190, 196, 204), width=2)
    cable((x0 + 8, y0 + 46), (x0 + 62, y0 + 42), 24)
    cable((x0 + 62, y0 + 42), (x1 - 62, y0 + 42), 28)
    cable((x1 - 62, y0 + 42), (x1 - 8, y0 + 46), 24)
    # deck, left and right of the blown gap, with jagged broken ends
    gap = 48
    d.rectangle([x0 + 6, deck_y, mid - gap // 2, deck_y + 7], fill=(205, 210, 216))
    d.rectangle([mid + gap // 2, deck_y, x1 - 6, deck_y + 7], fill=(205, 210, 216))
    d.polygon([(mid - gap // 2, deck_y), (mid - gap // 2 + 8, deck_y + 7),
               (mid - gap // 2 + 2, deck_y + 12), (mid - gap // 2 - 4, deck_y + 8)],
              fill=(170, 176, 184))
    d.polygon([(mid + gap // 2, deck_y), (mid + gap // 2 - 8, deck_y + 7),
               (mid + gap // 2 - 2, deck_y + 12), (mid + gap // 2 + 4, deck_y + 8)],
              fill=(170, 176, 184))
    # deck segment tipping down into the gap, nose-first toward the water
    d.polygon([(mid - gap // 2 + 2, deck_y + 2), (mid + 10, deck_y + 4),
               (mid - 6, deck_y + 34), (mid - gap // 2 - 2, deck_y + 30)],
              fill=(178, 184, 192))
    d.line([(mid - 6, deck_y + 34), (mid + 2, water_y - 2)], fill=(178, 184, 192),
           width=3)
    # fireball in the gap
    cx, cy = mid, deck_y - 10
    for ang in range(0, 360, 20):
        ln = 30 if ang % 60 == 0 else 22
        ex = cx + math.cos(math.radians(ang)) * ln
        ey = cy + math.sin(math.radians(ang)) * ln
        d.line([(cx, cy), (ex, ey)], fill=(255, 176, 32), width=4)
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 120, 20))
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 214, 90))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 244, 200))
    # smoke column rising straight from the blast, drifting left at the top
    for sx, sy, r, col in [(mid - 2, cy - 26, 13, (110, 112, 118)),
                           (mid - 8, cy - 44, 15, (128, 130, 136)),
                           (mid - 20, cy - 60, 13, (146, 148, 154)),
                           (mid - 32, cy - 64, 10, (160, 162, 168)),
                           (mid + 12, cy - 52, 9, (128, 130, 136))]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=col)
    # blast light shimmering on the water under the gap
    for wy, wl in [(water_y + 8, 44), (water_y + 16, 30), (water_y + 24, 20)]:
        d.line([(cx - wl // 2, wy), (cx + wl // 2, wy)], fill=(214, 130, 40),
               width=2)
    d.text((x0 + 10, y0 + 8), "KERCH CROSSING", font=fnt(SANS_B, 12),
           fill=(255, 255, 255))
    d.text((x0 + 10, y1 - 22), "A span down — the bridge to Crimea",
           font=fnt(SANS_R, 11), fill=(214, 224, 238))
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_lead(d, y):
    top = y
    d.text((MX, y), LEAD_KICK, font=fnt(SANS_B, 13), fill=RED)
    y += 22
    lx, lw = MX, 600
    y = para(d, lx, y, LEAD_HEAD, fnt(SERIF_B, 30), lw, leading=4, max_lines=2)
    y += 4
    y = para(d, lx, y, LEAD_DECK, fnt(SERIF_R, 15), lw, fill=SOFTINK,
             leading=4, max_lines=2)
    y += 4
    d.text((lx, y), LEAD_BYLINE, font=fnt(SERIF_I, 12), fill=GREY)
    draw_kerch(d, 656, top, W - MX - 656, 168)
    return max(y + 16, top + 168)


# ---------------------------------------------------------------- secondary illustrations
def mini_flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 34, 52))
    for i in range(0, 7, 2):
        d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                    fill=(240, 240, 240))
    d.rectangle([x, y, x + w * 0.42, y + h * 0.55], fill=(28, 48, 96))
    for r in range(3):
        for c in range(4):
            d.ellipse([x + 3 + c * 5, y + 3 + r * 5, x + 5 + c * 5, y + 5 + r * 5],
                      fill=(255, 255, 255))


def mini_flag_jp(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.ellipse([x + w // 2 - 7, y + h // 2 - 7, x + w // 2 + 7, y + h // 2 + 7],
              fill=(188, 0, 45))


def mini_flag_in(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h // 3], fill=(255, 153, 51))
    d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(255, 255, 255))
    d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(19, 136, 8))
    d.ellipse([x + w // 2 - 6, y + h // 2 - 6, x + w // 2 + 6, y + h // 2 + 6],
              outline=(0, 56, 120), width=1)


def mini_flag_au(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 40, 104))
    for sx, sy in [(w - 12, 8), (w - 20, 16), (w - 8, 22), (w - 16, 28)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    d.ellipse([x + w // 2 - 3, y + h - 12, x + w // 2 + 3, y + h - 6],
              fill=(255, 255, 255))


def draw_panel_quad(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(238, 228, 200))
    flags = [(mini_flag_us, "USA"), (mini_flag_jp, "JAPAN"),
             (mini_flag_in, "INDIA"), (mini_flag_au, "AUSTRALIA")]
    fw, fh, gap = 62, 38, 12
    total = 4 * fw + 3 * gap
    sx = x0 + (w - total) // 2
    lab = fnt(SANS_B, 8)
    for i, (fn, name) in enumerate(flags):
        fx = sx + i * (fw + gap)
        fn(d, fx, y0 + 16, fw, fh)
        d.rectangle([fx, y0 + 16, fx + fw, y0 + 16 + fh], outline=INK, width=1)
        d.text((fx + fw // 2, y0 + 58), name, font=lab, fill=SOFTINK, anchor="ma")


def draw_panel_apec(d, x0, y0, w, h):
    # dusk sky in bands, then a lit Shenzhen skyline
    sky = [(242, 196, 130), (226, 164, 122), (196, 130, 128), (150, 120, 140)]
    bh = h // len(sky)
    for i, col in enumerate(sky):
        d.rectangle([x0, y0 + i * bh, x0 + w, y0 + (i + 1) * bh], fill=col)
    d.ellipse([x0 + w - 62, y0 + 8, x0 + w - 34, y0 + 36], fill=(206, 64, 44))
    base = y0 + h
    for bx, bw, bhgt in [(8, 34, 34), (48, 26, 48), (80, 30, 40),
                         (116, 24, 56), (146, 34, 44), (186, 28, 38),
                         (220, 30, 50), (256, 26, 30)]:
        d.rectangle([x0 + bx, base - bhgt, x0 + bx + bw, base], fill=(38, 52, 78))
        for wy in range(base - bhgt + 6, base - 4, 9):
            for wx in range(x0 + bx + 5, x0 + bx + bw - 4, 9):
                if (wx * 7 + wy * 13) % 5 < 2:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(240, 200, 90))
    d.text((x0 + 10, y0 + 6), "APEC", font=fnt(SANS_B, 11), fill=(255, 255, 255))


def draw_panel_nvda(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(13, 59, 34))
    for gy in range(1, 4):
        yy = y0 + gy * h // 4
        d.line([(x0 + 8, yy), (x0 + w - 8, yy)], fill=(30, 90, 55), width=1)
    pts = [(x0 + 14, y0 + h - 16), (x0 + 62, y0 + h - 34),
           (x0 + 110, y0 + h - 26), (x0 + 158, y0 + h - 46),
           (x0 + 206, y0 + h - 52), (x0 + 254, y0 + h - 58),
           (x0 + w - 12, y0 + h - 62)]
    d.polygon(pts + [(x0 + w - 12, y0 + h - 4), (x0 + 14, y0 + h - 4)],
              fill=(24, 96, 58))
    d.line(pts, fill=(110, 220, 130), width=3, joint="curve")
    for px, py in pts[1:-1]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
    d.text((x0 + 12, y0 + 8), "NVDA", font=fnt(SANS_B, 13), fill=(255, 255, 255))
    d.text((x0 + w - 12, y0 + h - 16), "+112% YoY", font=fnt(SANS_B, 11),
           fill=(110, 220, 130), anchor="ra")
    d.text((x0 + 12, y0 + h - 16), "$115.8bn revenue", font=fnt(SANS_R, 9),
           fill=(170, 210, 180))


PANELS = {"quad": draw_panel_quad, "apec": draw_panel_apec, "nvda": draw_panel_nvda}


def draw_secondaries(d, y):
    col_w, gap = 306, 19
    bottom = y
    for i, sec in enumerate(SECONDARIES):
        x0 = MX + i * (col_w + gap)
        PANELS[sec["kind"]](d, x0, y, col_w, 72)
        d.rectangle([x0, y, x0 + col_w, y + 72], outline=INK, width=1)
        ty = y + 80
        d.text((x0, ty), sec["kick"], font=fnt(SANS_B, 11), fill=RED)
        ty += 16
        ty = para(d, x0, ty, sec["head"], fnt(SERIF_B, 15), col_w,
                  leading=2, max_lines=3)
        ty += 2
        ty = para(d, x0, ty, sec["stand"], fnt(SANS_R, 11), col_w,
                  fill=GREY, leading=2, max_lines=1)
        bottom = max(bottom, ty)
    return bottom


# ---------------------------------------------------------------- story grid + ticker
def draw_grid(d, y):
    d.text((MX, y), "AROUND THE WORLD", font=fnt(SANS_B, 13), fill=INK)
    d.text((W - MX, y), "18 MORE STORIES", font=fnt(SANS_R, 11), fill=GREY,
           anchor="ra")
    y += 20
    col_w, gap, row_h = 306, 19, 37
    kick_f, head_f = fnt(SANS_B, 9), fnt(SANS_R, 11)
    for row in range(6):
        for col in range(3):
            num, kick, head = GRID[row * 3 + col]
            x0 = MX + col * (col_w + gap)
            yy = y + row * row_h
            if num is not None:
                d.ellipse([x0, yy + 1, x0 + 15, yy + 16], fill=RED)
                d.text((x0 + 7.5, yy + 8), str(num), font=fnt(SANS_B, 9),
                       fill=(255, 255, 255), anchor="mm")
            else:
                d.ellipse([x0 + 4, yy + 6, x0 + 10, yy + 12], fill=GREY)
            tx = x0 + 21
            d.text((tx, yy), kick, font=kick_f, fill=RED)
            para(d, tx, yy + 12, head, head_f, col_w - 21, leading=1,
                 max_lines=2)
    return y + 6 * row_h


def draw_ticker(d, y):
    f_tick = fnt(SANS_R, 10)
    sep = "   •   "
    lines, cur = [], ""
    for item in TICKER:
        trial = f"{cur}{sep}{item}" if cur else item
        if d.textlength(trial, font=f_tick) <= W - 2 * MX - 20:
            cur = trial
        else:
            lines.append(cur)
            cur = item
    if cur:
        lines.append(cur)
    strip_h = 6 + len(lines) * 14 + 6
    d.rectangle([MX, y, W - MX, y + strip_h], fill=(17, 17, 17))
    for li, ln in enumerate(lines):
        d.text((MX + 10, y + 3 + li * 14), ln, font=f_tick, fill=(240, 240, 240))
    return y + strip_h, len(lines)


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = draw_masthead(d)
    y = draw_map(img, y + 8, 188)
    y = draw_lead(d, y + 8)
    y += 10
    rule(d, y, width=1)
    y = draw_secondaries(d, y + 10)
    y += 8
    rule(d, y, width=1)
    y = draw_grid(d, y + 8)
    y += 4
    y = double_rule(d, y)
    final_y, tick_lines = draw_ticker(d, y + 6)
    print("ticker lines:", tick_lines, "final y:", final_y)
    return img, final_y


def main():
    img, final_y = build()
    if final_y > H - 4:
        print(f"WARNING: content overflows by {final_y - (H - 4)}px", file=sys.stderr)
    here = os.path.dirname(os.path.abspath(__file__))
    img.save(os.path.join(here, "entry.png"))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        img.save(os.path.join(out_dir, "entry.png"))
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
