#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Essai 4 fonds — miniatures 1280x720 sur FOND 19 / 18 / 14 / 17.

Même structure pour les quatre ; seule la matière change.
Bleu violacé de la vignette de référence (#2F4DB1 / #2E2F93) réinjecté en 30 %
par voile violet ; accent menthe #68D8C0 pour les 10 % de signalétique.
Le FOND 18 (violet-magenta, hors charte) est recalé vers le bleu avant voile.
"""
import math
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont

W, H = 1280, 720
FD = "/usr/share/fonts/truetype/dejavu/"

TITRE_TTF = "polices/playfair-display-italic-var.ttf"
TITRE_VAR = "Black Italic"
SANS_TTF = "polices/montserrat-var.ttf"
SANS_VAR = "SemiBold"

VIOLET = (58, 59, 143)      # 30 % — prélevé sur la vignette de référence
MENTHE = (104, 216, 192)    # 10 % — accent
ACIER = (127, 182, 232)

JOBS = [
    dict(fond="fonds/f19-bleu-carreaux-translucides.jpg", out="miniature-fond19.jpg",
         label="FOND 19 — carreaux translucides", hue=0.0, wash=0.30, dark=0.92,
         scrim=1.05, title_scrim=110),
    dict(fond="fonds/_hors-charte/f18-violet-magenta-stries.jpg", out="miniature-fond18.jpg",
         label="FOND 18 — ramené au bleu", hue=-86.0, wash=0.28, dark=0.92,
         desat=0.62, scrim=1.15, title_scrim=115),
    dict(fond="fonds/f14-cyan-turquoise-flou.jpg", out="miniature-fond14.jpg",
         label="FOND 14 — cyan turquoise", hue=0.0, wash=0.42, dark=0.84,
         scrim=1.25, title_scrim=150),
    dict(fond="fonds/f17-bleu-scene-louange.jpg", out="miniature-fond17.jpg",
         label="FOND 17 — scène de louange", hue=0.0, wash=0.32, dark=0.86,
         scrim=1.45, title_scrim=120),
]


def font(n, s):
    return ImageFont.truetype(FD + n, s)


def var_font(path, size, variation=None):
    f = ImageFont.truetype(path, size)
    if variation:
        try:
            f.set_variation_by_name(variation)
        except Exception as e:
            print("variation indisponible:", variation, e)
    return f


def fit(path, variation, text, target_w, start=140, lo=60):
    """Corps le plus grand possible qui tient dans target_w."""
    size = start
    while size > lo:
        f = var_font(path, size, variation)
        if f.getlength(text) <= target_w:
            return f, size
        size -= 2
    return var_font(path, lo, variation), lo


def cover(im, w, h):
    sw, sh = im.size
    s = max(w / sw, h / sh)
    im = im.resize((round(sw * s), round(sh * s)), Image.LANCZOS)
    return im.crop(((im.width - w) // 2, (im.height - h) // 2,
                    (im.width - w) // 2 + w, (im.height - h) // 2 + h))


def hue_shift(im, deg, desat=1.0):
    if not deg and desat == 1.0:
        return im
    hsv = im.convert("HSV")
    h, s, v = hsv.split()
    if deg:
        d = int(round(deg * 255 / 360)) % 256
        h = h.point(lambda x: (x + d) % 256)
    if desat != 1.0:
        s = s.point(lambda x: int(x * desat))
    return Image.merge("HSV", (h, s, v)).convert("RGB")


def vgrad(w, h, stops):
    g = Image.new("RGBA", (1, h))
    px = g.load()
    for y in range(h):
        t = y / max(1, h - 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                k = 0 if p1 == p0 else (t - p0) / (p1 - p0)
                px[0, y] = tuple(round(c0[j] + (c1[j] - c0[j]) * k) for j in range(4))
                break
    return g.resize((w, h))


def radial(w, h, center, radius, color, peak):
    small = 160
    m = Image.new("L", (small, int(small * h / w)), 0)
    d = ImageDraw.Draw(m)
    cx = center[0] * small / w
    cy = center[1] * (small * h / w) / h
    r = radius * small / w
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=peak)
    m = m.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(60))
    layer = Image.new("RGBA", (w, h), color + (0,))
    layer.putalpha(m)
    return layer


def text_mask(text, fnt, tracking=0):
    widths = [fnt.getlength(ch) for ch in text]
    asc, desc = fnt.getmetrics()
    total = sum(widths) + tracking * max(0, len(text) - 1)
    m = Image.new("L", (max(1, int(round(total)) + 10), int(asc + desc + 8)), 0)
    d = ImageDraw.Draw(m)
    x = 4
    for ch, cw in zip(text, widths):
        d.text((x, 4), ch, font=fnt, fill=255)
        x += cw + tracking
    return m


def fill_gradient(mask, top, bottom):
    w, h = mask.size
    g = Image.new("RGB", (1, h))
    px = g.load()
    for y in range(h):
        k = y / max(1, h - 1)
        px[0, y] = tuple(round(top[i] + (bottom[i] - top[i]) * k) for i in range(3))
    layer = g.resize((w, h)).convert("RGBA")
    layer.putalpha(mask)
    return layer


def shear(layer, angle_deg, pad=90):
    w, h = layer.size
    b = -math.tan(math.radians(angle_deg))
    canvas = Image.new("RGBA", (w + pad, h + 20), (0, 0, 0, 0))
    canvas.paste(layer, (pad // 2, 10))
    return canvas.transform(canvas.size, Image.AFFINE,
                            (1, b, -b * (h + 10) * 0.5, 0, 1, 0), resample=Image.BICUBIC)


def drop(layer, blur, alpha, offset, color=(0, 0, 0)):
    sh = Image.new("RGBA", (layer.width + 120, layer.height + 120), (0, 0, 0, 0))
    tint = Image.new("RGBA", layer.size, color + (alpha,))
    sh.paste(tint, (60 + offset[0], 60 + offset[1]), layer)
    return sh.filter(ImageFilter.GaussianBlur(blur))


def paste_center(base, layer, cx, cy):
    base.alpha_composite(layer, (round(cx - layer.width / 2), round(cy - layer.height / 2)))


def build_background(job, root):
    """Fond seul d'un job : matière + voile + voiles, sans aucun texte."""
    bg = cover(Image.open(root + "/" + job["fond"]).convert("RGB"), W, H)
    bg = hue_shift(bg, job.get("hue", 0.0), job.get("desat", 1.0))
    bg = bg.filter(ImageFilter.UnsharpMask(radius=2.2, percent=95, threshold=2))
    if job["dark"] != 1.0:
        bg = Image.eval(bg, lambda v: min(255, int(v * job["dark"])))

    base = bg.convert("RGBA")

    wash = Image.eval(Image.new("RGB", (W, H), VIOLET), lambda v: int(v * 0.55))
    lit = ImageChops.screen(bg, wash)
    base = Image.blend(base, lit.convert("RGBA"), job["wash"])

    k = job.get("scrim", 1.0)
    a = lambda v: min(255, int(v * k))
    base.alpha_composite(vgrad(W, H, [
        (0.00, (6, 8, 34, a(200))),
        (0.30, (8, 12, 52, a(115))),
        (0.55, (8, 12, 52, a(55))),
        (0.78, (6, 8, 32, a(125))),
        (1.00, (4, 5, 24, a(210))),
    ]))
    base.alpha_composite(radial(W, H, (W * 0.5, H * 0.46), W * 0.62, (86, 92, 210), 62))

    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse([40, 170, 1240, 540], fill=job.get("title_scrim", 110))
    m = m.filter(ImageFilter.GaussianBlur(95))
    veil = Image.new("RGBA", (W, H), (4, 8, 30, 0))
    veil.putalpha(m)
    base.alpha_composite(veil)

    beam = Image.new("L", (W, H), 0)
    ImageDraw.Draw(beam).polygon(
        [(70, 252), (1240, 252), (1210, 314), (40, 314)], fill=165)
    beam = beam.filter(ImageFilter.GaussianBlur(3.4))
    vlayer = Image.eval(Image.new("RGB", (W, H), (96, 84, 196)), lambda v: int(v * 0.62))
    vlit = ImageChops.screen(base.convert("RGB"), vlayer)
    base = Image.composite(vlit.convert("RGBA"), base, beam)
    return base


def render(job, root, outdir):
    base = build_background(job, root)

    d = ImageDraw.Draw(base, "RGBA")
    d.polygon([(96, 74), (128, 74), (112, 104)], fill=MENTHE + (215,))
    d.line([(150, 88), (1184, 88)], fill=MENTHE + (70,), width=2)

    f, size = fit(TITRE_TTF, TITRE_VAR, "ATMOSPHÈRE", 1060, start=170)
    print("corps du titre :", size)
    l1 = fill_gradient(text_mask("ATMOSPHÈRE", f, 1), (255, 255, 255), (226, 233, 250))
    l2 = fill_gradient(text_mask("DE PRIÈRE", f, 1), (255, 255, 255), (226, 233, 250))
    s1 = drop(l1, 16, 120, (5, 7))
    s2 = drop(l2, 16, 120, (5, 7))
    paste_center(base, s1, W / 2 - 3, 292)
    paste_center(base, s2, W / 2 - 3, 450)
    paste_center(base, l1, W / 2, 288)
    paste_center(base, l2, W / 2, 446)

    fs = var_font(SANS_TTF, 27, SANS_VAR)
    mt = text_mask("À ICC PAHOU", fs, 9)
    col = Image.new("RGBA", mt.size, MENTHE + (255,))
    col.putalpha(mt)
    y = 604
    paste_center(base, col, W / 2, y)
    wl = mt.width / 2 + 40
    d.line([(W / 2 - wl - 90, y), (W / 2 - wl, y)], fill=ACIER + (200,), width=2)
    d.line([(W / 2 + wl, y), (W / 2 + wl + 90, y)], fill=ACIER + (200,), width=2)

    base.convert("RGB").save(outdir + "/" + job["out"], quality=93, subsampling=1, optimize=True)
    print("écrit", job["out"])


def planche(outdir):
    tw, th, pad, gap, lh = 620, 349, 24, 18, 34
    sw, sh = pad * 2 + tw * 2 + gap, pad * 2 + (th + lh) * 2 + gap
    sheet = Image.new("RGB", (sw, sh), (9, 12, 26))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 20)
    for i, job in enumerate(JOBS):
        im = Image.open(outdir + "/" + job["out"]).resize((tw, th), Image.LANCZOS)
        x = pad + (i % 2) * (tw + gap)
        y = pad + (i // 2) * (th + lh + gap)
        sheet.paste(im, (x, y))
        d.text((x + 2, y + th + 8), job["label"], font=f, fill=(214, 226, 244))
    sheet.save(outdir + "/planche-4-fonds.jpg", quality=90, optimize=True)
    print("écrit planche-4-fonds.jpg")


if __name__ == "__main__":
    root, outdir = sys.argv[1], sys.argv[2]
    for j in JOBS:
        render(j, root, outdir)
    planche(outdir)
