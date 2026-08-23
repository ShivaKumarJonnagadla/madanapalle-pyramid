#!/usr/bin/env python3
"""Generate a shareable donation poster (PNG) for social media."""
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import pathlib

root = pathlib.Path(__file__).parent
IMG = root / "assets" / "img"
W, H = 1080, 1500
M = 72

# palette
INDIGO_TOP = (30, 24, 68)
INDIGO_BOT = (58, 38, 92)
GOLD = (233, 173, 40)
GOLD_SOFT = (240, 205, 110)
CREAM = (247, 240, 226)
MUTED = (200, 190, 168)
PANEL = (255, 253, 247)
INK = (34, 28, 46)

F = "/System/Library/Fonts/Supplemental/"
def gfont(size, bold=False, italic=False):
    name = "Georgia"
    if bold and italic: name += " Bold Italic"
    elif bold: name += " Bold"
    elif italic: name += " Italic"
    return ImageFont.truetype(F + name + ".ttf", size)
def uni(size):
    return ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", size)

img = Image.new("RGB", (W, H), INDIGO_TOP)
draw = ImageDraw.Draw(img)

# vertical gradient
for y in range(H):
    t = y / H
    r = int(INDIGO_TOP[0] + (INDIGO_BOT[0]-INDIGO_TOP[0])*t)
    g = int(INDIGO_TOP[1] + (INDIGO_BOT[1]-INDIGO_TOP[1])*t)
    b = int(INDIGO_TOP[2] + (INDIGO_BOT[2]-INDIGO_TOP[2])*t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# soft golden glow behind top
glow = Image.new("RGB", (W, H), INDIGO_TOP)
gd = ImageDraw.Draw(glow)
gd.ellipse([W//2-360, -260, W//2+360, 460], fill=(120, 92, 30))
glow = glow.filter(ImageFilter.GaussianBlur(120))
img = Image.blend(img, glow, 0.35)
draw = ImageDraw.Draw(img)

def ctext(y, text, font, fill, spacing=0):
    if spacing:
        total = sum(draw.textlength(ch, font=font)+spacing for ch in text) - spacing
        x = (W-total)/2
        for ch in text:
            draw.text((x, y), ch, font=font, fill=fill)
            x += draw.textlength(ch, font=font)+spacing
        return
    w = draw.textlength(text, font=font)
    draw.text(((W-w)/2, y), text, font=font, fill=fill)

def wrap_center(y, text, font, fill, maxw, lh):
    words = text.split()
    line, lines = "", []
    for w in words:
        test = (line+" "+w).strip()
        if draw.textlength(test, font=font) <= maxw:
            line = test
        else:
            lines.append(line); line = w
    if line: lines.append(line)
    for ln in lines:
        ctext(y, ln, font, fill); y += lh
    return y

def rounded(im, radius):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.size[0], im.size[1]], radius, fill=255)
    im.putalpha(mask)
    return im

def tile(path, box_w, box_h, radius=18):
    im = Image.open(path).convert("RGB")
    im = ImageOps.exif_transpose(im)
    im = ImageOps.fit(im, (box_w, box_h), Image.LANCZOS)
    return rounded(im, radius)

y = 58
# pyramid glyph
tri = [(W/2, y), (W/2-58, y+92), (W/2+58, y+92)]
draw.polygon(tri, outline=GOLD, width=5)
draw.line([(W/2-30, y+44),(W/2+30, y+44)], fill=(GOLD[0],GOLD[1],GOLD[2]), width=3)
y += 118

ctext(y, "MADANAPALLE  ·  ANNAMAYYA  ·  ANDHRA PRADESH", uni(24), GOLD_SOFT, spacing=4)
y += 46
ctext(y, "A Meditation Pyramid", gfont(72, bold=True), CREAM)
y += 82
ctext(y, "for the whole community", gfont(44, italic=True), GOLD_SOFT)
y += 92

# quote
draw.text((M-6, y-18), "“", font=gfont(120, bold=True), fill=(GOLD[0],GOLD[1],GOLD[2]))
y2 = wrap_center(y+18, "Quiet the mind, and the soul will speak.", gfont(40, italic=True), CREAM, W-2*M-40, 54)
ctext(y2+6, "Ma Jaya Sati Bhagavati", uni(24), MUTED)
y = y2 + 62

# photo montage 2x2
gap = 20
tw = (W - 2*M - gap)//2
th = 236
photos = [("team.jpg","Our team & well-wishers"),
          ("pooja-1.jpg","Bhoomi pooja"),
          ("foundation-1.jpg","Foundation work"),
          ("pillars-1.jpg","Pillar work")]
positions = [(M, y), (M+tw+gap, y), (M, y+th+gap), (M+tw+gap, y+th+gap)]
for (fn,_),(px,py) in zip(photos, positions):
    t = tile(IMG/fn, tw, th)
    img.paste(t, (px, py), t)
    draw.rounded_rectangle([px,py,px+tw,py+th], 18, outline=(GOLD[0],GOLD[1],GOLD[2]), width=3)
y = y + 2*th + gap + 40

# appeal
y = wrap_center(y, "The land is donated. Foundation, borewell and pillars are done, but the funds are now finished and work has paused.",
                uni(30), CREAM, W-2*M, 42)
y += 12
ctext(y, "Even ₹10 helps us complete it, and makes many smile.", uni(31), GOLD_SOFT)
y += 66

# donation panel
panel_h = 250
panel = Image.new("RGB", (W-2*M, panel_h), PANEL)
pr = rounded(panel.copy(), 24)
img.paste(pr, (M, y), pr)
pd = ImageDraw.Draw(img)
# QR
qr = Image.open(IMG/"upi-qr.jpg").convert("RGB")
qr = ImageOps.fit(qr, (196, 196), Image.LANCZOS)
img.paste(qr, (M+28, y+27))
tx = M+28+196+34
pd.text((tx, y+30), "SCAN TO DONATE", font=uni(24), fill=(GOLD[0]-20,120,20))
pd.text((tx, y+66), "UPI  6509092255@myapgb", font=uni(30), fill=INK)
pd.text((tx, y+108), "A/C 650910016995155", font=uni(24), fill=(80,74,90))
pd.text((tx, y+140), "IFSC UBIN00G7999 · AP Grameena Bank", font=uni(23), fill=(80,74,90))
pd.text((tx, y+182), "madanapalle-pyramid.vercel.app", font=uni(27), fill=(150,100,10))
y += panel_h + 34

# contacts
ctext(y, "President J. Anuradha  92469 83035   ·   Treasurer Subramanyam  99898 59591",
      uni(23), MUTED)
y += 40
ctext(y, "Madanapalle Pyramid Spiritual Society", uni(26), GOLD_SOFT)

out = IMG / "donation-poster.png"
img.save(out, "PNG")
print("saved", out, img.size)
