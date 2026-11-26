#!/usr/bin/env python3
"""Page art for the zombie-apocalypse food mod in the Stardew Delight page style.

  py make_page.py [base_url]

Writes into docs/:
  banner.png/.gif/.webp        1536x512, the supply-crate loop (items hop out one by one)
  icon-512.png, icon-animated.gif/.webp
  promo-tile.png/.gif/.webp    768x352
  clips/pantry.gif/.webp       all 17 items, then each one with its name and effect
  desc/title-<section>.png/.webp, desc/divider.png/.webp
  description.md / description.html   page text (images from base_url/docs/...)
  page_preview.html            the page with local images, to look at it before uploading
Item textures are read from ../art/textures.
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gifkit  # noqa: E402
import pa  # noqa: E402

TEX = HERE.parent / "art" / "textures"
DOCS = HERE / "docs"
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://raw.githubusercontent.com/USER/REPO/main").rstrip("/")

MOD_TOP, MOD_MAIN = "APOCALYPSE", "PANTRY"
MOD_NAME = "Apocalypse Pantry"
TAGLINE = "EAT. SURVIVE. REPEAT."
TAG_ACCENT_FROM = 14

# ---------------------------------------------------------------- palette
INK = "#0B0F0C"
SKY = "#1B2420"
SKY_DIM, SKY_MID, GLINT = "#2C3832", "#45544B", "#B9C9A8"
CITY = ["#111714", "#161E1A"]
WINDOW = ["#C9A54A", "#7A6A3A"]
MOON = ["#5E1A16", "#8E2A20", "#B8402C", "#D8603E", "#F08A5E"]
RUST = dict(bands=["#FFE7C0", "#FFC983", "#FFC983", "#FFC983", "#F49A47", "#F49A47", "#F49A47", "#C95C2C", "#C95C2C",
                   "#C95C2C"], extrude=["#6E2A16", "#45190E"])
TOXIC = dict(bands=["#F2FFC0", "#C3EA6C", "#C3EA6C", "#C3EA6C", "#8ED14E", "#8ED14E", "#8ED14E", "#5BB23E", "#5BB23E",
                    "#5BB23E"], extrude=["#236B33", "#17492D"])
ACCENT = "#8ED14E"
WOOD = ["#2A1F18", "#45362A", "#5F4B3A", "#7C6550", "#A38A6A", "#C7B08A"]
IRON = ["#23272B", "#3A4046", "#59626A", "#86909A", "#B9C1C8"]
DIRT = ["#1E1712", "#2B211A", "#3B2E23"]
BONE = ["#F2EAD2", "#E2D6B4", "#C9B98E"]


def C(h):
    return pa.hexrgb(h) + (255,)


def new(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def put(im, x, y, c):
    if 0 <= x < im.width and 0 <= y < im.height:
        im.putpixel((x, y), C(c))


def outlined(im, ink=INK):
    bb = im.getbbox()
    im = im.crop(bb)
    out = new(im.width + 2, im.height + 2)
    solid = {(x, y) for y in range(im.height) for x in range(im.width) if im.getpixel((x, y))[3] > 0}
    for x, y in solid:
        for dx, dy in pa.N8:
            if (x + dx, y + dy) not in solid:
                out.putpixel((x + dx + 1, y + dy + 1), C(ink))
    out.alpha_composite(im, (1, 1))
    return out


def item(name):
    return Image.open(TEX / f"{name}.png").convert("RGBA")


def twinkle(im, x, y, big, c1=GLINT, c2=SKY_MID):
    if big:
        put(im, x, y, c1)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            put(im, x + dx, y + dy, c2)
    else:
        put(im, x, y, c2)


def sparkle(im, x, y, size):
    """Four-point glint, size 1..3."""
    put(im, x, y, "#FFFFFF")
    for d in range(1, size + 1):
        c = "#FFF3B0" if d < size else "#E8C85A"
        for dx, dy in ((d, 0), (-d, 0), (0, d), (0, -d)):
            put(im, x + dx, y + dy, c)


def moon(im, cx, cy, r):
    for y in range(cy - r - 1, cy + r + 2):
        for x in range(cx - r - 1, cx + r + 2):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            if d <= r:
                lx = (x + 0.5 - cx + r * 0.4) ** 2 + (y + 0.5 - cy + r * 0.4) ** 2
                k = 4 if lx < (r * 0.45) ** 2 else 3 if lx < (r * 0.9) ** 2 else 2 if d < r - 0.8 else 1
                put(im, x, y, MOON[k])
    for (dx, dy, s) in ((2, -1, 1), (-2, 2, 1), (1, 3, 0)):
        put(im, cx + dx, cy + dy, MOON[1])
        if s:
            put(im, cx + dx + 1, cy + dy, MOON[1])


def skyline(im, y_base, seed, frame=0, n=72, x0=0, x1=None):
    """Ruined city along the bottom: broken roofs, a few lit windows that flicker."""
    x1 = im.width if x1 is None else x1
    rnd = random.Random(seed)
    x = x0
    while x < x1:
        w = rnd.randrange(6, 15)
        h = rnd.randrange(4, 12)
        col = CITY[rnd.randrange(2)]
        top = y_base - h
        for xx in range(x, min(x + w, x1)):
            broken = rnd.random() < 0.25
            t = top + (rnd.randrange(1, 3) if broken else 0)
            for yy in range(t, im.height):
                put(im, xx, yy, col)
        for wy in range(top + 2, y_base, 3):
            for wx in range(x + 2, min(x + w - 1, x1), 3):
                r = rnd.random()
                if r < 0.12:
                    lit = ((frame // 6 + wx + wy) % 9) != 0
                    put(im, wx, wy, WINDOW[0] if lit else WINDOW[1])
        x += w + rnd.randrange(0, 2)


def sky_layer(w, h, frame, n, seed, keep_out=lambda x, y: False, city=True, moon_at=None):
    im = Image.new("RGBA", (w, h), C(SKY))
    rnd = random.Random(seed)
    taken = set()
    for _ in range(w * h // 260):
        x, y = rnd.randrange(2, w - 2), rnd.randrange(2, h - 14)
        if (x // 4, y // 4) in taken or keep_out(x, y):
            continue
        taken.add((x // 4, y // 4))
        put(im, x, y, SKY_DIM if rnd.random() < 0.7 else SKY_MID)
    tw = [(rnd.randrange(4, w - 4), rnd.randrange(3, h - 18)) for _ in range(9)]
    for i, (x, y) in enumerate(tw):
        if keep_out(x, y):
            continue
        ph = (frame + i * n // len(tw)) % n
        twinkle(im, x, y, ph < n // 3)
    if moon_at:
        moon(im, *moon_at)
    if city:
        skyline(im, h - 3, seed + 1, frame, n)
    return im


# ---------------------------------------------------------------- the crate scene (64x64 texels)
FRAMES_PER = 24
HOPPERS = ["canned_stew", "energy_drink", "herbal_tea_canteen"]
FRAMES = FRAMES_PER * len(HOPPERS)
FPS = 12
STILL = FRAMES_PER + 11
RIM = 31                                   # item pixels at or below this row are inside the crate
BOTTOM = {0: 52, 1: 52, 2: 52, 3: 44, 4: 36, 5: 30, 6: 26, 7: 24, 8: 23, 9: 23, 10: 22, 11: 22, 12: 22, 13: 23,
          14: 23, 15: 22, 16: 22, 17: 24, 18: 28, 19: 34, 20: 42, 21: 50, 22: 52, 23: 52}
SQUASH = {4: (0.82, 1.18), 5: (0.9, 1.1), 8: (1.08, 0.92), 9: (1.04, 0.96), 18: (0.9, 1.1)}
LID_TILT = {3: 6, 4: 9, 5: 5, 6: 2, 21: -3, 22: 2}


def crate_back():
    im = new(64, 64)
    # ground shadow + grass
    for y in range(55, 62):
        for x in range(2, 62):
            if ((x + 0.5 - 32) / 29) ** 2 + ((y + 0.5 - 58) / 3.4) ** 2 <= 1:
                put(im, x, y, DIRT[1] if y > 57 else DIRT[2])
    for gx, gh in ((5, 3), (7, 2), (57, 3), (59, 2), (55, 2)):
        for k in range(gh):
            put(im, gx + (k % 2), 57 - k, "#4D5A33" if k else "#3A4628")
    # inside of the open crate + back rim
    for y in range(26, 31):
        for x in range(10, 54):
            put(im, x, y, WOOD[4] if y == 26 else WOOD[2] if y == 27 else DIRT[0])
    for x in range(10, 54):
        put(im, x, 25, INK)
    for x in (9, 54):
        for y in range(25, 31):
            put(im, x, y, INK)
    # stock peeking out: can lids and a pouch corner
    for cx in (17, 24, 41):
        for x in range(cx - 3, cx + 4):
            put(im, x, 29, IRON[3] if abs(x - cx) < 3 else IRON[2])
            put(im, x, 30, IRON[2])
        for x in range(cx - 2, cx + 3):
            put(im, x, 28, IRON[4] if x < cx else IRON[3])
    for x in range(46, 52):
        for y in range(28, 31):
            put(im, x, y, "#6B7340" if y > 28 else "#8A9256")
    return im


def lid(tilt):
    """The lid propped open behind the crate, pivot near its bottom-right."""
    im = new(64, 64)
    d = ImageDraw.Draw(im)
    # hinged on the back rim and leaning back: bottom edge on the rim, top edge pushed right by the tilt
    sh = 6 + tilt * 0.5
    top_y = 10 - tilt * 0.3
    bl, br = (12.0, 25.0), (51.0, 25.0)
    tl, tr = (12.0 + sh, top_y), (51.0 + sh, top_y)
    d.polygon([bl, br, tr, tl], fill=C(WOOD[3]))
    for s in (1 / 3, 2 / 3):                              # board seams across the lid
        y = 25 + (top_y - 25) * s
        x0 = 12 + sh * s
        d.line([(x0, y), (x0 + 39, y)], fill=C(WOOD[1]))
        d.line([(x0, y + 1), (x0 + 39, y + 1)], fill=C(WOOD[4]))
    d.line([tl, tr], fill=C(WOOD[5]))
    d.line([bl, tl], fill=C(WOOD[4]))
    d.line([br, tr], fill=C(WOOD[2]))
    for s in (0.2, 0.8):                                  # hinges
        x = 12 + 39 * s
        d.rectangle([x - 1, 22, x + 1, 24], fill=C(IRON[3]))
    return outlined_in_place(im)


def outlined_in_place(im):
    out = new(im.width, im.height)
    solid = {(x, y) for y in range(im.height) for x in range(im.width) if im.getpixel((x, y))[3] > 0}
    for x, y in solid:
        for dx, dy in pa.N8:
            if (x + dx, y + dy) not in solid:
                put(out, x + dx, y + dy, INK)
    out.alpha_composite(im)
    return out


def crate_front():
    im = new(64, 64)
    x0, x1, y0, y1 = 9, 54, 31, 57
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            edge = x in (x0, x0 + 1, x1 - 1, x1) or y in (y0, y0 + 1, y1 - 1, y1)
            if edge:
                c = WOOD[4] if y in (y0, y0 + 1) else WOOD[1] if y in (y1 - 1, y1) or x in (x1 - 1, x1) else WOOD[3]
            else:
                board = (y - y0 - 2) // 8
                yy = (y - y0 - 2) % 8
                c = WOOD[2] if yy == 7 else WOOD[4] if yy == 0 else WOOD[3]
                if (x * 7 + board * 13) % 23 == 0 and 1 < yy < 6:
                    c = WOOD[2]
            put(im, x, y, c)
    # diagonal brace
    for t in range(0, 101):
        x = round(x0 + 3 + (x1 - x0 - 6) * t / 100)
        y = round(y1 - 3 - (y1 - y0 - 6) * t / 100)
        put(im, x, y, WOOD[5])
        put(im, x, y + 1, WOOD[4])
        put(im, x, y + 2, WOOD[2])
    # corner brackets and nails
    for bx, by in ((x0, y0), (x1 - 3, y0), (x0, y1 - 3), (x1 - 3, y1 - 3)):
        for dy in range(4):
            for dx in range(4):
                if (dx in (0, 3) or dy in (0, 3)) or (dx, dy) == (1, 1):
                    put(im, bx + dx, by + dy, IRON[3] if dy < 2 else IRON[2])
        put(im, bx + 1, by + 1, IRON[4])
    # stencil: a can and the number 17 in faded paint
    paint = "#BFB28A"
    can_px = ["#.#.#", "#.#.#", "#####", ".###.", "..#..", "..#..", "..#.."]   # a fork
    for r, row in enumerate(can_px):
        for c, v in enumerate(row):
            if v == "#":
                put(im, 16 + c, 40 + r, paint)
    seven = ["#.###", "#...#", "#..#.", "#..#.", "#.#..", "#.#..", "#.#.."]
    for r, row in enumerate(seven):
        for c, v in enumerate(row):
            if v == "#":
                put(im, 43 + c, 40 + r, paint)
    out = new(64, 64)
    solid = {(x, y) for y in range(64) for x in range(64) if im.getpixel((x, y))[3] > 0}
    for x, y in solid:
        for dx, dy in pa.N8:
            if (x + dx, y + dy) not in solid:
                put(out, x + dx, y + dy, INK)
    out.alpha_composite(im)
    return out


_BACK, _FRONT = None, None


def scene_layers(f):
    """(under, top) 64x64 layers for frame f: back + lid + hopping item, then the crate front."""
    global _BACK, _FRONT
    if _BACK is None:
        _BACK, _FRONT = crate_back(), crate_front()
    k, lf = divmod(f, FRAMES_PER)
    name = HOPPERS[k]
    under = new(64, 64)
    under.alpha_composite(lid(LID_TILT.get(lf, 0)))
    under.alpha_composite(_BACK)
    spr = outlined(item(name))
    sx, sy = SQUASH.get(lf, (1.0, 1.0))
    if (sx, sy) != (1.0, 1.0):
        spr = spr.resize((max(1, round(spr.width * sx)), max(1, round(spr.height * sy))), Image.NEAREST)
    bottom = BOTTOM[lf]
    x = 32 - spr.width // 2
    y = bottom - spr.height
    hop = new(64, 64)
    hop.alpha_composite(spr, (x, max(-spr.height, y)) if y > -64 else (x, 0))
    for yy in range(RIM, 64):          # hide what is still inside the crate
        for xx in range(64):
            hop.putpixel((xx, yy), (0, 0, 0, 0))
    under.alpha_composite(hop)
    if 9 <= lf <= 15:
        s = (1, 2, 3, 2, 3, 2, 1)[lf - 9]
        sparkle(under, x + spr.width + 1, y + 2, s)
    if lf in (21, 22):                  # dust when it lands back in the crate
        for px, py in ((12, 29), (52, 29), (8, 27), (56, 27)):
            put(under, px + (lf - 21) * (-1 if px < 32 else 1), py - (lf - 21), "#6A6A62")
    top = _FRONT.copy()
    return under, top


# ---------------------------------------------------------------- banner
BW, BH, GRID = 1536, 512, 8
ART_SCALE = 7
ART_ORIGIN = (1232 - 32 * ART_SCALE, 256 - 32 * ART_SCALE)


def lettering():
    top = pa.title_sprite(MOD_TOP, RUST, INK)
    main = pa.title_sprite(MOD_MAIN, TOXIC, INK)
    tag = pa.label_sprite(TAGLINE, lambda i: ACCENT if i > TAG_ACCENT_FROM else "#FFFFFF", INK)
    return [(top, 6, (72, 97)), (main, 10, (70, 193)), (tag, 6, (74, 361))]


def banner_frames():
    letters = lettering()

    def keep_out(x, y):
        return x < 112 and 8 <= y < 54
    frames = []
    for i in range(FRAMES):
        sky = sky_layer(BW // GRID, BH // GRID, i, FRAMES, 1987, keep_out, moon_at=(110, 12, 6))
        out = pa.scaled(sky, GRID)
        for img, s, pos in letters:
            out.alpha_composite(pa.scaled(img, s), pos)
        under, top = scene_layers(i)
        out.alpha_composite(pa.scaled(under, ART_SCALE), ART_ORIGIN)
        out.alpha_composite(pa.scaled(top, ART_SCALE), ART_ORIGIN)
        frames.append(out)
    return frames


def save_anim(frames, stem, fps, corners=None):
    rgb = [f.convert("RGB") for f in frames]
    key = corners.point(lambda v: 255 - v) if corners is not None else None
    n = gifkit.write_gif(rgb, stem.with_suffix(".gif"), fps, key_mask=key)
    rgba = []
    for f in frames:
        g = f.copy()
        if corners is not None:
            g.putalpha(corners)
        rgba.append(g)
    gifkit.write_webp(rgba, stem.with_suffix(".webp"), fps)
    return n


# ---------------------------------------------------------------- headers, divider, tile, icon (x4 texels)
SCALE = 4
HW = 384
NAVY = SKY
RING = "#121814"
HEAD = dict(bands=RUST["bands"], extrude=["#3A2A1E", "#3A2A1E"])
SECTIONS = [
    ("features", "FEATURES", "canned_beans", "energy_drink"),
    ("effects", "EFFECTS", "zombie_jerky", "herbal_tea_canteen"),
    ("food", "FOOD", "survivor_stew", "mre_ration"),
    ("credits", "CREDITS", "hardtack", "chocolate_ration"),
    ("license", "LICENSE", "jerky", "condensed_milk"),
]
DIVIDER = ("canned_peaches", "pickled_cucumbers")
SKULL = ["...#######...",
         "..#########..",
         ".###########.",
         ".###########.",
         ".#ooo###ooo#.",
         ".#ooo###ooo#.",
         ".#####o#####.",
         "..#########..",
         "...#o#o#o#...",
         "...#######..."]


def skull():
    im = new(len(SKULL[0]), len(SKULL))
    for y, row in enumerate(SKULL):
        for x, ch in enumerate(row):
            if ch == "#":
                put(im, x, y, BONE[0] if y < 3 else BONE[1] if y < 7 else BONE[2])
            elif ch == "o":
                put(im, x, y, "#3A1A14")
    return outlined(im)


def panel(im, x0, y0, x1, y1, fill, outline=INK, ring=RING, r=2, thick=True):
    for y in range(y0, y1 + 1):
        k = min(y - y0, y1 - y)
        for x in range(x0, x1 + 1):
            j = min(x - x0, x1 - x)
            if k == 0:
                c = outline if j >= r else None
            elif k <= r and thick:
                lo = r - k
                c = None if j < lo else outline if j <= lo + 1 else ring if j == lo + 2 else fill
            elif k < r:
                lo = r - k
                c = None if j < lo else outline if j == lo else fill
            else:
                c = outline if j == 0 else (ring if (thick and j == 1 and k == r + 1) else fill)
            if c:
                put(im, x, y, c)
    return im


def plank(im, x0, x1, y0):
    """Weathered board with nails and a strand of barbed wire, 7 rows."""
    rows = [INK, WOOD[4], WOOD[3], WOOD[3], WOOD[3], WOOD[2], INK]
    for x in range(x0, x1 + 1):
        for k, c in enumerate(rows):
            put(im, x, y0 + k, c)
    for x in range(x0, x1 + 1):
        if x % 28 == 0:
            for k in range(1, 6):
                put(im, x, y0 + k, WOOD[1])
            put(im, x + 1, y0 + 1, WOOD[5])
            for nx in (x - 3, x + 3):
                if x0 <= nx <= x1:
                    put(im, nx, y0 + 3, IRON[4])
                    put(im, nx, y0 + 4, WOOD[1])
    for board in range(x0 // 28, x1 // 28 + 1):
        rnd = random.Random(board * 104729 + 7)
        for _ in range(3):
            row = rnd.choice((2, 3, 3, 4))
            start = board * 28 + rnd.randrange(6, 18)
            for x in range(start, start + rnd.randrange(3, 8)):
                if x0 <= x <= x1 and x % 28 not in (0, 25, 26, 27, 1, 2, 3, 4):
                    put(im, x, y0 + row, WOOD[2])
    # barbed wire just above the board: a thin strand with a barb every 14 texels
    for x in range(x0 + 4, x1 - 3):
        put(im, x, y0 - 1 + (1 if (x // 7) % 2 else 0), IRON[2])
        if x % 14 == 0:
            for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
                put(im, x + dx, y0 - 1 + dy + (1 if (x // 7) % 2 else 0), IRON[3])
    return im


def glints(im, pts):
    for (x, y, big) in pts:
        if big:
            put(im, x, y, "#9BD86A")
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                put(im, x + dx, y + dy, "#3E5A34")
        else:
            put(im, x, y, "#3E5A34")


def header(text, left, right, h=22):
    im = new(HW, h)
    cy = h // 2
    lcap, rcap = outlined(item(left)), outlined(item(right))
    lx, rx = 1, HW - 1 - rcap.width
    plank(im, lx + lcap.width // 2, rx + rcap.width // 2, cy - 3)
    im.alpha_composite(lcap, (lx, cy - lcap.height // 2))
    im.alpha_composite(rcap, (rx, cy - rcap.height // 2))
    if text:
        label = pa.title_sprite(text, HEAD, INK)
        tx = (HW - label.width) // 2
        x0, x1 = tx - 11, tx + label.width - 1 + 11
        panel(im, x0, 1, x1, h - 2, NAVY)
        glints(im, [(x1 - 7, 5, True), (x0 + 8, 12, True), (x0 + 4, 15, False), (x1 - 8, 12, False)])
        im.alpha_composite(label, (tx, 4))
    return im


def divider():
    im = header(None, *DIVIDER, h=20)
    s = skull()
    im.alpha_composite(s, ((HW - s.width) // 2, 10 - s.height // 2))
    return im


def save_static(im, stem, scale=SCALE):
    big = pa.scaled(im, scale)
    big.save(stem.with_suffix(".png"), optimize=True)
    big.save(stem.with_suffix(".webp"), lossless=True, method=6)
    return big


TW, TH = 192, 88
TILE_ART = (8, 12)
TILE_TEXT_X = 78


def badge(text):
    label = pa.scaled(pa.label_sprite(text, "#FFFFFF", "#000000"), 3)
    units = -(-(label.width + 32) // SCALE)
    pill = new(units, 13)
    panel(pill, 0, 0, units - 1, 12, "#0F1411", r=2, thick=False)
    big = pa.scaled(pill, SCALE)
    big.alpha_composite(label, ((big.width - label.width) // 2, SCALE + (44 - label.height) // 2))
    return big


def tile_frames():
    top = pa.title_sprite(MOD_TOP, RUST, INK)
    main = pa.title_sprite(MOD_MAIN, TOXIC, INK)
    tag = pa.scaled(pa.label_sprite(TAGLINE, lambda i: ACCENT if i > TAG_ACCENT_FROM else "#FFFFFF", INK), 3)
    pill = badge("SURVIVAL FOOD MOD")

    def keep_out(x, y):
        return (TILE_TEXT_X - 2 <= x < 186 and 10 <= y < 78) or (x < 76 and y > 8)
    frames = []
    for i in range(FRAMES):
        sky = sky_layer(TW, TH, i, FRAMES, 2024, keep_out, city=False, moon_at=(60, 9, 4))
        tile = new(TW, TH)
        panel(tile, 0, 0, TW - 1, TH - 1, SKY, r=3)
        mask = tile.getchannel("A")
        body = Image.composite(sky, new(TW, TH), mask)
        # keep the panel outline on top of the sky
        edge = new(TW, TH)
        panel(edge, 0, 0, TW - 1, TH - 1, SKY, r=3)
        for y in range(TH):
            for x in range(TW):
                p = edge.getpixel((x, y))
                if p[3] and p[:3] != pa.hexrgb(SKY):
                    body.putpixel((x, y), p)
        body.alpha_composite(top, (TILE_TEXT_X, 15))
        body.alpha_composite(main, (TILE_TEXT_X, 30))
        under, art = scene_layers(i)
        body.alpha_composite(under, TILE_ART)
        body.alpha_composite(art, TILE_ART)
        big = pa.scaled(body, SCALE)
        big.alpha_composite(tag, (TILE_TEXT_X * SCALE, 48 * SCALE))
        big.alpha_composite(pill, (TILE_TEXT_X * SCALE - 4, 60 * SCALE))
        frames.append(big)
    return frames


def icon_frames():
    frames = []
    for i in range(FRAMES):
        base = new(64, 64)
        panel(base, 0, 0, 63, 63, SKY, r=3)
        sky = sky_layer(64, 64, i, FRAMES, 77, lambda x, y: x > 8 and y > 20, city=False, moon_at=(12, 11, 4))
        body = Image.composite(sky, new(64, 64), base.getchannel("A"))
        for y in range(64):
            for x in range(64):
                p = base.getpixel((x, y))
                if p[3] and p[:3] != pa.hexrgb(SKY):
                    body.putpixel((x, y), p)
        under, top = scene_layers(i)
        under = under.crop((0, 0, 64, 62))
        body.alpha_composite(under, (0, 1))
        body.alpha_composite(top.crop((0, 0, 64, 62)), (0, 1))
        frames.append(body)
    return frames


# ---------------------------------------------------------------- pantry clip
ITEMS = [  # id, English name, short effect line (SMALL font: upper case, no %)
    ("canned_beans", "CANNED BEANS", "STAMINA 3:00"),
    ("canned_stew", "CANNED STEW", "STRENGTH I, STAMINA 5:00"),
    ("canned_peaches", "CANNED PEACHES", "SPEED I, REGENERATION I"),
    ("condensed_milk", "CONDENSED MILK", "ABSORPTION I, HASTE I"),
    ("energy_drink", "ENERGY DRINK", "ADRENALINE, THEN A CRASH"),
    ("bottled_water", "BOTTLED WATER", "CLEARS CRASH AND NAUSEA"),
    ("mre_ration", "MRE RATION", "STAMINA 8:00, RESISTANCE I"),
    ("protein_bar", "PROTEIN BAR", "STRENGTH I, FAST TO EAT"),
    ("hardtack", "HARDTACK", "STAMINA 1:00, CHEAP"),
    ("instant_noodles", "INSTANT NOODLES", "REGENERATION I, STAMINA"),
    ("jerky", "JERKY", "STRENGTH I 1:00"),
    ("zombie_jerky", "ZOMBIE JERKY", "UNDEAD SCENT 2:00"),
    ("grilled_rat", "GRILLED RAT", "FILLING, MAY POISON YOU"),
    ("pickled_cucumbers", "PICKLED CUCUMBERS", "CLEARS POISON AND NAUSEA"),
    ("herbal_tea_canteen", "HERBAL TEA CANTEEN", "CURES INFECTION"),
    ("survivor_stew", "SURVIVOR'S STEW", "RESISTANCE, REGEN, STAMINA"),
    ("chocolate_ration", "CHOCOLATE RATION", "SPEED I, HASTE I, ABSORPTION"),
]
CW, CH = 192, 80
SLOT = 20
GX, GY = (CW - 9 * SLOT) // 2, 14


def slot(im, x, y, sel=False):
    for yy in range(SLOT - 1):
        for xx in range(SLOT - 1):
            edge_tl = xx == 0 or yy == 0
            edge_br = xx == SLOT - 2 or yy == SLOT - 2
            c = "#0E1310" if edge_tl else "#3C4A40" if edge_br else "#243029"
            if sel and (xx in (0, SLOT - 2) or yy in (0, SLOT - 2)):
                c = "#C3EA6C"
            put(im, x + xx, y + yy, c)


def pantry_frames():
    REVEAL, SHOW = 2, 8
    total = len(ITEMS) * REVEAL + 4 + len(ITEMS) * SHOW
    title = pa.label_sprite("THE PANTRY: 17 ITEMS", lambda i: ACCENT if i > 11 else "#FFFFFF", INK)
    sprites = [item(n) for n, _, _ in ITEMS]
    frames = []
    for f in range(total):
        im = new(CW, CH)
        panel(im, 0, 0, CW - 1, CH - 1, SKY, r=3)
        im.alpha_composite(title, ((CW - title.width) // 2, 3))
        shown = min(len(ITEMS), f // REVEAL + 1)
        sel = None
        if f >= len(ITEMS) * REVEAL + 4:
            sel = (f - len(ITEMS) * REVEAL - 4) // SHOW
        for i in range(18):
            x, y = GX + (i % 9) * SLOT, GY + (i // 9) * SLOT
            slot(im, x, y, sel == i)
            if i < shown:
                pop = 1 if (i == shown - 1 and f < len(ITEMS) * REVEAL and f % REVEAL == 0) else 0
                im.alpha_composite(sprites[i], (x + 1, y + 1 - pop))
        if sel is not None:
            _, name, fx = ITEMS[sel]
            a = pa.label_sprite(name, "#FFE7C0", INK)
            b = pa.label_sprite(fx, ACCENT, INK)
            im.alpha_composite(a, ((CW - a.width) // 2, 57))
            im.alpha_composite(b, ((CW - b.width) // 2, 67))
        frames.append(pa.scaled(im, SCALE))
    return frames


# ---------------------------------------------------------------- page text
FOOD_ROWS = [
    ("Canned Beans", "6", "Stamina 3:00", "Leaves an empty can"),
    ("Canned Stew", "8", "Strength I 1:30, Stamina 5:00", "Leaves an empty can"),
    ("Canned Peaches", "5", "Speed I 1:00, Regeneration I 0:10", "Leaves an empty can"),
    ("Condensed Milk", "4", "Absorption I 2:00, Haste I 1:00", "Can be eaten when full; leaves an empty can"),
    ("Energy Drink", "1", "Adrenaline 0:45, then Crash 0:30", "Resets the time since you last slept; leaves an empty can"),
    ("Bottled Water", "0", "Regeneration I 0:05", "Clears Crash, Hunger and Nausea; leaves a glass bottle"),
    ("MRE Ration", "10", "Stamina 8:00, Resistance I 2:00", "Slow to eat, stacks to 8"),
    ("Protein Bar", "4", "Strength I 0:45", "Eaten in 0.8 s"),
    ("Hardtack", "3", "Stamina 1:00", "Cheap to craft"),
    ("Instant Noodles", "6", "Regeneration I 0:15, Stamina 2:00", "Made with bottled water"),
    ("Jerky", "6", "Strength I 1:00", "Eaten in 0.8 s; cooked beef or porkchop with sugar"),
    ("Zombie Jerky", "4", "Undead Scent 2:00, Nausea 0:05", "Rotten flesh in a smoker or on a campfire"),
    ("Grilled Rat", "5", "20% chance of Poison 0:10", "Gives the stick back"),
    ("Pickled Cucumbers", "3", "-", "Clears Poison and Nausea"),
    ("Herbal Tea Canteen", "2", "Regeneration I 0:10", "Cures Infection; leaves an empty canteen to refill"),
    ("Survivor's Stew", "10", "Resistance I 3:00, Regeneration I 0:20, Stamina 6:00", "In a bowl, stacks to 16"),
    ("Chocolate Ration", "5", "Speed I and Haste I 1:30, Absorption I 1:00", "-"),
]


def page_md(base):
    def img(path, alt=""):
        return f"![{alt}]({base}/docs/{path})"

    def title(key, alt):
        return img(f"desc/title-{key}.webp", alt)
    rows = "\n".join(f"| **{n}** | {h} | {e} | {o} |" for n, h, e, o in FOOD_ROWS)
    return f"""{img("banner.webp", MOD_NAME)}

**Food for the end of the world: canned stew, MREs, energy drinks and zombie jerky, each with its own way to keep you alive.**

{MOD_NAME} adds 17 survival foods to Minecraft and five effects built around a zombie apocalypse: an Infection you catch from zombies, a scent that makes the undead ignore you, and an adrenaline rush that comes with a crash.

{img("clips/pantry.webp", "The pantry")}

{title("features", "Features")}

- **17 survival foods.** Cans, rations, drinks and things you would only eat at the end of the world. Every item has its own 16×16 texture.
- **Infection.** Zombies can infect you when they hit you. Only the Herbal Tea Canteen cures it, so keep one on you.
- **Food that fits the moment.** Protein Bars are eaten in a blink for fights, MREs fill you for a long trip, Energy Drinks get you out of trouble and Zombie Jerky lets you walk past the horde.
- **Empty cans.** Canned food leaves an empty can: fill it again with new food or smelt it into an iron nugget.
- **Zombie loot.** Zombies you kill sometimes drop canned food, hardtack, an energy drink or bottled water.
- **Milk will not save you.** Infection survives milk and totems; the Herbal Tea Canteen is the only cure.

{title("effects", "Effects")}

| Effect | What it does |
| --- | --- |
| **Infection** | Caught from zombie, husk, drowned and zombie villager hits (10% on Normal, 25% on Hard). Makes you hungry faster; after 5 minutes adds Weakness, after 10 Slowness. If you die infected, a zombie with your name rises where you fell. |
| **Undead Scent** | Zombies and other undead ignore you until you attack them. |
| **Adrenaline** | Speed II and Jump Boost I. When it ends you get a Crash. |
| **Crash** | Slowness I and Mining Fatigue I. Water clears it. |
| **Stamina** | Hunger drains half as fast. |

{title("food", "Food")}

| Food | Hunger | Effects | Notes |
| --- | --- | --- | --- |
{rows}

{title("credits", "Credits")}

- Texture style inspired by **Farmer's Delight** by vectorwing.

{title("license", "License")}

{MOD_NAME} is released under the **MIT License**.

{img("desc/divider.webp")}
"""


def to_html(md):
    import html
    import re

    def inline(t):
        t = html.escape(t, quote=False)
        t = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        return t
    out, lines, i = [], md.strip().split("\n"), 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("- "):
            out.append("<ul>")
            while i < len(lines) and lines[i].startswith("- "):
                out.append(f"<li>{inline(lines[i][2:])}</li>")
                i += 1
            out.append("</ul>")
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr></thead><tbody>")
            for r in rows[2:]:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("</tbody></table>")
        else:
            out.append(f"<p>{inline(ln)}</p>")
            i += 1
    return "\n".join(out) + "\n"


PREVIEW_CSS = """body{background:#1d1f21;color:#e8e6e3;font:15px/1.55 'Segoe UI',Arial,sans-serif;margin:0}
main{max-width:1000px;margin:24px auto;background:#26282b;padding:24px 32px;border-radius:6px}
img{max-width:100%;image-rendering:pixelated}table{border-collapse:collapse;margin:8px 0}
td,th{border:1px solid #444;padding:6px 10px;vertical-align:top}th{background:#2f3236}strong{color:#fff}"""


def main():
    (DOCS / "desc").mkdir(parents=True, exist_ok=True)
    (DOCS / "clips").mkdir(parents=True, exist_ok=True)

    frames = banner_frames()
    corners = pa.stepped_corners(BW, BH)
    still = frames[STILL].copy()
    still.putalpha(corners)
    still.save(DOCS / "banner.png", optimize=True)
    n = save_anim(frames, DOCS / "banner", FPS, corners)
    print(f"banner: {len(frames)} frames, {n} colours, gif {(DOCS / 'banner.gif').stat().st_size // 1024} KiB")

    for key, text, l, r in SECTIONS:
        save_static(header(text, l, r), DOCS / "desc" / f"title-{key}")
    save_static(divider(), DOCS / "desc" / "divider")
    print(f"headers: {len(SECTIONS)} + divider")

    tf = tile_frames()
    tf[STILL].save(DOCS / "promo-tile.png", optimize=True)
    key = tf[STILL].getchannel("A").point(lambda v: 255 if v > 127 else 0)
    save_anim(tf, DOCS / "promo-tile", FPS, key)

    icf = icon_frames()
    pa.scaled(icf[STILL], 8).save(DOCS / "icon-512.png", optimize=True)
    big = [pa.scaled(f, 4) for f in icf]
    save_anim(big, DOCS / "icon-animated", FPS, big[0].getchannel("A").point(lambda v: 255 if v > 127 else 0))
    print(f"icon: gif {(DOCS / 'icon-animated.gif').stat().st_size // 1024} KiB")

    pf = pantry_frames()
    save_anim(pf, DOCS / "clips" / "pantry", 8, pf[0].getchannel("A").point(lambda v: 255 if v > 127 else 0))
    print(f"pantry clip: {len(pf)} frames")

    md = page_md(BASE)
    (DOCS / "description.md").write_text(md, encoding="utf-8")
    (DOCS / "description.html").write_text(to_html(md), encoding="utf-8")
    local = to_html(page_md("..")).replace('src="../docs/', 'src="')
    (DOCS / "page_preview.html").write_text(
        f"<!doctype html><meta charset=utf-8><title>{MOD_NAME}</title><style>{PREVIEW_CSS}</style><main>{local}</main>",
        encoding="utf-8")
    print("description.md, description.html, page_preview.html")


if __name__ == "__main__":
    main()
