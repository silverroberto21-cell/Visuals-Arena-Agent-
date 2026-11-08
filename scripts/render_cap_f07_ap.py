#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Miniature 1280×720 — « Maintiens le CAP » : le flyer du thème (sans les points)
+ l'orateur AP découpé de la photo fournie.

Mêmes briques que la miniature v2 (`render_cap_f07_texte.py`) : **même fond f07**,
même palette (bleus mesurés sur f07 + acier + or pâle), même duo Anton + Montserrat,
mêmes textes, mêmes filets, même grain de lumière. Ce qui bouge : le sujet prend la
colonne de droite, la date et le prédicateur se rangent sous le titre.

    python3 scripts/render_cap_f07_ap.py <photo_decoupee.png> <out.jpg>
"""
import importlib
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import render_cap_f07_texte as T

W, H = T.W, T.H
OR, ACIER = T.OR, T.ACIER

PANEL_W = 500          # largeur du panneau du sujet, calé à droite
TOP = 30               # le sujet ne touche pas le bord haut
RIGHT = 34             # ni le bord droit
BOTTOM_FADE = 76       # le bas du buste se dissout dans le fond


def prepare_subject(path):
    """Sujet découpé : recadrage + lumière + accord d'ambiance, jamais de retouche."""
    im = Image.open(path).convert("RGBA")
    # on ne garde que la partie utile : tête → mains, pas les jambes coupées
    sw, sh = im.size
    im = im.crop((0, 0, sw, int(sh * 0.96)))
    h = H - TOP - 10
    w = round(im.width * h / im.height)
    im = im.resize((w, h), Image.LANCZOS)

    rgb = im.convert("RGB")
    rgb = Image.eval(rgb, lambda v: min(255, int(255 * (v / 255) ** 0.90)))
    rgb = Image.eval(rgb, lambda v: min(255, max(0, int((v - 128) * 1.05 + 132))))
    wash = Image.eval(Image.new("RGB", rgb.size, T.ACIER), lambda v: int(v * 0.5))
    rgb = Image.blend(rgb, ImageChops.screen(rgb, wash), 0.18)   # accord, pas virage
    out = rgb.convert("RGBA")
    out.putalpha(im.split()[3])
    return out


def place_subject(base, sub, panel_w=PANEL_W, feather=0.16):
    h = sub.height
    canvas = Image.new("RGBA", (panel_w, h), (0, 0, 0, 0))
    canvas.alpha_composite(sub, (panel_w - sub.width, 0))

    # le fond reprend la main sur le bord gauche du panneau
    f = int(panel_w * feather)
    ramp = Image.new("L", (panel_w, h), 255)
    d = ImageDraw.Draw(ramp)
    for x in range(f):
        d.line([(x, 0), (x, h)], fill=int(255 * (x / f) ** 1.25))
    # fondu bas : le buste se dissout, pas de coupe nette au ras du cadre
    bot = Image.new("L", (panel_w, h), 255)
    db = ImageDraw.Draw(bot)
    for y in range(h - BOTTOM_FADE, h):
        k = (y - (h - BOTTOM_FADE)) / BOTTOM_FADE
        db.line([(0, y), (panel_w, y)], fill=int(255 * (1 - k) ** 1.7))
    ramp = ImageChops.multiply(ramp, bot)
    canvas.putalpha(ImageChops.multiply(canvas.split()[3], ramp))

    # ombre portée : le sujet se détache du bokeh
    sh = Image.new("RGBA", (panel_w + 220, h + 80), (0, 0, 0, 0))
    sil = canvas.split()[3].point(lambda v: int(v * 0.5))
    sh.paste(Image.new("RGBA", canvas.size, (3, 8, 30, 255)), (130, 26), sil)
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(28)), (W - panel_w - 110 - RIGHT, TOP - 26))
    base.alpha_composite(canvas, (W - panel_w - RIGHT, TOP))


def caption(base, d):
    """Colonne de gauche : titre + sous-titre + date + prédicateur."""
    target = 600
    f1, s1 = T.fit_width(T.TITRE, "MAINTIENS", target, start=190)
    f2, s2 = T.fit_width(T.TITRE, "LE CAP", target, start=190)
    print("corps:", s1, s2)
    l1 = T.fill_gradient(T.text_mask("MAINTIENS", f1, 1), (255, 255, 255), (219, 233, 252))
    l2 = T.fill_gradient(T.text_mask("LE", f2, 1), (255, 255, 255), (219, 233, 252))
    l3 = T.fill_gradient(T.text_mask("CAP", f2, 1), (255, 249, 228), OR)

    y1 = 128
    T.paste_left(base, T.drop(l1, 20, 120, (5, 9)), 68, y1 + 8)
    T.paste_left(base, l1, 64, y1)
    h1 = l1.getbbox()[3] - l1.getbbox()[1]
    y2 = y1 + int(h1 * 0.98)
    T.paste_left(base, T.drop(l2, 20, 120, (5, 9)), 68, y2 + 8)
    T.paste_left(base, l2, 64, y2)
    cap_x = 64 + l2.getbbox()[2] + 28
    T.paste_left(base, T.drop(l3, 20, 120, (5, 9)), cap_x + 4, y2 + 8)
    T.paste_left(base, l3, cap_x, y2)

    cap_h = l3.getbbox()[3] - l3.getbbox()[1]
    ysub = y2 + int(cap_h * 0.98) + 26
    fs = T.font(T.SANS, 32, "SemiBold")
    xcur = 66
    for txt, col in (("sa ", (238, 245, 255)), ("Gloire", (250, 222, 158)),
                     (" se manifestera", (238, 245, 255))):
        ms = T.text_mask(txt, fs, 2)
        sub = T.fill_gradient(ms, col, tuple(max(0, c - 30) for c in col))
        T.paste_left(base, T.drop(sub, 10, 100, (3, 5)), xcur + 3, ysub + 4)
        T.paste_left(base, sub, xcur, ysub)
        xcur += int(round(ms.width)) - 4

    # filet + date
    yb = ysub + 104
    d.line([(64, yb), (300, yb)], fill=OR + (200,), width=2)

    fd = T.font(T.SANS, 20, "SemiBold")
    md = T.text_mask("DIMANCHE 8 NOVEMBRE 2026", fd, 5)
    cold = Image.new("RGBA", md.size, OR + (245,))
    cold.putalpha(md)
    T.paste_left(base, cold, 64, yb + 18)

    fl = T.font(T.SANS, 15, "SemiBold")
    ml = T.text_mask("PRÉDICATEUR", fl, 7)
    lab = Image.new("RGBA", ml.size, ACIER + (215,))
    lab.putalpha(ml)
    T.paste_left(base, lab, 64, yb + 58)

    fn = T.font(T.SANS, 27, "Bold")
    mn = T.text_mask("AP Enock MISSIMAHOU", fn, 2)
    nom = Image.new("RGBA", mn.size, (255, 255, 255, 255))
    nom.putalpha(mn)
    T.paste_left(base, T.drop(nom, 10, 110, (3, 4)), 66, yb + 90)
    T.paste_left(base, nom, 64, yb + 88)


def main(photo, out, fond=T.FOND):
    bg = T.cover(Image.open(fond).convert("RGB"), W, H)
    bg = bg.filter(ImageFilter.GaussianBlur(1.4))
    bg = bg.filter(ImageFilter.UnsharpMask(radius=3, percent=75, threshold=2))
    bg = Image.eval(bg, lambda v: min(255, int(v * 0.88)))

    base = bg.convert("RGBA")
    base.alpha_composite(T.vgrad(W, H, [
        (0.00, (4, 10, 40, 172)),
        (0.24, (5, 14, 52, 92)),
        (0.50, (5, 14, 52, 40)),
        (0.80, (4, 10, 38, 122)),
        (1.00, (3, 6, 28, 208)),
    ]))
    base.alpha_composite(T.radial(W, H, W * 0.78, H * 0.16, W * 0.52, (60, 140, 235), 50, 90))
    base.alpha_composite(T.radial(W, H, 330, 470, 320, OR, 34, 90))

    # sujet AVANT le texte : il vit derrière, le titre reste net devant
    place_subject(base, prepare_subject(photo))

    d = ImageDraw.Draw(base, "RGBA")

    # marque
    fm = T.font(T.SANS, 19, "SemiBold")
    m = T.text_mask("ICC PAHOU", fm, 8)
    col = Image.new("RGBA", m.size, ACIER + (255,))
    col.putalpha(m)
    T.paste_left(base, col, 68, 46)
    d.line([(68, 90), (102, 90)], fill=OR + (235,), width=3)
    d.line([(110, 90), (232, 90)], fill=ACIER + (95,), width=1)

    caption(base, d)

    base.convert("RGB").save(out, quality=94, subsampling=1, optimize=True)
    print("écrit", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else T.FOND)
