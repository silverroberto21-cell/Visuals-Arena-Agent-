#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Miniature 1280×720 — thème « Maintiens le CAP, sa Gloire se manifestera » (FOND 7).

Palette reconstruite sur le fond fourni f07 (bleu nuit bokeh) : 60 % bleus mesurés
(#0D56B1 / #0B3AC8 / #0764C5), 30 % secondaire acier de la chemise de l'orateur,
10 % accent or pâle (#E8C87A) — l'accent « Gloire » qui court du titre à la date.
Deux polices : Anton (titre, capitales condensées qui tiennent en vignette)
+ Montserrat (signalétique). Aucun élément d'interface de modèle.

    python3 scripts/render_cap_f07.py <photo.jpg> livrables/<date>-miniature-...jpg

La bannière violette de la scène derrière l'orateur est ramenée au bleu par
`blue_the_scene()` : seuls les pixels magenta saturés changent de teinte.
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
BLEU_VIF = (11, 58, 200)
CYAN = (13, 137, 210)
# 30 % — secondaire (chemise claire de l'orateur, ramenée au bleu)
ACIER = (176, 214, 246)
# 10 % — accent
OR = (232, 200, 122)

CROP = (92, 92, 1957, 1953)   # rognage de la bordure grise du fichier source


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
    x = (im.width - w) // 2
    y = (im.height - h) // 2
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


def radial(w, h, cx, cy, r, color, peak, blur=70):
    small = 180
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
    m = Image.new("L", (max(1, int(round(total)) + 14), int(asc + desc + 18)), 0)
    d = ImageDraw.Draw(m)
    x = 7
    for c, cw in zip(text, widths):
        d.text((x, 9), c, font=fnt, fill=255)
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
    sh = Image.new("RGBA", (layer.width + 140, layer.height + 140), (0, 0, 0, 0))
    tint = Image.new("RGBA", layer.size, color + (alpha,))
    sh.paste(tint, (70 + offset[0], 70 + offset[1]), layer)
    return sh.filter(ImageFilter.GaussianBlur(blur))


def fit_width(path, variation, text, target_w, start=200, lo=40):
    size = start
    while size > lo:
        f = font(path, size, variation)
        if f.getlength(text) <= target_w:
            return f, size
        size -= 2
    return font(path, lo, variation), lo


def paste_left(base, layer, x, y):
    """x, y = position du coin haut-gauche visuel (le masque a une marge interne)."""
    bb = layer.getbbox()
    base.alpha_composite(layer, (round(x - bb[0]), round(y - bb[1])))


def blue_the_scene(im, target=162):
    """Ramène au bleu les seuls pixels magenta/violet saturés (décor de scène)."""
    hsv = im.convert("HSV")
    hh, ss, vv = hsv.split()
    hp, sp = hh.load(), ss.load()
    w, ht = im.size
    out = hh.copy()
    op = out.load()
    for y in range(ht):
        for x in range(w):
            h, sat = hp[x, y], sp[x, y]
            if sat > 50 and 166 <= h <= 245:      # bande magenta / violet / pourpre
                k = min(1.0, (h - 166) / 62.0)
                op[x, y] = int(round(target - 16 * k))         # bleu, plus froid vers le pourpre
    return Image.merge("HSV", (out, ss, vv)).convert("RGB")


def orator(path, h, crop_left=0.0, crop=CROP):
    im = Image.open(path).convert("RGB")
    if crop:
        im = im.crop(crop)
    if crop_left:
        sw, sh = im.size
        im = im.crop((int(sw * crop_left), 0, sw, sh))
    w = round(im.width * h / im.height)
    im = im.resize((w, h), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.5, percent=60, threshold=3))
    # lumière : relève des tons moyens, jamais de retouche du visage ni de la tenue
    im = Image.eval(im, lambda v: min(255, int(255 * (v / 255) ** 0.85)))
    im = Image.eval(im, lambda v: min(255, max(0, int((v - 128) * 1.05 + 132))))
    # ambiance : la bannière magenta de la scène est ramenée au bleu du FOND 7.
    # On ne touche QU'AUX pixels violet/magenta saturés : les peaux, la chemise et
    # le visage gardent leur teinte — le sujet n'est pas retouché.
    im = blue_the_scene(im)
    return im


def main(photo, out, fond=FOND):
    bg = cover(Image.open(fond).convert("RGB"), W, H)
    bg = bg.filter(ImageFilter.GaussianBlur(1.2))
    bg = bg.filter(ImageFilter.UnsharpMask(radius=3, percent=70, threshold=2))
    bg = Image.eval(bg, lambda v: min(255, int(v * 0.90)))

    base = bg.convert("RGBA")
    # scrim de lisibilité : bas + gauche, sans éteindre le bokeh
    base.alpha_composite(vgrad(W, H, [
        (0.00, (4, 10, 40, 168)),
        (0.26, (5, 14, 52, 84)),
        (0.52, (5, 14, 52, 40)),
        (0.80, (4, 10, 38, 120)),
        (1.00, (3, 6, 28, 205)),
    ]))
    base.alpha_composite(radial(W, H, W * 0.78, H * 0.20, W * 0.50, (60, 140, 235), 54, 90))

    # lueur derrière le mot CAP
    base.alpha_composite(radial(W, H, 400, 470, 300, OR, 46, 80))

    ########################################
    # orateur — panneau droit, fondu sur le bord gauche
    PW = 604
    OH = 708                      # photo un peu rentrée : la main levée ne touche pas le bord
    img = orator(photo, OH, crop_left=0.14)
    canvas = Image.new("RGB", (PW, OH), (0, 0, 0))
    canvas.paste(img, (PW - img.width, 0))   # calé à droite : on rogne par la gauche
    lay = canvas.convert("RGBA")
    ramp = Image.new("L", (PW, OH), 255)
    d = ImageDraw.Draw(ramp)
    f = int(PW * 0.34)
    for x in range(f):
        d.line([(x, 0), (x, OH)], fill=int(255 * (x / f) ** 1.45))
    # bord haut : fondu court, le décor de scène se raccorde au bokeh
    top = Image.new("L", (PW, OH), 255)
    dt = ImageDraw.Draw(top)
    ft = 22
    for y in range(ft):
        dt.line([(0, y), (PW, y)], fill=int(255 * (y / ft) ** 1.2))
    ramp = ImageChops.multiply(ramp, top)
    lay.putalpha(ramp)
    # ombre portée du panneau : le sujet se détache du bokeh
    sh = Image.new("RGBA", (PW + 200, OH + 60), (0, 0, 0, 0))
    sh.paste(Image.new("RGBA", (PW, OH), (3, 8, 30, 150)), (140, 20), ramp)
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(28)), (W - PW - 120, 12))
    base.alpha_composite(lay, (W - PW, 12))

    d = ImageDraw.Draw(base, "RGBA")

    ########################################
    # accroche + marque
    fm = font(SANS, 19, "SemiBold")
    m = text_mask("ICC PAHOU", fm, 8)
    col = Image.new("RGBA", m.size, ACIER + (255,))
    col.putalpha(m)
    paste_left(base, col, 68, 64)
    d.line([(68, 108), (68 + 34, 108)], fill=OR + (235,), width=3)
    d.line([(110, 108), (232, 108)], fill=ACIER + (90,), width=1)

    ########################################
    # titre : MAINTIENS LE CAP — 3 lignes, CAP à l'accent
    target = 566
    f1, s1 = fit_width(TITRE, None, "MAINTIENS", target, start=190)
    f2, s2 = fit_width(TITRE, None, "LE CAP", target, start=190)
    print("corps:", s1, s2)
    l1 = fill_gradient(text_mask("MAINTIENS", f1, 1), (255, 255, 255), (219, 233, 252))
    l2 = fill_gradient(text_mask("LE", f2, 1), (255, 255, 255), (219, 233, 252))
    l3 = fill_gradient(text_mask("CAP", f2, 1), (255, 249, 228), OR)

    y1 = 186
    paste_left(base, drop(l1, 18, 120, (5, 8)), 66, y1 + 8)
    paste_left(base, l1, 62, y1)
    h1 = l1.getbbox()[1]
    step = (l1.getbbox()[3] - l1.getbbox()[1]) * 0.98
    y2 = y1 + step + 6
    paste_left(base, drop(l2, 18, 120, (5, 8)), 66, y2 + 8)
    paste_left(base, l2, 62, y2)

    # CAP posé à droite de « LE », filet or qui court sous le mot
    gap = 30
    cap_x = 62 + l2.getbbox()[2] + gap
    y3 = y2
    paste_left(base, drop(l3, 18, 120, (5, 8)), cap_x + 4, y3 + 8)
    paste_left(base, l3, cap_x, y3)

    ########################################
    # sous-titre : sa Gloire se manifestera
    fs = font(SANS, 30, "SemiBold")
    ysub = y2 + step + 54
    xcur = 64
    for txt, col in (("sa ", (238, 245, 255)), ("Gloire", (250, 222, 158)),
                     (" se manifestera", (238, 245, 255))):
        ms = text_mask(txt, fs, 2)
        sub = fill_gradient(ms, col, tuple(max(0, c - 26) for c in col))
        paste_left(base, drop(sub, 10, 100, (3, 5)), xcur + 3, ysub + 4)
        paste_left(base, sub, xcur, ysub)
        xcur += int(round(ms.width)) - 2 + 2


    # rose des vents discrète : le CAP, en arcs fins dans l'angle bas
    comp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dc = ImageDraw.Draw(comp)
    for r, col, wdt in ((150, ACIER + (46,), 2), (214, ACIER + (32,), 2),
                        (286, OR + (34,), 2), (352, ACIER + (18,), 1)):
        dc.arc([40 - r, 812 - r, 40 + r, 812 + r], 250, 350, fill=col, width=wdt)
    base.alpha_composite(comp)

    # filet + date
    yb = ysub + 96
    d.line([(64, yb), (300, yb)], fill=OR + (200,), width=2)
    fd = font(SANS, 20, "Medium")
    md = text_mask("AUJOURD’HUI", fd, 5)
    col = Image.new("RGBA", md.size, ACIER + (235,))
    col.putalpha(md)
    paste_left(base, col, 64, yb + 16)

    # prédicateur
    fp = font(SANS, 24, "Bold")     # prénom/nom recopiés tels que fournis
    mp = text_mask("AP Enock MISSIMAHOU", fp, 2)
    colp = Image.new("RGBA", mp.size, (255, 255, 255, 255))
    colp.putalpha(mp)
    paste_left(base, colp, 64, yb + 52)

    base.convert("RGB").save(out, quality=94, subsampling=1, optimize=True)
    print("écrit", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else FOND)
