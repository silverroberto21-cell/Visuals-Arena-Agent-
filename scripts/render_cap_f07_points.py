#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Récapitulatif 1280×720 — « Maintiens le CAP » : les trois points du thème.

Mêmes éléments que la miniature v2 : **FOND 7**, palette 60/30/10 (bleus du fond,
acier, or pâle), Anton + Montserrat, aucune photo d'orateur, date « Dimanche
8 Novembre 2026 », prédicateur AP Enock MISSIMAHOU. Seul ajout : les trois points.

    python3 scripts/render_cap_f07_points.py livrables/<AAAA-MM-JJ>-recap-....jpg
"""
import importlib
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image, ImageDraw, ImageFilter
import render_cap_f07_texte as T

W, H = T.W, T.H
OR, ACIER = T.OR, T.ACIER

POINTS = [("01", "LA CONFIANCE"), ("02", "L’ALIGNEMENT"), ("03", "LA PERSÉVÉRANCE")]


def main(out, fond=T.FOND):
    bg = T.cover(Image.open(fond).convert("RGB"), W, H)
    bg = bg.filter(ImageFilter.GaussianBlur(1.4))
    bg = bg.filter(ImageFilter.UnsharpMask(radius=3, percent=75, threshold=2))
    bg = Image.eval(bg, lambda v: min(255, int(v * 0.88)))

    base = bg.convert("RGBA")
    base.alpha_composite(T.vgrad(W, H, [
        (0.00, (4, 10, 40, 180)),
        (0.24, (5, 14, 52, 104)),
        (0.52, (5, 14, 52, 62)),
        (0.80, (4, 10, 38, 134)),
        (1.00, (3, 6, 28, 214)),
    ]))
    base.alpha_composite(T.radial(W, H, W * 0.82, H * 0.12, W * 0.46, (60, 140, 235), 50, 90))
    base.alpha_composite(T.radial(W, H, 300, 210, 300, OR, 30, 90))

    d = ImageDraw.Draw(base, "RGBA")

    # ---------- marque
    fm = T.font(T.SANS, 19, "SemiBold")
    m = T.text_mask("ICC PAHOU", fm, 8)
    col = Image.new("RGBA", m.size, ACIER + (255,))
    col.putalpha(m)
    T.paste_left(base, col, 64, 30)
    d.line([(64, 74), (98, 74)], fill=OR + (235,), width=3)
    d.line([(106, 74), (228, 74)], fill=ACIER + (95,), width=1)

    # ---------- titre, colonne de gauche
    f1, s1 = T.fit_width(T.TITRE, "MAINTIENS", 540, start=150)
    print("corps titre :", s1)
    l1 = T.text_mask("MAINTIENS", f1, 1)
    l2 = T.text_mask("LE ", f1, 1)
    l3 = T.text_mask("CAP", f1, 1)
    a1 = T.fill_gradient(l1, (255, 255, 255), (219, 233, 252))
    a2 = T.fill_gradient(l2, (255, 255, 255), (219, 233, 252))
    a3 = T.fill_gradient(l3, (255, 249, 228), OR)

    y1 = 104
    T.paste_left(base, T.drop(a1, 18, 120, (5, 8)), 68, y1 + 7)
    T.paste_left(base, a1, 64, y1)
    h1 = a1.getbbox()[3] - a1.getbbox()[1]
    y2 = y1 + int(h1 * 0.98)
    T.paste_left(base, T.drop(a2, 18, 120, (5, 8)), 68, y2 + 7)
    T.paste_left(base, a2, 64, y2)
    x3 = 64 + a2.getbbox()[2] + 2
    T.paste_left(base, T.drop(a3, 18, 120, (5, 8)), x3 + 3, y2 + 7)
    T.paste_left(base, a3, x3, y2)

    # sous-titre, sous le titre, colonne de gauche
    ysub = y2 + int(h1 * 0.98) + 26
    fs = T.font(T.SANS, 28, "SemiBold")
    xcur = 66
    for txt, colr in (("sa ", (238, 245, 255)), ("Gloire", (250, 222, 158)),
                      (" se manifestera", (238, 245, 255))):
        ms = T.text_mask(txt, fs, 2)
        sub = T.fill_gradient(ms, colr, tuple(max(0, c - 30) for c in colr))
        T.paste_left(base, T.drop(sub, 9, 100, (3, 4)), xcur + 3, ysub + 3)
        T.paste_left(base, sub, xcur, ysub)
        xcur += int(round(ms.width)) - 4

    # ---------- colonne de droite : les trois points
    RX0, RX1 = 690, 1216
    fc = T.font(T.SANS, 16, "SemiBold")
    mc = T.text_mask("LES 3 POINTS DU THÈME", fc, 7)
    cap = Image.new("RGBA", mc.size, OR + (225,))
    cap.putalpha(mc)
    T.paste_left(base, cap, RX0, 116)
    d.line([(RX0 + cap.getbbox()[2] + 22, 130), (RX1, 130)], fill=OR + (110,), width=2)

    rows = [(168, "01", "LA CONFIANCE"), (330, "02", "L’ALIGNEMENT"),
            (492, "03", "LA PERSÉVÉRANCE")]
    for i, (y, num, label) in enumerate(rows):
        # filet de rangée
        d.line([(RX0, y - 12), (RX1, y - 12)], fill=ACIER + (55,), width=1)
        # chiffre
        fnum = T.font(T.TITRE, 78)
        mnum = T.text_mask(num, fnum, 1)
        nb = T.fill_gradient(mnum, (255, 250, 232), OR)
        T.paste_left(base, T.drop(nb, 14, 110, (4, 6)), RX0 + 3, y + 6)
        T.paste_left(base, nb, RX0, y)
        nh = nb.getbbox()[3] - nb.getbbox()[1]

        # libellé, calé sur la ligne de base du chiffre
        fl, size = T.fit_width(T.SANS, label, RX1 - (RX0 + 130), start=38, lo=18)
        try:
            fl.set_variation_by_name("Bold")
        except Exception:
            pass
        ml = T.text_mask(label, fl, 3)
        lab = T.fill_gradient(ml, (255, 255, 255), (212, 229, 250))
        ylab = y + nh - (ml.getbbox()[3] - ml.getbbox()[1]) - 6
        T.paste_left(base, T.drop(lab, 10, 100, (3, 5)), RX0 + 132, ylab + 3)
        T.paste_left(base, lab, RX0 + 129, ylab)

    # ---------- pied
    d.line([(64, 596), (1216, 596)], fill=ACIER + (50,), width=1)

    fl = T.font(T.SANS, 15, "SemiBold")
    ml = T.text_mask("PRÉDICATEUR", fl, 7)
    lab = Image.new("RGBA", ml.size, OR + (225,))
    lab.putalpha(ml)
    T.paste_left(base, lab, 66, 616)

    fn = T.font(T.SANS, 26, "Bold")
    mn = T.text_mask("AP Enock MISSIMAHOU", fn, 2)
    nom = Image.new("RGBA", mn.size, (255, 255, 255, 255))
    nom.putalpha(mn)
    T.paste_left(base, T.drop(nom, 10, 110, (3, 4)), 66, 650)
    T.paste_left(base, nom, 64, 648)

    fd2 = T.font(T.SANS, 26, "Bold")
    mj = T.text_mask("8 NOVEMBRE 2026", fd2, 2)
    jour = T.fill_gradient(mj, (255, 255, 255), (216, 232, 252))
    T.paste_right(base, jour, 1216, 646)

    fd1 = T.font(T.SANS, 15, "SemiBold")
    mdj = T.text_mask("DIMANCHE", fd1, 7)
    dj = Image.new("RGBA", mdj.size, ACIER + (235,))
    dj.putalpha(mdj)
    T.paste_right(base, dj, 1216, 620)

    base.convert("RGB").save(out, quality=94, subsampling=1, optimize=True)
    print("écrit", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else T.FOND)
