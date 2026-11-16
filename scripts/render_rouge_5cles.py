#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Visuel 1280×720 — « Les 5 clés pour vivre une vie chrétienne victorieuse : ROUGE ».

La demande porte une **couleur imposée** : ROUGE. Elle est traitée comme l'**accent** (~10 %)
du visuel — le mot ROUGE, les lettres-clés, les chiffres et les filets — jamais comme teinte
de fond : le bleu du FOND 6 reste la dominante (~60 %), l'acier la secondaire (~30 %).

Acrostiche recopié à la lettre : R · O · U · G · E, chacun avec son verbe, sa glose et sa
référence biblique. Aucune date, aucun orateur : rien n'est inventé, la note le signale.

    python3 scripts/render_rouge_5cles.py <sortie.jpg> [fond]
"""
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, "scripts")
import render_cap_f07_texte as T  # noqa: E402  (bibliothèque partagée du dépôt)

W, H = 1280, 720
SANS = "polices/jost-var.ttf"       # texte : géométrique, très lisible en petit
TITRE = T.TITRE                     # Anton, capitales condensées
FOND = "fonds/f06-bleu-acier-texture.jpg"

# 60 % — bleus mesurés sur f06 (#046398 / #02446A / #058BBE / #0AB0D9)
NUIT = (4, 34, 58)
BLEU = (4, 99, 152)
CYAN = (10, 176, 217)
# 30 % — secondaire
ACIER = (176, 214, 246)
BLANC = (240, 247, 255)
# 10 % — accent : le ROUGE demandé
ROUGE = (222, 38, 56)
ROUGE_CLAIR = (255, 106, 96)
ROUGE_FONCE = (168, 16, 40)

CLE = [
    ("R", "RECHERCHER", "Continuellement la présence de Dieu.", "Psaume 105:4"),
    ("O", "OBÉIR", "À la Parole de Dieu.", "Josué 1:8"),
    ("U", "UTILISER", "Les armes spirituelles.", "Éphésiens 6:11-18"),
    ("G", "GARDER", "Son cœur et sa foi.", "Proverbes 4:23"),
    ("E", "ENDURER", "Jusqu’à la fin dans la foi.", "Matthieu 24:13"),
]


def fond_bleu(path):
    bg = T.cover(Image.open(path).convert("RGB"), W, H)
    bg = bg.filter(ImageFilter.GaussianBlur(1.2))
    bg = bg.filter(ImageFilter.UnsharpMask(radius=3, percent=70, threshold=2))
    bg = Image.eval(bg, lambda v: min(255, int(v * 0.90)))
    base = bg.convert("RGBA")
    base.alpha_composite(T.vgrad(W, H, [
        (0.00, (4, 18, 36, 176)),
        (0.28, (4, 22, 44, 104)),
        (0.62, (4, 18, 36, 84)),
        (1.00, (3, 12, 26, 212)),
    ]))
    base.alpha_composite(T.radial(W, H, W * 0.88, H * 0.16, W * 0.42, (20, 170, 215), 46, 90))
    base.alpha_composite(T.radial(W, H, W * 0.16, H * 0.80, W * 0.30, ROUGE, 40, 110))
    return base


def lettre(base, ch, x, y, size, clair=ROUGE_CLAIR, couleur=ROUGE):
    """Une lettre-clé : Anton plein, dégradé rouge, ombre portée. Renvoie sa hauteur."""
    f = T.font(TITRE, size)
    m = T.text_mask(ch, f, 1)
    lay = T.fill_gradient(m, clair, couleur)
    T.paste_left(base, T.drop(lay, 16, 120, (4, 6)), x + 3, y + 4)
    T.paste_left(base, lay, x, y)
    return lay.getbbox()[3] - lay.getbbox()[1]


def texte(base, txt, font, x, y, couleur, tracking=0, droite=None, ombre=True):
    """Pose un texte ; renvoie sa largeur. `droite` = bord droit visé."""
    m = T.text_mask(txt, font, tracking)
    lay = Image.new("RGBA", m.size, couleur + (255,))
    lay.putalpha(m)
    if droite is None:
        if ombre:
            T.paste_left(base, T.drop(lay, 9, 95, (3, 4)), x + 2, y + 2)
        T.paste_left(base, lay, x, y)
    else:
        T.paste_right(base, lay, droite, y)
    return m.width


def main(out, fond=FOND):
    base = fond_bleu(fond)
    d = ImageDraw.Draw(base, "RGBA")

    # ================= colonne de gauche : l'accroche =================
    fk, sk = T.fit_width(TITRE, "LES 5 CLÉS", 396, start=62, lo=30)
    mk = T.text_mask("LES 5 CLÉS", fk, 3)
    hk = mk.getbbox()[3] - mk.getbbox()[1]

    fr, sr = T.fit_width(TITRE, "ROUGE", 388, start=178, lo=90)
    widths = [fr.getlength(c) for c in "ROUGE"]
    asc, desc = fr.getmetrics()
    L = Image.new("L", (int(sum(widths)) + 40, asc + desc + 24), 0)
    dl = ImageDraw.Draw(L)
    xx = 8
    for c, cw in zip("ROUGE", widths):
        dl.text((xx, 10), c, font=fr, fill=255)
        xx += cw + 1
    grad = T.fill_gradient(L, ROUGE_CLAIR, ROUGE_FONCE)
    hr = grad.getbbox()[3] - grad.getbbox()[1]

    y_marque = 44
    y_acc = 138                       # « LES 5 CLÉS »
    y_rouge = y_acc + hk + 44         # « ROUGE »
    y_sub = y_rouge + hr + 26         # sous-titre, sous l'encre du mot

    # marque
    fm = T.font(SANS, 19, "SemiBold")
    texte(base, "ICC PAHOU", fm, 62, y_marque, ACIER, tracking=8, ombre=False)
    d.line([(62, y_marque + 34), (96, y_marque + 34)], fill=ROUGE + (240,), width=3)
    d.line([(104, y_marque + 34), (226, y_marque + 34)], fill=ACIER + (95,), width=1)

    texte(base, "LES 5 CLÉS", fk, 58, y_acc, BLANC, tracking=3)
    d.line([(62, y_acc + hk + 14), (62 + 150, y_acc + hk + 14)], fill=ROUGE + (225,), width=3)

    T.paste_left(base, T.drop(grad, 26, 145, (6, 10)), 60, y_rouge + 8)
    T.paste_left(base, grad, 54, y_rouge)

    fs = T.font(SANS, 30, "Medium")
    for i, line in enumerate(("pour vivre une vie", "chrétienne victorieuse")):
        texte(base, line, fs, 60, y_sub + i * 37, BLANC, tracking=1)

    # légende de la figure, sous le sous-titre
    y_cap = y_sub + 2 * 37 + 16
    f5 = T.font(SANS, 14, "Medium")
    texte(base, "ACROSTICHE  ·  CINQ CLÉS", f5, 62, y_cap, ACIER, tracking=3, ombre=False)

    # séparateur vertical entre les deux colonnes
    d.line([(462, 96), (462, 664)], fill=ACIER + (34,), width=1)

    # ================= colonne de droite : les cinq clés =================
    X0, X1 = 506, 1224
    TOP, BOT = 100, 656
    pas = (BOT - TOP) / 5.0

    for i, (ch, verbe, glose, ref) in enumerate(CLE):
        y = TOP + i * pas
        d.line([(X0, y), (X1, y)], fill=ACIER + (60,), width=1)

        # lettre-clé
        lettre(base, ch, X0 + 2, y + 16, 56)

        # verbe (titre) puis glose (texte)
        fv = T.font(TITRE, 33)
        texte(base, verbe, fv, X0 + 68, y + 14, BLANC, tracking=2)
        fg = T.font(SANS, 22, "Regular")
        texte(base, glose, fg, X0 + 70, y + 60, ACIER, tracking=0, ombre=False)

        # référence biblique, à droite, sur la ligne du verbe
        frf = T.font(SANS, 21, "SemiBold")
        texte(base, ref, frf, 0, y + 34, (236, 245, 255), tracking=1, droite=X1, ombre=True)

    d.line([(X0, BOT), (X1, BOT)], fill=ACIER + (110,), width=1)


    base.convert("RGB").save(out, quality=94, subsampling=1, optimize=True)
    print("écrit", out, "· corps ROUGE", sr, "· corps accroche", sk)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else FOND)
