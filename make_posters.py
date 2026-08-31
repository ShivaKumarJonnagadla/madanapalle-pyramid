#!/usr/bin/env python3
"""Generate donation posters in multiple sizes: portrait, square, story."""
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import pathlib

root = pathlib.Path(__file__).parent
IMG = root / "assets" / "img"

INDIGO_TOP = (30, 24, 68)
INDIGO_BOT = (58, 38, 92)
GOLD = (233, 173, 40)
GOLD_SOFT = (240, 205, 110)
CREAM = (247, 240, 226)
MUTED = (200, 190, 168)
PANEL = (255, 253, 247)
INK = (34, 28, 46)

F = "/System/Library/Fonts/Supplemental/"
HN = "/System/Library/Fonts/HelveticaNeue.ttc"
def gfont(size, bold=False, italic=False):
    name = "Georgia"
    if bold and italic: name += " Bold Italic"
    elif bold: name += " Bold"
    elif italic: name += " Italic"
    return ImageFont.truetype(F + name + ".ttf", size)
def uni(size):
    return ImageFont.truetype(HN, size)

G = {}
def new_canvas(W, H):
    img = Image.new("RGB", (W, H), INDIGO_TOP)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        c = tuple(int(INDIGO_TOP[i] + (INDIGO_BOT[i]-INDIGO_TOP[i])*t) for i in range(3))
        draw.line([(0, y), (W, y)], fill=c)
    glow = Image.new("RGB", (W, H), INDIGO_TOP)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W//2-360, -int(H*0.18), W//2+360, int(H*0.30)], fill=(120, 92, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img = Image.blend(img, glow, 0.35)
    G["img"] = img; G["draw"] = ImageDraw.Draw(img); G["W"] = W; G["H"] = H
    return img

def ctext(y, text, font, fill, spacing=0):
    draw, W = G["draw"], G["W"]
    if spacing:
        total = sum(draw.textlength(ch, font=font)+spacing for ch in text) - spacing
        x = (W-total)/2
        for ch in text:
            draw.text((x, y), ch, font=font, fill=fill); x += draw.textlength(ch, font=font)+spacing
        return
    w = draw.textlength(text, font=font)
    draw.text(((W-w)/2, y), text, font=font, fill=fill)

def wrap_center(y, text, font, fill, maxw, lh):
    draw = G["draw"]
    words, line, lines = text.split(), "", []
    for w in words:
        test = (line+" "+w).strip()
        if draw.textlength(test, font=font) <= maxw: line = test
        else: lines.append(line); line = w
    if line: lines.append(line)
    for ln in lines: ctext(y, ln, font, fill); y += lh
    return y

def rounded(im, radius):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.size[0], im.size[1]], radius, fill=255)
    im.putalpha(mask); return im

def tile(path, box_w, box_h, radius=18):
    im = ImageOps.exif_transpose(Image.open(path).convert("RGB"))
    return rounded(ImageOps.fit(im, (box_w, box_h), Image.LANCZOS), radius)

def triangle(cy, half, h):
    d, W = G["draw"], G["W"]
    d.polygon([(W/2, cy), (W/2-half, cy+h), (W/2+half, cy+h)], outline=GOLD, width=5)
    d.line([(W/2-half*0.5, cy+h*0.48), (W/2+half*0.5, cy+h*0.48)], fill=GOLD, width=3)

def paste_tiles(files, M, y, cols, tw, th, gap):
    img, draw = G["img"], G["draw"]
    for i, fn in enumerate(files):
        r, c = divmod(i, cols)
        px = M + c*(tw+gap); py = y + r*(th+gap)
        t = tile(IMG/fn, tw, th); img.paste(t, (px, py), t)
        draw.rounded_rectangle([px, py, px+tw, py+th], 18, outline=GOLD, width=3)
    rows = (len(files)+cols-1)//cols
    return y + rows*th + (rows-1)*gap

def donation_panel(M, y, W, ph=250, qr=196):
    img, pd = G["img"], G["draw"]
    panel = rounded(Image.new("RGB", (W-2*M, ph), PANEL), 24)
    img.paste(panel, (M, y), panel)
    q = ImageOps.fit(Image.open(IMG/"upi-qr.jpg").convert("RGB"), (qr, qr), Image.LANCZOS)
    img.paste(q, (M+28, y+(ph-qr)//2))
    tx = M+28+qr+34
    pd.text((tx, y+28), "SCAN TO DONATE", font=uni(24), fill=(200,120,20))
    pd.text((tx, y+64), "UPI  6509092255@myapgb", font=uni(30), fill=INK)
    pd.text((tx, y+106), "A/C 650910016995155", font=uni(23), fill=(80,74,90))
    pd.text((tx, y+138), "IFSC UBIN0CG7999 · AP Grameena Bank", font=uni(22), fill=(80,74,90))
    pd.text((tx, y+180), "madanapalle-pyramid.vercel.app", font=uni(26), fill=(150,100,10))
    return y + ph

QUOTE = "Quiet the mind, and the soul will speak."

# ---------- SQUARE 1080x1080 ----------
def render_square():
    W, H, M = 1080, 1080, 66
    new_canvas(W, H)
    y = 44
    triangle(y, 46, 74); y += 92
    ctext(y, "MADANAPALLE · ANDHRA PRADESH", uni(22), GOLD_SOFT, spacing=3); y += 40
    ctext(y, "A Meditation Pyramid", gfont(58, bold=True), CREAM); y += 68
    ctext(y, "for the whole community", gfont(32, italic=True), GOLD_SOFT); y += 54
    ctext(y, QUOTE, gfont(28, italic=True), CREAM); y += 52
    gap = 16; tw = (W-2*M-2*gap)//3; th = 200
    y = paste_tiles(["team.jpg", "pooja-1.jpg", "pillars-1.jpg"], M, y, 3, tw, th, gap); y += 30
    y = wrap_center(y, "Land donated. Foundation, borewell and pillars built. The funds are now finished.", uni(27), CREAM, W-2*M, 38); y += 8
    ctext(y, "Even ₹10 helps us complete it.", uni(29), GOLD_SOFT); y += 52
    y = donation_panel(M, y, W, ph=214, qr=168); y += 22
    ctext(y, "Madanapalle Pyramid Spiritual Society", uni(24), GOLD_SOFT)
    G["img"].save(IMG/"donation-poster-square.png", "PNG"); print("square", G["img"].size)

# ---------- STORY 1080x1920 ----------
def render_story():
    W, H, M = 1080, 1920, 80
    new_canvas(W, H)
    y = 120
    triangle(y, 58, 92); y += 128
    ctext(y, "MADANAPALLE · ANNAMAYYA · ANDHRA PRADESH", uni(26), GOLD_SOFT, spacing=4); y += 52
    ctext(y, "A Meditation Pyramid", gfont(78, bold=True), CREAM); y += 96
    ctext(y, "for the whole community", gfont(46, italic=True), GOLD_SOFT); y += 104
    G["draw"].text((M-6, y-20), "“", font=gfont(130, bold=True), fill=GOLD)
    y2 = wrap_center(y+22, QUOTE, gfont(44, italic=True), CREAM, W-2*M-40, 60)
    ctext(y2+4, "Ma Jaya Sati Bhagavati", uni(26), MUTED); y = y2 + 78
    gap = 22; tw = (W-2*M-gap)//2; th = 300
    y = paste_tiles(["team.jpg", "pooja-1.jpg", "foundation-1.jpg", "pillars-1.jpg"], M, y, 2, tw, th, gap); y += 54
    y = wrap_center(y, "The land is donated. Foundation, borewell and pillars are done, but the funds are now finished and work has paused.", uni(34), CREAM, W-2*M, 48); y += 14
    ctext(y, "Even ₹10 helps us complete it, and makes many smile.", uni(34), GOLD_SOFT); y += 74
    y = donation_panel(M, y, W, ph=260, qr=204); y += 40
    ctext(y, "President J. Anuradha  92469 83035   ·   Treasurer  99898 59591", uni(24), MUTED); y += 42
    ctext(y, "Madanapalle Pyramid Spiritual Society", uni(28), GOLD_SOFT)
    G["img"].save(IMG/"donation-poster-story.png", "PNG"); print("story", G["img"].size)

render_square()
render_story()
