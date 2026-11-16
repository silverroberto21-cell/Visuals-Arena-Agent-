#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Miniature 1280×720 — « Maintiens le CAP, sa Gloire se manifestera » (FOND 7).

Composition **sans photo d'orateur** : le fond fourni porte tout le visuel, le thème
est dit par la typographie. Pas de portrait, pas de silhouette, pas de détourage.

Palette reconstruite sur f07 : 60 % bleus mesurés (#0A398F / #0D56B1 / #0B3AC8),
30 % acier (#B0D6F6) et 10 % or pâle (#E8C87A) sur le mot CAP, la date et les filets.
Polices : Anton (titre condensé) + Montserrat (signalétique) — duo du thème.

    python3 scripts/render_cap_f07_texte.py livrables/<AAAA-MM-JJ>-miniature-...jpg
"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

W, H = 1280, 720
TITRE = "polices/anton-regular.ttf"
SANS = "polices/montserrat-var.ttf"
FOND = "fonds/f07-bleu-nuit-bokeh.jpg"

# 60 % — nuances relevées sur f07
NUIT = (7, 26, 78)
BLEU = (13, 86, 177)
CYAN = (13, 137, 210)
# 30 % — secondaire
ACIER = (176, 214, 246)
# 10 % — accent
OR = (232, 200, 122)

DATE_JOUR = "DIMANCHE"
DATE_JOUR_NUM = "8"
DATE_MOIS = "NOVEMBRE"
DATE_AN = "2026"
ORATEUR = "AP Enock MISSIMAHOU"


def font(path, size, variation=None):
    f = ImageFont.truetype(path, size)
    if variation:
        try:
            f.set_variation_by_name(variation)
        except Exception as e:
            print("variation indisponible:", variation, e)
    return f


def cover(im, w, h):
    sw, sh = im.size
    s = max(w / sw, h / sh)
    im = im.resize((round(sw * s), round(sh * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


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


def radial(w, h, cx, cy, r, color, peak, blur=80):
    small = 200
    sh = int(small * h / w)
    m = Image.new("L", (small, sh), 0)
    ImageDraw.Draw(m).ellipse([cx * small / w - r * small / w, cy * sh / h - r * sh / h,
                               cx * small / w + r * small / w, cy * sh / h + r * sh / h],
                              fill=peak)
    m = m.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(blur))
    lay = Image.new("RGBA", (w, h), color + (0,))
    lay.putalpha(m)
    return lay


def text_mask(text, fnt, tracking=0):
    widths = [fnt.getlength(c) for c in text]
    asc, desc = fnt.getmetrics()
    total = sum(widths) + tracking * max(0, len(text) - 1)
    m = Image.new("L", (max(1, int(round(total)) + 16), int(asc + desc + 20)), 0)
    d = ImageDraw.Draw(m)
    x = 8
    for c, cw in zip(text, widths):
        d.text((x, 10), c, font=fnt, fill=255)
        x += cw + tracking
    return m


def fill_gradient(mask, top, bottom):
    w, h = mask.size
    g = Image.new("RGB", (1, h))
    px = g.load()
    for y in range(h):
        k = y / max(1, h - 1)
        px[0, y] = tuple(round(top[i] + (bottom[i] - top[i]) * k) for i in range(3))
    lay = g.resize((w, h)).convert("RGBA")
    lay.putalpha(mask)
    return lay


def drop(layer, blur, alpha, offset, color=(0, 0, 0)):
    sh = Image.new("RGBA", (layer.width + 160, layer.height + 160), (0, 0, 0, 0))
    tint = Image.new("RGBA", layer.size, color + (alpha,))
    sh.paste(tint, (80 + offset[0], 80 + offset[1]), layer)
    return sh.filter(ImageFilter.GaussianBlur(blur))


def fit_width(path, text, target_w, start=200, lo=40):
    size = start
    while size > lo:
        f = font(path, size)
        if f.getlength(text) <= target_w:
            return f, size
        size -= 2
    return font(path, lo), lo


def paste_left(base, layer, x, y):
    bb = layer.getbbox()
    if bb is None:
        return
    base.alpha_composite(layer, (round(x - bb[0]), round(y - bb[1])))


def paste_right(base, layer, right, y):
    bb = layer.getbbox()
    if bb is None:
        return
    base.alpha_composite(layer, (round(right - bb[2]), round(y - bb[1])))


def compass(draw, cx, cy, r, color, alpha=40):
    """Rose des vents filaire : le CAP, sans imager un bateau."""
    for k, rr in enumerate((r, r * 0.72, r * 0.44)):
        a = int(alpha * (1.0 if k == 0 else 0.7))
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=color + (a,), width=2)
    # branches de la rose
    for ang in range(0, 360, 45):
        import math
        rad = math.radians(ang)
        long = r * (1.02 if ang % 90 == 0 else 0.78)
        x0, y0 = cx + math.cos(rad) * r * 0.12, cy + math.sin(rad) * r * 0.12
        x1, y1 = cx + math.cos(rad) * long, cy + math.sin(rad) * long
        draw.line([(x0, y0), (x1, y1)], fill=color + (alpha,), width=2)
    # pointes
    draw.polygon([(cx, cy - r * 1.12), (cx - 9, cy - r * 0.96), (cx + 9, cy - r * 0.96)],
                 fill=OR + (150,))


def main(out, fond=FOND):
    bg = cover(Image.open(fond).convert("RGB"), W, H)
    bg = bg.filter(ImageFilter.GaussianBlur(1.4))
    bg = bg.filter(ImageFilter.UnsharpMask(radius=3, percent=75, threshold=2))
    bg = Image.eval(bg, lambda v: min(255, int(v * 0.88)))

    base = bg.convert("RGBA")
    base.alpha_composite(vgrad(W, H, [
        (0.00, (4, 10, 40, 176)),
        (0.24, (5, 14, 52, 96)),
        (0.50, (5, 14, 52, 46)),
        (0.78, (4, 10, 38, 128)),
        (1.00, (3, 6, 28, 214)),
    ]))
    base.alpha_composite(radial(W, H, W * 0.80, H * 0.14, W * 0.46, (60, 140, 235), 52, 90))
    base.alpha_composite(radial(W, H, 352, 452, 320, OR, 40, 90))

    d = ImageDraw.Draw(base, "RGBA")

    # rose des vents, discrète, dans le tiers droit : le CAP sans imager un bateau
    compass(d, 1004, 296, 152, ACIER, 30)

    ########################################
    # marque
    fm = font(SANS, 19, "SemiBold")
    m = text_mask("ICC PAHOU", fm, 8)
    col = Image.new("RGBA", m.size, ACIER + (255,))
    col.putalpha(m)
    paste_left(base, col, 68, 60)
    d.line([(68, 104), (102, 104)], fill=OR + (235,), width=3)
    d.line([(110, 104), (232, 104)], fill=ACIER + (95,), width=1)

    ########################################
    # titre
    target = 600
    f1, s1 = fit_width(TITRE, "MAINTIENS", target, start=190)
    f2, s2 = fit_width(TITRE, "LE CAP", target, start=190)
    print("corps:", s1, s2)
    l1 = fill_gradient(text_mask("MAINTIENS", f1, 1), (255, 255, 255), (219, 233, 252))
    l2 = fill_gradient(text_mask("LE", f2, 1), (255, 255, 255), (219, 233, 252))
    l3 = fill_gradient(text_mask("CAP", f2, 1), (255, 249, 228), OR)

    y1 = 176
    paste_left(base, drop(l1, 20, 120, (5, 9)), 68, y1 + 8)
    paste_left(base, l1, 64, y1)
    asc1 = l1.getbbox()[3] - l1.getbbox()[1]
    y2 = y1 + int(asc1 * 0.98)
    paste_left(base, drop(l2, 20, 120, (5, 9)), 68, y2 + 8)
    paste_left(base, l2, 64, y2)
    gap = 28
    cap_x = 64 + l2.getbbox()[2] + gap
    paste_left(base, drop(l3, 20, 120, (5, 9)), cap_x + 4, y2 + 8)
    paste_left(base, l3, cap_x, y2)

    cap_h = l3.getbbox()[3] - l3.getbbox()[1]
    # filet or au-dessus du titre (règle éditoriale, ne touche aucun texte)
    d.line([(64, y1 - 22), (64 + 372, y1 - 22)], fill=OR + (225,), width=3)

    ########################################
    # sous-titre : sa Gloire se manifestera (Gloire en or)
    ysub = y2 + int(cap_h * 0.98) + 30
    fs = font(SANS, 34, "SemiBold")
    xcur = 66
    for txt, col in (("sa ", (238, 245, 255)), ("Gloire", (250, 222, 158)),
                     (" se manifestera", (238, 245, 255))):
        ms = text_mask(txt, fs, 2)
        sub = fill_gradient(ms, col, tuple(max(0, c - 30) for c in col))
        paste_left(base, drop(sub, 10, 100, (3, 5)), xcur + 3, ysub + 4)
        paste_left(base, sub, xcur, ysub)
        xcur += int(round(ms.width)) - 4

    ########################################
    # date : bloc bas-droite, aligné à droite
    RX = 1216
    d.line([(RX - 340, 556), (RX, 556)], fill=OR + (190,), width=3)

    fd1 = font(SANS, 18, "SemiBold")
    md = text_mask(DATE_JOUR, fd1, 9)
    cold = Image.new("RGBA", md.size, OR + (245,))
    cold.putalpha(md)
    paste_right(base, cold, RX, 572)

    fd2 = font(SANS, 40, "Bold")
    mj = text_mask("8 NOVEMBRE", fd2, 1)
    jour = fill_gradient(mj, (255, 255, 255), (216, 232, 252))
    paste_right(base, drop(jour, 14, 110, (4, 6)), RX + 3, 604)
    paste_right(base, jour, RX, 600)

    fan = font(SANS, 24, "Medium")
    man = text_mask(DATE_AN, fan, 9)
    an = Image.new("RGBA", man.size, ACIER + (235,))
    an.putalpha(man)
    paste_right(base, an, RX, 654)

    ########################################
    # orateur, en pied à gauche
    yp = 596
    fl = font(SANS, 15, "SemiBold")
    ml = text_mask("PRÉDICATEUR", fl, 7)
    lab = Image.new("RGBA", ml.size, OR + (225,))
    lab.putalpha(ml)
    paste_left(base, lab, 68, yp)
    fn = font(SANS, 24, "Bold")
    mn = text_mask(ORATEUR, fn, 2)
    nom = Image.new("RGBA", mn.size, (255, 255, 255, 255))
    nom.putalpha(mn)
    paste_left(base, drop(nom, 10, 110, (3, 4)), 68, yp + 34)
    paste_left(base, nom, 66, yp + 32)

    base.convert("RGB").save(out, quality=94, subsampling=1, optimize=True)
    print("écrit", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else FOND)
