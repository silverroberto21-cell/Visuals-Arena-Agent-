#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Miniature « Atmosphère de Prière » sur FOND 18, orateur (AP) intégré.

Même fond travaillé, mêmes polices, mêmes textes, même structure que l'essai
FOND 18 (scripts/render_essai_4fonds.py : build_background + gouttière) ;
seul ajout : la photo de l'orateur, posée en panneau fondu à droite, et le bloc
de titre resserré (corps réduit, colonne décalée à gauche) pour lui laisser la place.
Traitement de la photo : recadrage + lumière, aucune retouche du sujet.
"""
import importlib
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops

sys.path.insert(0, "scripts")
E = importlib.import_module("render_essai_4fonds")

W, H = E.W, E.H
VIOLET = E.VIOLET
MENTHE = E.MENTHE
ACIER = E.ACIER
F18 = [j for j in E.JOBS if j["out"] == "miniature-fond18.jpg"][0]

TITLE_W = 600          # largeur utile du titre (colonne de gauche)
COL_CX = 340           # axe du bloc de titre
PANEL_W = 722          # largeur du panneau photo (photo entière, hauteur 720)


def orator_panel(path, w, h, crop_left=0.0, grade=0.32, feather=0.26, dark=0.96):
    im = Image.open(path).convert("RGB")
    sw, sh = im.size
    if crop_left:
        im = im.crop((int(sw * crop_left), 0, sw, sh))
    # photo entière, calée sur la hauteur de la vignette, recadrée par la droite
    im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    if im.width > w:
        im = im.crop((im.width - w, 0, im.width, h))
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=65, threshold=3))

    wash = Image.eval(Image.new("RGB", im.size, VIOLET), lambda v: int(v * 0.5))
    im = Image.blend(im, ImageChops.screen(im, wash), grade)
    # lumière : bascule douce des tons moyens vers le haut (sujet lisible en vignette)
    im = Image.eval(im, lambda v: min(255, int(255 * (v / 255) ** 0.86)))
    im = Image.eval(im, lambda v: min(255, max(0, int((v - 128) * 1.06 + 130))))
    if dark != 1.0:
        im = Image.eval(im, lambda v: min(255, int(v * dark)))

    # le côté qui porte le texte est assombri : le raccord se fait dans l'ombre
    rgba = im.convert("RGBA")
    shade = Image.new("RGBA", rgba.size, (7, 9, 38, 0))
    grad = Image.new("L", (w, 1), 0)
    gp = grad.load()
    span = int(w * 0.30)
    # le raccord se fait dans l'ombre du bord gauche seulement : le sujet reste en pleine
    # lumière (son visage commence à ~20 % du panneau)
    for x in range(span):
        k = (1 - x / span) ** 1.5
        gp[x, 0] = int(96 * k)
    for x in range(span, w):
        gp[x, 0] = 0
    shade.putalpha(grad.resize((w, h)))
    rgba = Image.alpha_composite(rgba, shade)

    ramp = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(ramp)
    f = int(w * feather)
    for x in range(f):
        d.line([(x, 0), (x, h)], fill=int(255 * (x / f) ** 1.5))
    rgba.putalpha(ramp)
    return rgba


def main(photo, out, fond=None):
    base = E.build_background(F18, ".")

    panel = orator_panel(photo, PANEL_W, H)
    base.alpha_composite(panel, (W - PANEL_W, 0))

    d = ImageDraw.Draw(base, "RGBA")
    d.polygon([(96, 74), (128, 74), (112, 104)], fill=MENTHE + (215,))
    d.line([(150, 88), (COL_CX + TITLE_W / 2, 88)], fill=MENTHE + (70,), width=2)

    f, size = E.fit(E.TITRE_TTF, E.TITRE_VAR, "ATMOSPHÈRE", TITLE_W, start=140)
    print("corps du titre :", size)
    l1 = E.fill_gradient(E.text_mask("ATMOSPHÈRE", f, 1), (255, 255, 255), (226, 233, 250))
    l2 = E.fill_gradient(E.text_mask("DE PRIÈRE", f, 1), (255, 255, 255), (226, 233, 250))
    s1 = E.drop(l1, 16, 120, (5, 7))
    s2 = E.drop(l2, 16, 120, (5, 7))
    lh = size * 1.16          # interligne du modèle d'origine (vignette de référence)
    cy1, cy2 = 300, 300 + lh
    for sh, lay, cy in ((s1, l1, cy1), (s2, l2, cy2)):
        E.paste_center(base, sh, COL_CX - 3, cy + 4)
        E.paste_center(base, lay, COL_CX, cy)

    fs = E.var_font(E.SANS_TTF, 24, E.SANS_VAR)
    mt = E.text_mask("À ICC PAHOU", fs, 9)
    col = Image.new("RGBA", mt.size, MENTHE + (255,))
    col.putalpha(mt)
    y = cy2 + 92
    E.paste_center(base, col, COL_CX, y)
    wl = mt.width / 2 + 36
    d.line([(COL_CX - wl - 84, y), (COL_CX - wl, y)], fill=ACIER + (200,), width=2)
    d.line([(COL_CX + wl, y), (COL_CX + wl + 84, y)], fill=ACIER + (200,), width=2)

    base.convert("RGB").save(out, quality=93, subsampling=1, optimize=True)
    print("écrit", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
