#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Miniature YouTube 1280×720 — thème « Les 5 clés… : ROUGE », **sans les points**.

Variante demandée : « c'est juste le thème sans les points ». La miniature ne porte donc que
l'intitulé du thème, comme la miniature du thème CAP : accroche, mot-acrostiche, phrase du
thème. Aucune liste, aucun verbe-clé, aucune référence biblique — elles restent sur le visuel
1280 × 720 du thème.

Le sujet du thème (une clé, cinq clés) est dit par un **motif de clé filaire**, pas par du
texte : c'est le seul ajout, et il remplace la colonne de droite laissée libre.

    python3 scripts/render_rouge_5cles_theme.py <sortie.jpg> [fond]
"""
import math
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, "scripts")
import render_cap_f07_texte as T  # noqa: E402  (bibliothèque partagée du dépôt)

W, H = 1280, 720
DISPLAY = T.TITRE                  # Anton
TEXTE = "polices/jost-var.ttf"     # Jost
FOND = "fonds/f06-bleu-acier-texture.jpg"

# 60 % — bleus mesurés sur f06
NUIT = (4, 34, 58)
BLEU = (4, 99, 152)
CYAN = (10, 176, 217)
# 30 % — secondaire
ACIER = (176, 214, 246)
BLANC = (242, 249, 255)
# 10 % — accent : le ROUGE demandé
ROUGE = (222, 38, 56)
ROUGE_CLAIR = (255, 106, 96)
ROUGE_FONCE = (168, 16, 40)


def fond_bleu(path):
    bg = T.cover(Image.open(path).convert("RGB"), W, H)
    bg = bg.filter(ImageFilter.GaussianBlur(1.2))
    bg = bg.filter(ImageFilter.UnsharpMask(radius=3, percent=70, threshold=2))
    bg = Image.eval(bg, lambda v: min(255, int(v * 0.86)))
    base = bg.convert("RGBA")
    base.alpha_composite(T.vgrad(W, H, [
        (0.00, (4, 16, 32, 196)),
        (0.30, (4, 20, 40, 124)),
        (0.66, (4, 16, 32, 118)),
        (1.00, (3, 10, 22, 226)),
    ]))
    base.alpha_composite(T.radial(W, H, W * 0.90, H * 0.14, W * 0.44, (20, 170, 215), 52, 90))
    base.alpha_composite(T.radial(W, H, W * 0.16, H * 0.90, W * 0.30, ROUGE, 34, 110))
    return base


def texte(base, s, font, x, y, couleur, tracking=0, ombre=True, droite=None, alpha=255):
    m = T.text_mask(s, font, tracking)
    lay = Image.new("RGBA", m.size, tuple(couleur) + (alpha,))
    lay.putalpha(m)
    if ombre:
        sh = T.drop(lay, 10, 95, (3, 5), (2, 8, 14))
        if droite is None:
            T.paste_left(base, sh, x + 2, y + 2)
        else:
            T.paste_right(base, sh, droite + 2, y + 2)
    if droite is None:
        T.paste_left(base, lay, x, y)
    else:
        T.paste_right(base, lay, droite, y)
    return m.width


def cle(w, h, ep=12):
    """Clé filaire de profil : anneau, tige, deux dents — tracés épais à bouts arrondis."""
    S = 3
    Wl, Hl = w * S, h * S
    lay = Image.new("RGBA", (Wl, Hl), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    e = ep * S
    r = h * 0.29 * S                      # rayon EXTÉRIEUR de l'anneau
    cx, cy = r + e, Hl * 0.46
    col = ACIER + (205,)
    # anneau (extérieur + intérieur pour un tracé net)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=e)
    # tige
    x0 = cx + r - e // 2
    x1 = Wl - e
    d.line([(x0, cy), (x1, cy)], fill=col, width=e)
    d.ellipse([x1 - e // 2, cy - e // 2, x1 + e // 2, cy + e // 2], fill=col)
    # dents, sous la tige
    for dx, hh in ((5.6 * e, h * 0.30 * S), (3.0 * e, h * 0.20 * S)):
        xd = Wl - dx - e // 2
        d.line([(xd, cy), (xd, cy + hh)], fill=col, width=e)
        d.ellipse([xd - e // 2, cy + hh - e // 2, xd + e // 2, cy + hh + e // 2], fill=col)
    # liseré rouge sur le haut de l'anneau : l'accent du thème
    d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340, fill=ROUGE_CLAIR + (240,), width=e)
    return lay.resize((w, h), Image.LANCZOS)


def main(out, fond=FOND):
    base = fond_bleu(fond)
    d = ImageDraw.Draw(base, "RGBA")

    # ---------------- marque
    fm = T.font(TEXTE, 18, "SemiBold")
    texte(base, "ICC PAHOU", fm, 56, 48, ACIER, tracking=7, ombre=False)
    d.line([(56, 84), (88, 84)], fill=ROUGE + (245,), width=3)
    d.line([(96, 84), (208, 84)], fill=ACIER + (95,), width=1)

    # ---------------- accroche
    yk = 136
    fk, sk = T.fit_width(DISPLAY, "LES 5 CLÉS", 402, start=82, lo=40)
    texte(base, "LES 5 CLÉS", fk, 52, yk, BLANC, tracking=3)
    d.line([(56, yk + int(sk * 1.14)), (56 + 136, yk + int(sk * 1.14))],
           fill=ROUGE + (238,), width=3)

    # ---------------- le mot-acrostiche, très grand
    fr, sr = T.fit_width(DISPLAY, "ROUGE", 604, start=300, lo=140)
    widths = [fr.getlength(c) for c in "ROUGE"]
    asc, desc = fr.getmetrics()
    L = Image.new("L", (int(sum(widths)) + 40, asc + desc + 24), 0)
    dl = ImageDraw.Draw(L)
    xx = 8
    for c, cw in zip("ROUGE", widths):
        dl.text((xx, 10), c, font=fr, fill=255)
        xx += cw - 1
    grad = T.fill_gradient(L, ROUGE_CLAIR, ROUGE_FONCE)
    yR = yk + int(sk * 1.14) + 34
    T.paste_left(base, T.drop(grad, 28, 155, (6, 11), (24, 0, 6)), 54, yR + 9)
    T.paste_left(base, grad, 46, yR)
    hR = grad.getbbox()[3] - grad.getbbox()[1]

    # ---------------- phrase du thème
    ys = yR + hR + 28
    fs = T.font(TEXTE, 40, "SemiBold")
    texte(base, "pour vivre une vie", fs, 56, ys, BLANC, tracking=1)
    texte(base, "chrétienne victorieuse", fs, 56, ys + 50, BLANC, tracking=1)

    # ---------------- motif : la clé, filaire, à droite (entièrement dans le cadre)
    kw, kh = 470, 190
    k = cle(kw, kh, ep=11).rotate(-15, resample=Image.BICUBIC, expand=True)
    kx = 1216 - k.width
    ky = 168
    glow = k.filter(ImageFilter.GaussianBlur(20))
    rgl = Image.new("RGBA", glow.size, ROUGE + (0,))
    rgl.putalpha(glow.getchannel("A").point(lambda v: int(v * 0.5)))
    base.alpha_composite(rgl, (kx - 8, ky - 8))
    base.alpha_composite(k, (kx, ky))

    # cinq pastilles d'accent sous la clé : le compte des cinq clés, sans un mot
    yc = ky + k.height + 54
    for i in range(5):
        cx = kx + 26 + i * 40
        d.ellipse([cx - 7, yc - 7, cx + 7, yc + 7], fill=ROUGE + (245,))
        d.ellipse([cx - 3, yc - 3, cx + 3, yc + 3], fill=BLANC + (200,))

    base.convert("RGB").save(out, quality=94, subsampling=1, optimize=True)
    print("écrit", out, "· ROUGE", sr, "· accroche", sk)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else FOND)
