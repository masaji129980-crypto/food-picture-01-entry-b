#!/usr/bin/env python3
"""Draw 'Sate Grill Night' — satay skewers grilling over glowing charcoal.
Original illustration drawn entirely in code with Pillow. No copied assets.
Saves entry.png (1024x1024) in this directory."""
import math, random
from PIL import Image, ImageDraw, ImageFilter

random.seed(20261114)
W = H = 1024
img = Image.new("RGB", (W, H), (12, 8, 6))
d = ImageDraw.Draw(img, "RGBA")

def vgrad(top, bottom):
    g = Image.new("RGB", (1, H))
    gd = ImageDraw.Draw(g)
    for y in range(H):
        t = y / (H - 1)
        gd.point((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return g.resize((W, H))

def glow(cx, cy, r, color, peak=200):
    """Soft radial glow on its own layer, composited additively-ish."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    steps = 24
    for i in range(steps, 0, -1):
        rr = r * i / steps
        a = int(peak * (1 - i / steps) ** 2)
        ld.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=color + (a,))
    return layer.filter(ImageFilter.GaussianBlur(18))

def rrect(dr, box, rad, fill, outline=None, width=1):
    dr.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=width)

# ---- background: deep night sky warming toward the fire ----
img = vgrad((16, 10, 14), (46, 22, 10))
d = ImageDraw.Draw(img, "RGBA")

# faint stars / sparks in the upper sky
for _ in range(70):
    x = random.uniform(0, W); y = random.uniform(0, 380)
    a = random.randint(30, 130); s = random.uniform(0.6, 1.8)
    d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 220, 160, a))

# warm firelight wash across the whole lower scene
img.paste(Image.alpha_composite(img.convert("RGBA"), glow(512, 760, 620, (255, 120, 30), 110)), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# ---- charcoal grill bed ----
# grill body: dark metal rim with warm rim-light
rrect(d, [70, 640, 954, 960], 26, (38, 26, 18), outline=(120, 70, 30), width=4)
rrect(d, [86, 656, 938, 944], 20, (22, 14, 10))
# inner charcoal pit
rrect(d, [110, 676, 914, 920], 16, (10, 6, 4))

# glowing embers: clustered lumps of hot charcoal
ember_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ed = ImageDraw.Draw(ember_layer)
for _ in range(190):
    x = random.uniform(130, 894); y = random.uniform(700, 900)
    rx = random.uniform(12, 34); ry = random.uniform(8, 20)
    hot = random.random()
    if hot < 0.10:
        col = (255, random.randint(140, 180), 40, random.randint(170, 235))
    elif hot < 0.30:
        col = (225, 80, 22, random.randint(130, 200))
    else:
        col = (46 + random.randint(0, 22), 26, 20, random.randint(170, 220))
    # irregular charcoal lump (jittered polygon, not a round pebble)
    npts = 7
    poly = []
    for k in range(npts):
        a = 2 * math.pi * k / npts
        rr = random.uniform(0.7, 1.15)
        poly.append((x + math.cos(a) * rx * rr, y + math.sin(a) * ry * rr))
    ed.polygon(poly, fill=col)
    # bright crack on some embers
    if random.random() < 0.4:
        ed.line([x - rx * 0.6, y, x + rx * 0.6, y + random.uniform(-3, 3)],
                fill=(255, 200, 90, 220), width=2)
ember_layer = ember_layer.filter(ImageFilter.GaussianBlur(1.2))
img.paste(Image.alpha_composite(img.convert("RGBA"), ember_layer), (0, 0))
d = ImageDraw.Draw(img, "RGBA")
# heat glow just above the coals
img.paste(Image.alpha_composite(img.convert("RGBA"), glow(512, 780, 430, (255, 110, 25), 130)), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# flame tongues licking up between the skewers
flame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fd = ImageDraw.Draw(flame)
for fx in (250, 420, 600, 770):
    h = random.randint(90, 150); wdt = random.randint(26, 40)
    pts = []
    for i in range(9):
        t = i / 8
        yy = 700 - t * h
        xx = fx + math.sin(t * math.pi * 2.2) * wdt * 0.35 * (1 - t)
        pts.append((xx, yy))
    # teardrop flame: outer orange, inner yellow
    fd.polygon([(fx - wdt, 705), (fx - wdt * 0.4, 700 - h * 0.55),
                (fx, 700 - h), (fx + wdt * 0.4, 700 - h * 0.55), (fx + wdt, 705)],
               fill=(255, 130, 20, 170))
    fd.polygon([(fx - wdt * 0.5, 705), (fx - wdt * 0.2, 700 - h * 0.4),
                (fx, 700 - h * 0.72), (fx + wdt * 0.2, 700 - h * 0.4), (fx + wdt * 0.5, 705)],
               fill=(255, 210, 90, 200))
flame = flame.filter(ImageFilter.GaussianBlur(6))
img.paste(Image.alpha_composite(img.convert("RGBA"), flame), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# ---- satay skewers ----
def meat_cube(cx, cy, s, ang, shade):
    """One juicy, charred satay cube: shaded body, char marks, gloss, sauce sheen."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    # base cube with warm gradient feel via two overlapping rounded rects
    base = (172 + shade, 96 + shade // 2, 34)
    dark = (96 + shade, 48, 18)
    ld.rounded_rectangle([cx - s, cy - s * 0.82, cx + s, cy + s * 0.82], radius=s * 0.45, fill=base + (255,))
    # bottom shade
    ld.rounded_rectangle([cx - s, cy + s * 0.15, cx + s, cy + s * 0.82], radius=s * 0.45, fill=dark + (200,))
    # charred grill stripes (thin, so the meat still reads as meat)
    for k in (-0.3, 0.3):
        x0 = cx + k * s
        ld.line([x0 - 3, cy - s * 0.8, x0 + 3, cy + s * 0.8], fill=(52, 22, 10, 170), width=max(3, s // 9))
    # caramelised edges
    ld.arc([cx - s, cy - s * 0.82, cx + s, cy + s * 0.82], 200, 340, fill=(110, 52, 18, 170), width=max(3, s // 8))
    # glossy highlight (juice): small warm sheen, top-left only
    ld.ellipse([cx - s * 0.5, cy - s * 0.6, cx + s * 0.05, cy - s * 0.15], fill=(255, 196, 110, 130))
    ld.ellipse([cx - s * 0.15, cy - s * 0.45, cx + s * 0.3, cy - s * 0.2], fill=(255, 225, 160, 90))
    # peanut sauce drizzle over the top
    ld.arc([cx - s * 0.8, cy - s * 0.5, cx + s * 0.8, cy + s * 0.6], 300, 60, fill=(214, 138, 44, 235), width=max(4, s // 7))
    layer = layer.rotate(ang, center=(cx, cy), resample=Image.BICUBIC)
    return layer

def skewer(y, angle_deg, cubes, x0, x1, shade):
    """Bamboo stick with meat cubes, slight perspective."""
    ang = math.radians(angle_deg)
    dx = math.cos(ang); dy = math.sin(ang)
    # bamboo stick
    d.line([x0, y, x1, y + (x1 - x0) * dy / dx], fill=(214, 164, 96, 255), width=9)
    d.line([x0, y + 3, x1, y + 3 + (x1 - x0) * dy / dx], fill=(150, 104, 52, 255), width=3)
    # pointed tip
    tipx = x1 + 26
    tipy = y + (x1 - x0) * dy / dx + 26 * dy / dx
    d.polygon([(x1, y + (x1 - x0) * dy / dx - 5), (tipx, tipy), (x1, y + (x1 - x0) * dy / dx + 5)],
              fill=(228, 182, 110, 255))
    # meat cubes along the stick
    for i, (fx, s) in enumerate(cubes):
        cx = x0 + fx * (x1 - x0)
        cy = y + fx * (x1 - x0) * dy / dx
        layer = meat_cube(int(cx), int(cy), s, angle_deg, shade + (i % 2) * 8 - 8)
        img.paste(Image.alpha_composite(img.convert("RGBA"), layer), (0, 0))

# three skewers fanning across the grill, spaced so rows do not overlap
skewer(350, 7, [(0.16, 46), (0.34, 50), (0.52, 48), (0.70, 46), (0.86, 42)], 150, 880, -18)
skewer(465, -6, [(0.14, 54), (0.32, 58), (0.50, 56), (0.68, 54), (0.85, 48)], 130, 900, -6)
skewer(580, 10, [(0.18, 60), (0.36, 64), (0.54, 62), (0.72, 60), (0.87, 54)], 170, 860, 10)
d = ImageDraw.Draw(img, "RGBA")
# (no stray lines: the sticks themselves carry the composition)

# ---- smoke curls rising from the grill ----
smoke = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(smoke)
for base_x, height, wdt, alpha in ((300, 330, 60, 70), (520, 380, 70, 85), (730, 320, 55, 65), (640, 300, 45, 55)):
    pts = []
    for i in range(40):
        t = i / 39
        yy = 560 - t * height
        xx = base_x + math.sin(t * math.pi * 2.6 + base_x) * (18 + t * 46)
        pts.append((xx, yy))
    for i in range(len(pts) - 1):
        t = i / (len(pts) - 1)
        w = int(wdt * (0.35 + t * 0.9))
        a = int(alpha * (1 - t * 0.75))
        sd.line([pts[i], pts[i + 1]], fill=(200, 190, 185, a), width=w)
smoke = smoke.filter(ImageFilter.GaussianBlur(14))
img.paste(Image.alpha_composite(img.convert("RGBA"), smoke), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# rising sparks above the coals
for _ in range(46):
    x = random.uniform(180, 850); y = random.uniform(300, 640)
    s = random.uniform(1.0, 2.6); a = random.randint(120, 255)
    d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 190, 90, a))
    d.line([x - s * 2.2, y, x + s * 2.2, y], fill=(255, 210, 130, a // 2), width=1)

# ---- peanut sauce bowl, bottom left foreground ----
bx, by = 175, 880
d.ellipse([bx - 95, by - 18, bx + 95, by + 55], fill=(16, 9, 5, 255))          # shadow
d.ellipse([bx - 92, by - 42, bx + 92, by + 42], fill=(74, 44, 24, 255))        # bowl rim
d.ellipse([bx - 78, by - 32, bx + 78, by + 32], fill=(196, 118, 34, 255))      # sauce surface
d.ellipse([bx - 60, by - 24, bx + 20, by + 4], fill=(226, 158, 62, 200))       # sauce sheen
d.ellipse([bx - 78, by - 32, bx + 78, by + 32], outline=(52, 30, 16, 255), width=3)
# crushed peanut sprinkles
for _ in range(26):
    px = bx + random.uniform(-62, 62); py = by + random.uniform(-22, 22)
    d.ellipse([px - 3, py - 2, px + 3, py + 2], fill=(238, 196, 130, 230))
# chili flecks
for _ in range(8):
    px = bx + random.uniform(-55, 55); py = by + random.uniform(-20, 20)
    d.ellipse([px - 3, py - 2, px + 3, py + 2], fill=(190, 40, 20, 230))
# lime wedge beside the bowl: a flat half-disc, rind out
d.pieslice([bx + 108, by - 34, bx + 182, by + 40], 180, 360, fill=(150, 185, 55, 255))
d.pieslice([bx + 116, by - 26, bx + 174, by + 32], 180, 360, fill=(215, 238, 125, 255))
d.line([bx + 145, by - 30, bx + 145, by + 36], fill=(150, 185, 55, 255), width=3)
d.arc([bx + 108, by - 34, bx + 182, by + 40], 180, 360, fill=(110, 150, 40, 255), width=3)
# kecap drizzle across the grill edge, bottom right
for i, yy in enumerate((985, 1000)):
    d.arc([700, yy - 40, 980, yy + 40], 180, 360, fill=(40, 18, 8, 220), width=5)

# ---- gentle vignette to lead the eye to the food ----
vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vig)
vd.ellipse([-180, -140, W + 180, H + 140], outline=(0, 0, 0, 150), width=260)
vig = vig.filter(ImageFilter.GaussianBlur(60))
img.paste(Image.alpha_composite(img.convert("RGBA"), vig), (0, 0))

# subtle grain for a photographic feel (kept light so the PNG stays small)
grain = Image.effect_noise((W, H), 14).convert("L")
img = Image.composite(img, Image.blend(img, Image.new("RGB", (W, H), (128, 128, 128)), 0.03),
                      grain.point(lambda v: 255 if v > 200 else 0))

img.save("entry.png", optimize=True)
print("saved entry.png")
