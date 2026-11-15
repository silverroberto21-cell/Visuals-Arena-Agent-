#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Miniature YouTube 1280×720 — « Les 5 clés pour vivre une vie chrétienne victorieuse : ROUGE ».

Composition **sans photo** : le thème est un acrostiche, la typographie porte tout le visuel.
Même doctrine que le reste de la série : le bleu du fond reste la dominante (~60 %), l'acier la
secondaire (~30 %), et le **ROUGE demandé** joue l'accent (~10 %) — il saute aux yeux sans
peindre la miniature en rouge.

Lisibilité en vignette : deux blocs seulement.
- à gauche, l'accroche et le mot-acrostiche en très grand ;
- à droite, les cinq lettres-clés avec leur verbe.

    python3 scripts/render_rouge_5cles_miniature.py <sortie.jpg> [fond]

Textes : les cinq verbes et leurs références sont recopiés à la lettre depuis la demande.
Les gloses (« Continuellement la présence de Dieu », etc.) restent sur le récapitulatif
1280×720 du thème — une miniature ne porte pas trois niveaux de texte.
"""
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageChops

sys.path.insert(0, "scripts")
import render_cap_f07_texte as T  # noqa: E402  (bibliothèque partagée du dépôt)

W, H = 1280, 720
DISPLAY = T.TITRE                  # Anton — capitales condensées
TEXTE = "polices/jost-var.ttf"     # Jost — géométrique, lisible en petit
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

CLE = [("R", "RECHERCHER", "Psaume 105:4"),
       ("O", "OBÉIR", "Josué 1:8"),
       ("U", "UTILISER", "Éphésiens 6:11-18"),
       ("G", "GARDER", "Proverbes 4:23"),
       ("E", "ENDURER", "Matthieu 24:13")]


def fond_bleu(path):
    bg = T.cover(Image.open(path).convert("RGB"), W, H)
    bg = bg.filter(ImageFilter.GaussianBlur(1.2))
    bg = bg.filter(ImageFilter.UnsharpMask(radius=3, percent=70, threshold=2))
    bg = Image.eval(bg, lambda v: min(255, int(v * 0.86)))
    base = bg.convert("RGBA")
    base.alpha_composite(T.vgrad(W, H, [
        (0.00, (4, 16, 32, 190)),
        (0.30, (4, 20, 40, 120)),
        (0.66, (4, 16, 32, 110)),
        (1.00, (3, 10, 22, 224)),
    ]))
    base.alpha_composite(T.radial(W, H, W * 0.90, H * 0.12, W * 0.44, (20, 170, 215), 54, 90))
    base.alpha_composite(T.radial(W, H, W * 0.13, H * 0.88, W * 0.30, ROUGE, 40, 110))
    return base


def texte(base, s, font, x, y, couleur, tracking=0, ombre=True, droite=None, alpha=255,
          flou=8, ombre_alpha=88):
    m = T.text_mask(s, font, tracking)
    lay = Image.new("RGBA", m.size, tuple(couleur) + (alpha,))
    lay.putalpha(m)
    if ombre:
        sh = T.drop(lay, flou, ombre_alpha, (3, 5), (2, 8, 14))
        if droite is None:
            T.paste_left(base, sh, x + 2, y + 2)
        else:
            T.paste_right(base, sh, droite + 2, y + 2)
    if droite is None:
        T.paste_left(base, lay, x, y)
    else:
        T.paste_right(base, lay, droite, y)
    return m.width


def lettre_rouge(base, ch, x, y, size):
    f = T.font(DISPLAY, size)
    m = T.text_mask(ch, f, 0)
    lay = T.fill_gradient(m, ROUGE_CLAIR, ROUGE_FONCE)
    T.paste_left(base, T.drop(lay, 16, 135, (5, 7), (20, 0, 4)), x + 3, y + 4)
    T.paste_left(base, lay, x, y)
    return lay.getbbox()[3] - lay.getbbox()[1]


def main(out, fond=FOND):
    base = fond_bleu(fond)
    d = ImageDraw.Draw(base, "RGBA")

    # ---------------- marque
    fm = T.font(TEXTE, 17, "SemiBold")
    texte(base, "ICC PAHOU", fm, 54, 46, ACIER, tracking=7, ombre=False)
    d.line([(54, 80), (86, 80)], fill=ROUGE + (245,), width=3)
    d.line([(94, 80), (206, 80)], fill=ACIER + (95,), width=1)

    # ---------------- accroche : LES 5 CLÉS
    yk = 132
    fk, sk = T.fit_width(DISPLAY, "LES 5 CLÉS", 396, start=76, lo=34)
    texte(base, "LES 5 CLÉS", fk, 50, yk, BLANC, tracking=3)
    d.line([(54, yk + int(sk * 1.14)), (54 + 132, yk + int(sk * 1.14))],
           fill=ROUGE + (235,), width=3)

    # ---------------- le mot-acrostiche, très grand
    fr, sr = T.fit_width(DISPLAY, "ROUGE", 520, start=260, lo=120)
    widths = [fr.getlength(c) for c in "ROUGE"]
    asc, desc = fr.getmetrics()
    L = Image.new("L", (int(sum(widths)) + 40, asc + desc + 24), 0)
    dl = ImageDraw.Draw(L)
    xx = 8
    for c, cw in zip("ROUGE", widths):
        dl.text((xx, 10), c, font=fr, fill=255)
        xx += cw - 1
    grad = T.fill_gradient(L, ROUGE_CLAIR, ROUGE_FONCE)
    yR = yk + int(sk * 1.14) + 30
    T.paste_left(base, T.drop(grad, 26, 150, (6, 10), (24, 0, 6)), 52, yR + 8)
    T.paste_left(base, grad, 46, yR)
    hR = grad.getbbox()[3] - grad.getbbox()[1]

    # ---------------- sous-titre
    ys = yR + hR + 22
    fs = T.font(TEXTE, 35, "SemiBold")
    texte(base, "pour vivre une vie", fs, 54, ys, BLANC, tracking=1)
    texte(base, "chrétienne victorieuse", fs, 54, ys + 44, BLANC, tracking=1)

    # légende du procédé, en pied de colonne : elle occupe le vide et explique le visuel
    yc = ys + 44 + 62
    d.line([(54, yc), (150, yc)], fill=ROUGE + (225,), width=3)
    fc = T.font(TEXTE, 15, "SemiBold")
    texte(base, "ACROSTICHE  ·  CINQ CLÉS", fc, 54, yc + 14, ACIER, tracking=6,
          alpha=225, ombre=False)

    # ---------------- colonne de droite : plaque très légèrement assombrie.
    # Elle ne sert qu'à garantir le contraste des cinq clés partout où tombe la lumière du
    # fond : sans elle, la référence biblique perdait jusqu'à 1,8:1 sur le halo cyan.
    X0, X1 = 726, 1226
    TOP, BOT = 96, 636
    pas = (BOT - TOP) / 5.0

    # plaque : dégradé horizontal, opaque à droite, transparent à gauche
    plaque = T.vgrad(1, 1, [(0, (2, 12, 22, 0)), (1, (2, 12, 22, 0))])  # placeholder
    plate = Image.new("L", (W - X0 + 40, H), 0)
    pd = ImageDraw.Draw(plate)
    for k in range(W - X0 + 40):
        pd.line([(k, 0), (k, H)], fill=int(215 * (k / (W - X0 + 40)) ** 0.85))
    veil = Image.new("RGBA", (W - X0 + 40, H), (2, 10, 20, 255))
    veil.putalpha(plate)
    base.alpha_composite(veil, (X0 - 40, 0))
    for i, (ch, verbe, ref) in enumerate(CLE):
        y = TOP + i * pas
        d.line([(X0, y), (X1, y)], fill=ACIER + (58,), width=1)

        lettre_rouge(base, ch, X0 + 2, y + 18, 70)

        # verbe à gauche, référence à droite, sur la MÊME ligne de base : c'est ainsi que
        # les cinq clés se balaient d'un seul regard, même en vignette de téléphone.
        fv, sv = T.fit_width(DISPLAY, verbe, 288, start=46, lo=20)
        mv = T.text_mask(verbe, fv, 2)
        lv = Image.new("RGBA", mv.size, BLANC + (255,))
        lv.putalpha(mv)
        hv = mv.getbbox()[3] - mv.getbbox()[1]
        yv = y + 20 + (pas - 14 - hv) / 2
        T.paste_left(base, lv, X0 + 92, yv)

        fr2 = T.font(TEXTE, 21, "SemiBold")
        mr = T.text_mask(ref, fr2, 1)
        lr = Image.new("RGBA", mr.size, ACIER + (250,))
        lr.putalpha(mr)
        hr = mr.getbbox()[3] - mr.getbbox()[1]
        T.paste_right(base, lr, X1 - 2, yv + hv - hr)

    d.line([(X0, BOT), (X1, BOT)], fill=ACIER + (105,), width=1)

    base.convert("RGB").save(out, quality=94, subsampling=1, optimize=True)
    print("écrit", out, "· ROUGE", sr, "· accroche", sk)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else FOND)
