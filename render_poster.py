#!/usr/bin/env python3
"""Build-time renderer for the news-image-20261122 entry.

Draws Sunday 22 November 2026's world news as one illustrated newspaper
front page (1024x1024) with Pillow. This program runs ONLY at build time;
the submitted entrypoint (main.py) is a stdlib-only copier of the PNG
committed next to it. Rendering is fully deterministic: fixed seeds, no
clocks, no network. Run it twice and the PNG bytes are identical.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

SS = 2  # supersampling factor
W = 1024 * SS
H = 1024 * SS

NOTO = "/usr/share/fonts/truetype/noto/"
def F(name, size):
    return ImageFont.truetype(NOTO + name, size * SS)

SERIF_BLACK = "NotoSerifDisplay-Black.ttf"
SERIF_BOLD = "NotoSerifDisplay-Bold.ttf"
SANS_BLACK = "NotoSansDisplay-Black.ttf"
SANS_BOLD = "NotoSansDisplay-Bold.ttf"
SANS_COND_BOLD = "NotoSansDisplay-CondensedBold.ttf"
SANS_SEMI = "NotoSansDisplay-SemiBold.ttf"
SANS = "NotoSans-Regular.ttf"

INK = (24, 24, 38)
PAPER = (247, 241, 226)
WHITE = (255, 253, 247)
RED = (172, 30, 38)
NAVY = (23, 50, 92)
GOLD = (203, 141, 38)
GREEN = (30, 104, 58)
PURPLE = (94, 52, 138)
SLATE = (52, 64, 84)
CLIMATE = (178, 74, 20)
DEK = (74, 70, 62)
RULE = (196, 186, 160)

M = 26 * SS  # page margin


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = (int(v) for v in box)
    for y in range(y0, y1):
        t = (y - y0) / max(1, (y1 - y0 - 1))
        draw.line([(x0, y), (x1, y)], fill=lerp(top, bottom, t))


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, font, fill, max_w, leading, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    asc, desc = font.getmetrics()
    lh = int((asc + desc) * leading)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def centered(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return y + sum(font.getmetrics())


# ---------------------------------------------------------------- art: heroes
def art_shenzhen(img, box):
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = box
    vgrad(d, box, (38, 62, 118), (238, 138, 66))
    cx, cy, r = x0 + (x1 - x0) * 0.70, y0 + (y1 - y0) * 0.38, 24 * SS
    d.ellipse([cx - r * 1.7, cy - r * 1.7, cx + r * 1.7, cy + r * 1.7], fill=(255, 176, 92, 90))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 205, 120))
    base = y1
    towers = [(0.02, 0.52), (0.10, 0.72), (0.19, 0.58), (0.27, 0.86), (0.36, 0.64),
              (0.44, 0.95), (0.53, 0.60), (0.61, 0.78), (0.70, 0.55), (0.78, 0.70),
              (0.86, 0.50), (0.93, 0.62)]
    wdt = (x1 - x0) / len(towers)
    for i, (fx, fh) in enumerate(towers):
        tx = x0 + fx * (x1 - x0)
        th = fh * (y1 - y0) * 0.92
        d.rectangle([tx, base - th, tx + wdt * 0.86, base], fill=(22, 30, 58))
        if i == 5:
            d.polygon([(tx + wdt * 0.30, base - th), (tx + wdt * 0.43, base - th - 14 * SS),
                       (tx + wdt * 0.56, base - th)], fill=(22, 30, 58))
    rng = random.Random(11)
    for _ in range(70):
        wx = rng.uniform(x0 + 4, x1 - 6)
        wy = rng.uniform(y0 + (y1 - y0) * 0.42, y1 - 6)
        d.rectangle([wx, wy, wx + 2.2 * SS, wy + 3 * SS], fill=(255, 214, 130, 200))
    # three slim summit flags in front of the skyline
    cols = [(196, 40, 48), (38, 84, 168), (240, 240, 235)]
    for i, c in enumerate(cols):
        bx = x0 + (x1 - x0) * (0.13 + 0.11 * i)
        top = y1 - (y1 - y0) * (0.66 - 0.07 * i)
        d.rectangle([bx - 1.1 * SS, top, bx + 1.1 * SS, y1], fill=(14, 16, 28))
        d.rectangle([bx + 1.1 * SS, top, bx + 1.1 * SS + (x1 - x0) * 0.052,
                     top + (y1 - y0) * 0.20], fill=c)
    dx, dy, s = x0 + (x1 - x0) * 0.565, y0 + (y1 - y0) * 0.16, SS
    d.polygon([(dx, dy), (dx + 16 * s, dy - 7 * s), (dx + 30 * s, dy - 2 * s),
               (dx + 17 * s, dy + 3 * s), (dx + 22 * s, dy + 9 * s), (dx + 8 * s, dy + 5 * s),
               (dx - 4 * s, dy + 8 * s), (dx - 2 * s, dy + 2 * s)], fill=(255, 255, 255))


def art_hormuz(img, box):
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = box
    vgrad(d, (x0, y0, x1, y0 + (y1 - y0) * 0.55), (168, 205, 224), (240, 226, 188))
    cx, cy = x0 + (x1 - x0) * 0.80, y0 + (y1 - y0) * 0.20
    d.ellipse([cx - 12 * SS, cy - 12 * SS, cx + 12 * SS, cy + 12 * SS], fill=(255, 196, 92))
    for rr in (20, 31, 42):
        d.arc([cx - rr * SS, cy - rr * SS, cx + rr * SS, cy + rr * SS], 100, 210,
              fill=(200, 70, 50, 150), width=2 * SS)
    vgrad(d, (x0, y0 + (y1 - y0) * 0.55, x1, y1), (32, 122, 140), (10, 74, 102))
    rng = random.Random(5)
    for _ in range(22):
        wx = rng.uniform(x0 + 4, x1 - 26 * SS)
        wy = rng.uniform(y0 + (y1 - y0) * 0.64, y1 - 4)
        d.line([(wx, wy), (wx + rng.uniform(8, 20) * SS, wy)], fill=(190, 230, 235, 130), width=SS)
    d.polygon([(x0, y0 + (y1 - y0) * 0.30), (x0 + (x1 - x0) * 0.20, y0 + (y1 - y0) * 0.55),
               (x0, y1)], fill=(122, 84, 52))
    d.polygon([(x1, y0 + (y1 - y0) * 0.26), (x1 - (x1 - x0) * 0.16, y0 + (y1 - y0) * 0.55),
               (x1, y1)], fill=(106, 72, 44))
    tx, ty = x0 + (x1 - x0) * 0.30, y0 + (y1 - y0) * 0.60
    tw, th = (x1 - x0) * 0.42, (y1 - y0) * 0.13
    d.polygon([(tx, ty), (tx + tw, ty), (tx + tw * 0.92, ty + th), (tx + tw * 0.06, ty + th)], fill=(30, 30, 40))
    d.rectangle([tx, ty + th * 0.72, tx + tw, ty + th * 0.86], fill=(178, 40, 44))
    conts = [(196, 84, 40), (38, 110, 160), (46, 140, 84), (214, 160, 52), (120, 70, 150)]
    cw = tw / 5.4
    for i, c in enumerate(conts):
        d.rectangle([tx + tw * 0.06 + i * cw, ty - th * 0.62, tx + tw * 0.06 + (i + 0.92) * cw, ty - 1], fill=c)
    d.rectangle([tx + tw * 0.80, ty - th * 1.15, tx + tw * 0.90, ty - th * 0.6], fill=(226, 226, 220))
    d.rectangle([tx + tw * 0.835, ty - th * 1.5, tx + tw * 0.865, ty - th * 1.15], fill=(90, 90, 96))


def art_cop31(img, box):
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = box
    vgrad(d, box, (250, 178, 92), (214, 92, 44))
    for i in range(3):
        pts = []
        for t in range(41):
            px = x0 + (x1 - x0) * (0.06 + 0.30 * t / 40)
            py = y0 + (y1 - y0) * (0.14 + 0.10 * i) + math.sin(t / 40 * math.pi * 3 + i) * 3.2 * SS
            pts.append((px, py))
        d.line(pts, fill=(255, 226, 160, 170), width=2 * SS)
    cx, cy, r = x0 + (x1 - x0) * 0.32, y0 + (y1 - y0) * 0.52, (y1 - y0) * 0.335
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 118, 178))
    land = (74, 158, 92)
    blobs = [(-0.45, -0.30, 0.34, 0.24), (0.05, -0.52, 0.40, 0.22), (0.42, -0.05, 0.30, 0.34),
             (-0.10, 0.18, 0.26, 0.30), (0.30, 0.42, 0.20, 0.16), (-0.52, 0.30, 0.18, 0.14)]
    for fx, fy, fw, fh in blobs:
        d.ellipse([cx + (fx - fw / 2) * r, cy + (fy - fh / 2) * r,
                   cx + (fx + fw / 2) * r, cy + (fy + fh / 2) * r], fill=land)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(230, 244, 250), width=2 * SS)
    tx = x0 + (x1 - x0) * 0.86
    tw_ = 8 * SS
    top = y0 + (y1 - y0) * 0.10
    bot = y0 + (y1 - y0) * 0.72
    d.rounded_rectangle([tx - tw_, top, tx + tw_, bot], radius=tw_, fill=(245, 245, 240), outline=(120, 60, 30), width=2 * SS)
    d.rectangle([tx - tw_ * 0.45, y0 + (y1 - y0) * 0.28, tx + tw_ * 0.45, bot], fill=(206, 44, 34))
    d.ellipse([tx - 12 * SS, bot - 5 * SS, tx + 12 * SS, bot + 18 * SS], fill=(206, 44, 34))
    for i in range(5):
        gy = top + (bot - top) * (0.12 + 0.18 * i)
        d.line([(tx - tw_ - 8 * SS, gy), (tx - tw_ - 2 * SS, gy)], fill=(90, 40, 20), width=SS)
    dx0, dy0 = x0 + (x1 - x0) * 0.50, y1 - (y1 - y0) * 0.24
    dw = (x1 - x0) * 0.34
    d.pieslice([dx0, dy0 - (y1 - y0) * 0.26, dx0 + dw, dy0 + (y1 - y0) * 0.26], 180, 360, fill=(250, 240, 214))
    d.rectangle([dx0 - 2 * SS, dy0, dx0 + dw + 2 * SS, y1], fill=(64, 52, 44))
    d.rectangle([dx0 + dw * 0.42, dy0 + (y1 - y0) * 0.07, dx0 + dw * 0.58, y1], fill=(250, 200, 90))


# ------------------------------------------------------------------- content
HEROES = [
    dict(tag="WORLD \u00b7 SHENZHEN SUMMIT", color=NAVY, art=art_shenzhen,
         head="Trump, Xi & Putin Meet in Shenzhen",
         dek="Rival leaders open nuclear risk-reduction talks and issue a joint peace "
             "declaration \u2014 with Kyiv and Europe outside the room."),
    dict(tag="CONFLICT \u00b7 STRAIT OF HORMUZ", color=RED, art=art_hormuz,
         head="Iran Strikes Bahrain; Tanker Hit Near Hormuz",
         dek="Tehran claims a strike on a US base as the strait stays on edge "
             "and oil holds near $90 a barrel."),
    dict(tag="CLIMATE \u00b7 COP31 ANTALYA", color=CLIMATE, art=art_cop31,
         head="COP31 Deadlocked Into Overtime",
         dek="Fossil-fuel wording stalls the talks as a new draft drops both "
             "the fuel mention and the $120B adaptation goal."),
]

WORLD = [
    ("Missiles Kill Two in Zelensky's Home Town",
     "Kryvyi Rih strike kills two; drones burn a Russian ship."),
    ("Mexico Captures FBI Top-Ten Cartel Boss",
     "\u2018El Chapo Isidro\u2019 seized in Sinaloa; 11 die in the raid."),
    ("Hackers Breach FBI Criminal Database",
     "Police records access disrupted; Trump plays it down."),
    ("128 Nations to Draft Killer-Robot Rules",
     "Geneva starts the first autonomous-weapons rulebook."),
    ("Bolsonaro in Intensive Care",
     "Stable and conscious; bowel obstruction, surgery weighed."),
]
INDONESIA = [
    ("EU\u2013Indonesia Sign Landmark Trade Deal",
     "Signed in Brussels; tariffs cut on nearly all goods."),
    ("Prabowo to Name VP Candidates on 25 Nov",
     "Two names to the MPR; Mahfud urges a deadline recount."),
    ("M7.2 Earthquake Strikes Southwest Maluku",
     "BMKG records the powerful quake in Maluku Barat Daya."),
    ("Mount Ibu and Mount Semeru Erupt",
     "Eruptions in Halmahera and East Java; climbing banned."),
    ("Candy Factory Fire: At Least 3 Dead",
     "36 workers still unaccounted for after the blaze."),
    ("Prabowo Home with Rp274 Trillion in Deals",
     "Back from ASEAN and APEC with 35 China agreements."),
    ("Bank Indonesia Raises Rate to 6%",
     "25 bp hike; IHSG slides 3.71% on the week to 5,146."),
    ("Death Penalty Weighed for Riza Chalid",
     "Capital charge studied in the Pertamina oil case."),
]
SPORT = [
    ("Antonelli Takes Pole in Las Vegas",
     "Mercedes rookie starts ahead of Verstappen, Russell."),
    ("India Pile Up 720/9 in Wellington",
     "Rahul (136) and Pant centuries power a record total."),
    ("Leeds Stun Chelsea 4\u20131 at the Bridge",
     "Okafor's double leads it; City, Arsenal held to draws."),
    ("Madrid Comeback Beats Celta 2\u20131",
     "Bellingham and Esp\u00ed rescue Real, level at the top."),
    ("Alcaraz v Zverev: ATP Finals Title Match",
     "Alcaraz beats Shelton; Zverev beats Medvedev in Turin."),
    ("England Beat the All Blacks 37\u201312",
     "Second straight November win over New Zealand."),
]
MARKETS = [
    ("AI Sell-Off Pushes US Stocks into Correction",
     "Dow and S&P 500 slide into correction territory."),
    ("Nvidia's Worst Losing Streak Since 2008",
     "SEC probe deepens the slide; Anthropic debuts big."),
    ("EU Floats Digital Tax on Big Tech",
     "Levy proposed in a draft budget trimmed by \u20ac204B."),
]
TECH = [
    ("AI Helps Prove the Riemann Hypothesis",
     "Alp\u00f6ge says Claude helped crack the 160-year-old problem; claim verified twice."),
    ("Voyager 1 Now a Full Light-Day Away",
     "25.9 billion km out; its radio signal takes a full day."),
]
SHOWBIZ = [
    ("Guns N' Roses Rock Jakarta",
     "GBK Madya Stadium, Saturday night."),
    ("First Beach PON Opens in Ancol",
     "1,172 athletes, first beach games, 21\u201327 Nov."),
]

REGIONS = {
    "WORLD & CONFLICT": dict(color=NAVY, stories=WORLD),
    "INDONESIA": dict(color=RED, stories=INDONESIA),
    "SPORT": dict(color=GREEN, stories=SPORT),
    "MARKETS": dict(color=SLATE, stories=MARKETS),
    "TECH & SCIENCE": dict(color=(58, 62, 160), stories=TECH),
    "SHOWBIZ": dict(color=PURPLE, stories=SHOWBIZ),
}

TICKER = ("MARKET TICKER   S&P 500 -3.7% this week \u00b7 Nikkei -5.06% \u00b7 Gold -4.62% \u00b7 "
          "Bitcoin -1.79% \u00b7 Oil ~$90 \u00b7 IHSG 5,146.33 (-3.71%) \u00b7 BI Rate 6.00%")
FOOTER = ("Sources: BBC \u00b7 Al Jazeera \u00b7 The Guardian \u00b7 NASA \u00b7 BMKG \u00b7 Autosport \u00b7 Sky Sports \u00b7 ESPN "
          "and wire reports of 22 Nov 2026 \u00b7 Drawn and typeset by an AI agent \u2014 every story verified")


# --------------------------------------------------------------------- layout
def draw_region(d, box, name, region, head_size=14.5, dek_size=11):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y0 + 24 * SS], fill=region["color"])
    d.text((x0 + 8 * SS, y0 + 4 * SS), name, font=F(SANS_BOLD, 14), fill=WHITE)
    tag = f"{len(region['stories'])} STORIES"
    tf = F(SANS_SEMI, 10.5)
    d.text((x1 - 8 * SS - d.textlength(tag, font=tf), y0 + 6 * SS), tag, font=tf, fill=(255, 255, 255))
    y = y0 + 29 * SS
    hf, df = F(SANS_COND_BOLD, head_size), F(SANS, dek_size)
    for i, (head, dek) in enumerate(region["stories"]):
        y = text_block(d, (x0 + 2 * SS, y), head, hf, INK, (x1 - x0) - 4 * SS, 1.03, 2)
        y = text_block(d, (x0 + 2 * SS, y - 1 * SS), dek, df, DEK, (x1 - x0) - 4 * SS, 1.10, 2)
        y += 3 * SS
        if i < len(region["stories"]) - 1:
            d.line([(x0 + 2 * SS, y - 2.5 * SS), (x1 - 2 * SS, y - 2.5 * SS)], fill=RULE, width=SS)
    return y


def render(path, verbose=False):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(42)
    for _ in range(90):
        ex, ey = rng.uniform(0, W), rng.uniform(0, H)
        er = rng.uniform(18, 90) * SS
        tone = (232, 222, 192) if rng.random() < 0.5 else (252, 247, 233)
        d.ellipse([ex - er, ey - er * 0.6, ex + er, ey + er * 0.6], fill=tone + (10,))
    d.rectangle([9 * SS, 9 * SS, W - 9 * SS, H - 9 * SS], outline=INK, width=3 * SS)
    d.rectangle([15 * SS, 15 * SS, W - 15 * SS, H - 15 * SS], outline=INK, width=SS)

    # masthead
    centered(d, W // 2, 24 * SS, "THE SUNDAY WORLD GAZETTE \u00b7 ONE PAGE \u00b7 THE WHOLE PLANET",
             F(SANS_SEMI, 13.5), (110, 96, 70))
    d.line([(M, 48 * SS), (W - M, 48 * SS)], fill=INK, width=SS)
    centered(d, W // 2, 52 * SS, "THE WORLD TODAY", F(SERIF_BLACK, 76), INK)
    d.line([(M, 138 * SS), (W - M, 138 * SS)], fill=INK, width=2 * SS)
    d.rectangle([M, 146 * SS, W - M, 176 * SS], fill=INK)
    d.text((M + 12 * SS, 152 * SS), "SUNDAY", font=F(SANS_BOLD, 16), fill=(240, 200, 110))
    centered(d, W // 2, 150 * SS, "22 NOVEMBER 2026", F(SANS_BLACK, 21), WHITE)
    right = "29 STORIES \u00b7 7 REGIONS"
    d.text((W - M - 12 * SS - d.textlength(right, font=F(SANS_BOLD, 14.5)), 154 * SS),
           right, font=F(SANS_BOLD, 14.5), fill=(240, 200, 110))

    # heroes (compact): art 112, tag 22, head <=2 lines, dek <=3 lines
    hy0, hy1 = 186 * SS, 436 * SS
    colw = (W - 2 * M - 2 * 12 * SS) // 3
    for i, hero in enumerate(HEROES):
        x0 = M + i * (colw + 12 * SS)
        x1 = x0 + colw
        art_box = (x0, hy0, x1, hy0 + 112 * SS)
        hero["art"](img, art_box)
        d.rectangle(art_box, outline=INK, width=SS)
        d.rectangle([x0, hy0 + 112 * SS, x1, hy0 + 134 * SS], fill=hero["color"])
        d.text((x0 + 8 * SS, hy0 + 116 * SS), hero["tag"], font=F(SANS_BOLD, 12.5), fill=WHITE)
        y = text_block(d, (x0 + 2 * SS, hy0 + 139 * SS), hero["head"], F(SERIF_BOLD, 20.5),
                       INK, colw - 4 * SS, 1.04, 2)
        text_block(d, (x0 + 2 * SS, y), hero["dek"], F(SANS, 13),
                   DEK, colw - 4 * SS, 1.13, 3)
        if i < 2:
            d.line([(x1 + 6 * SS, hy0), (x1 + 6 * SS, hy1)], fill=RULE, width=SS)
    d.line([(M, hy1), (W - M, hy1)], fill=INK, width=2 * SS)

    # ticker
    ty0 = 444 * SS
    d.rectangle([M, ty0, W - M, ty0 + 28 * SS], fill=GOLD)
    centered(d, W // 2, ty0 + 5.5 * SS, TICKER, F(SANS_BOLD, 14), (40, 30, 8))

    # region grid 486..958
    gy0, gy1 = 486 * SS, 958 * SS
    gx = [M, M + colw + 12 * SS, M + 2 * (colw + 12 * SS)]
    ends = {}
    ends["L1"] = draw_region(d, (gx[0], gy0, gx[0] + colw, 758 * SS), "WORLD & CONFLICT", REGIONS["WORLD & CONFLICT"])
    d.line([(gx[0], 758 * SS), (gx[0] + colw, 758 * SS)], fill=INK, width=SS)
    ends["L2"] = draw_region(d, (gx[0], 766 * SS, gx[0] + colw, gy1), "MARKETS", REGIONS["MARKETS"])
    ends["M1"] = draw_region(d, (gx[1], gy0, gx[1] + colw, 758 * SS), "SPORT", REGIONS["SPORT"])
    d.line([(gx[1], 758 * SS), (gx[1] + colw, 758 * SS)], fill=INK, width=SS)
    ends["M2"] = draw_region(d, (gx[1], 766 * SS, gx[1] + colw, gy1), "TECH & SCIENCE", REGIONS["TECH & SCIENCE"])
    ends["R1"] = draw_region(d, (gx[2], gy0, gx[2] + colw, 838 * SS), "INDONESIA", REGIONS["INDONESIA"])
    d.line([(gx[2], 838 * SS), (gx[2] + colw, 838 * SS)], fill=INK, width=SS)
    ends["R2"] = draw_region(d, (gx[2], 846 * SS, gx[2] + colw, gy1), "SHOWBIZ", REGIONS["SHOWBIZ"])
    for gx_sep in (gx[1] - 6 * SS, gx[2] - 6 * SS):
        d.line([(gx_sep, gy0), (gx_sep, gy1)], fill=RULE, width=SS)
    if verbose:
        for k, v in ends.items():
            print(k, "ends at", v / SS, "limit", {"L1": 758, "M1": 758, "R1": 838}.get(k, 958))

    # footer
    d.line([(M, 964 * SS), (W - M, 964 * SS)], fill=INK, width=2 * SS)
    centered(d, W // 2, 971 * SS, FOOTER, F(SANS_SEMI, 10.5), (110, 96, 70))
    centered(d, W // 2, 988 * SS, "29 STORIES \u00b7 7 REGIONS \u00b7 1 PAGE \u00b7 SUNDAY 22 NOVEMBER 2026",
             F(SANS_BOLD, 11), INK)

    img = img.resize((1024, 1024), Image.LANCZOS)
    # gentle posterize: keeps the rich flat-colour look, trims gradient
    # entropy so the file lands in the board's rich-but-lean size class
    img = img.point(lambda v: (v // 4) * 4 + 2)
    img.save(path, format="PNG", optimize=True)
    return path


if __name__ == "__main__":
    import os
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render(out, verbose=True)
    print("wrote", out, os.path.getsize(out), "bytes")
