#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thème RECTIFIÉ — « ALERTE CODE R.O.U.G.E : les 5 clés pour vivre une chrétienne victorieuse ».

Rectification du 2026-11-07 : l'intitulé du thème change. « LES 5 CLÉS / ROUGE » devient
**« ALERTE CODE R.O.U.G.E »** en accroche, avec la phrase du thème en sous-titre. Le mot-code
s'écrit **avec ses points**, exactement comme la source le donne (« R.O.U.G.E »).

Quatre variantes, un seul bloc typographique pour qu'elles ne divergent jamais :

* ``theme``     — miniature 1280×720 du thème seul (motif : clé filaire + cinq pastilles) ;
* ``ap``        — miniature 1280×720 avec **AP Enock MISSIMAHOU** détouré, FOND 6 ;
* ``ap-fond26`` — même miniature, fond fourni **FOND 26** ramené au bleu (variante v2) ;
* ``visuel``    — visuel 1280×720 portant **les cinq clés**, leurs gloses et leurs références.

Les fonds, le détourage et le placement du sujet sont **repris tels quels** du rendu précédent
(`render_rouge_5cles_ap.py`) : une seule source de vérité pour la lumière et la silhouette.
La photo de l'orateur est **coupée en bas à la source** → ancrage au bord bas, aucun rognage
(`specs/photos-sujet.md`), et **aucun outil génératif** sur le visage, la peau ou la tenue.

    python3 scripts/render_alerte_code_rouge.py <theme|ap|ap-fond26|visuel> <sortie.jpg>
"""
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, "scripts")
import render_cap_f07_texte as T          # noqa: E402  (bibliothèque partagée : font, cover, radial…)
import render_rouge_5cles_ap as AP        # noqa: E402  (fonds, décontamination, placement du sujet)
import render_rouge_5cles_theme as TH     # noqa: E402  (motif de la clé filaire)

W, H = 1280, 720
DISPLAY = T.TITRE                  # Anton
TEXTE = "polices/jost-var.ttf"     # Jost — duo du thème

ACIER = AP.ACIER
BLANC = AP.BLANC
ROUGE = AP.ROUGE
ROUGE_CLAIR = AP.ROUGE_CLAIR
ROUGE_FONCE = AP.ROUGE_FONCE

MARQUE = "ICC PAHOU"
ACCROCHE = "ALERTE CODE"                       # recopié à la lettre
CODE = "R.O.U.G.E"                             # recopié à la lettre, points compris
PHRASE = "les 5 clés pour vivre une chrétienne victorieuse"
ORATEUR = "AP Enock"                           # nom demandé : sans le patronyme
# Césures préférées : elles tombent sur une frontière de sens (« … pour vivre » / « une … »).
# Elles ne sont retenues que si elles tiennent dans la colonne ; sinon `retours()` décide.
CESURES = (("les 5 clés pour vivre", "une chrétienne victorieuse"),
           ("les 5 clés", "pour vivre une chrétienne victorieuse"))

CLE = [
    ("R", "RECHERCHER", "Continuellement la présence de Dieu.", "Psaume 105:4"),
    ("O", "OBÉIR", "À la Parole de Dieu.", "Josué 1:8"),
    ("U", "UTILISER", "Les armes spirituelles.", "Éphésiens 6:11-18"),
    ("G", "GARDER", "Son cœur et sa foi.", "Proverbes 4:23"),
    ("E", "ENDURER", "Jusqu’à la fin dans la foi.", "Matthieu 24:13"),
]


# --------------------------------------------------------------------------- outils
def texte(base, s, fnt, x, y, couleur, tracking=0, ombre=True, alpha=255):
    """Pose un texte aligné sur son bord gauche d'encre ; renvoie (largeur, hauteur)."""
    m = T.text_mask(s, fnt, tracking)
    lay = Image.new("RGBA", m.size, tuple(couleur) + (alpha,))
    lay.putalpha(m)
    if ombre:
        T.paste_left(base, T.drop(lay, 10, 95, (3, 5), (2, 8, 14)), x + 2, y + 3)
    T.paste_left(base, lay, x, y)
    bb = m.getbbox()
    return bb[2] - bb[0], bb[3] - bb[1]


def mesure(s, fnt, tracking=0):
    bb = T.text_mask(s, fnt, tracking).getbbox()
    return bb[2] - bb[0], bb[3] - bb[1]


def fit(s, target, start=200, lo=30):
    return T.fit_width(DISPLAY, s, target, start=start, lo=lo)


def retours(phrase, fnt, largeur):
    """Découpe la phrase en lignes **équilibrées** : le moins de lignes possible, puis la
    répartition qui minimise la ligne la plus longue. Aucune coupure de mot, aucun tiret."""
    mots = phrase.split(" ")
    n = len(mots)

    def largeur_de(i, j):                      # largeur de la ligne mots[i:j]
        return fnt.getlength(" ".join(mots[i:j]))

    # 1. nombre minimal de lignes (glouton)
    lignes, k, i = 1, 0, 0
    for j in range(1, n + 1):
        if largeur_de(i, j) > largeur and j - 1 > i:
            lignes += 1
            i = j - 1
    # 2. meilleure répartition à ce nombre de lignes : minimiser la ligne la plus longue
    INF = float("inf")
    best = {}                                  # (index, lignes restantes) -> (max, coupe)
    def solve(pos, reste):
        if reste == 1:
            w = largeur_de(pos, n)
            return (w, n) if w <= largeur else (INF, n)
        if (pos, reste) in best:
            return best[(pos, reste)]
        bm, bc = INF, n
        for j in range(pos + 1, n - reste + 2):
            w = largeur_de(pos, j)
            if w > largeur:
                break
            sub, _ = solve(j, reste - 1)
            m = max(w, sub)
            if m < bm:
                bm, bc = m, j
        best[(pos, reste)] = (bm, bc)
        return bm, bc

    out, pos, reste = [], 0, lignes
    while pos < n:
        _, j = solve(pos, reste)
        out.append(" ".join(mots[pos:j]))
        pos, reste = j, reste - 1
    return out


def mot_code(base, x, y, largeur, start=300, lo=90):
    """« R.O.U.G.E » : Anton monolithe, dégradé rouge clair → rouge foncé, ombre portée.

    Les points sont ceux de la police — ils font le « code » sans qu'on ajoute un ornement."""
    f, s = fit(CODE, largeur, start=start, lo=lo)
    largeurs = [f.getlength(c) for c in CODE]
    asc, desc = f.getmetrics()
    L = Image.new("L", (int(sum(largeurs)) + 60, asc + desc + 30), 0)
    dl = ImageDraw.Draw(L)
    xx = 12
    for c, cw in zip(CODE, largeurs):
        dl.text((xx, 14), c, font=f, fill=255)
        xx += cw - 2                     # resserré d'un cheveu : un bloc, pas cinq lettres
    grad = T.fill_gradient(L, ROUGE_CLAIR, ROUGE_FONCE)
    T.paste_left(base, T.drop(grad, 28, 160, (7, 12), (22, 0, 6)), x + 4, y + 12)
    T.paste_left(base, grad, x, y)
    bb = grad.getbbox()
    return s, bb[2] - bb[0], bb[3] - bb[1]


def bloc_titre(base, x, y, largeur, orateur=None, corps_accroche=0, corps_phrase=30):
    """Le bloc de gauche, dans l'ordre de lecture de la source :

        ICC PAHOU
        ▍ALERTE CODE
        R.O.U.G.E
        ──────
        les 5 clés pour vivre une chrétienne victorieuse
        (PRÉDICATEUR / AP Enock)

    Tout est mesuré avant d'être posé : aucun chevauchement, aucun débordement."""
    d = ImageDraw.Draw(base, "RGBA")

    # ---- marque
    fm = T.font(TEXTE, 18, "SemiBold")
    texte(base, MARQUE, fm, x, y, ACIER, tracking=7, ombre=False)
    d.line([(x, y + 36), (x + 32, y + 36)], fill=ROUGE + (245,), width=3)
    d.line([(x + 40, y + 36), (x + 152, y + 36)], fill=ACIER + (95,), width=1)
    y += 76

    # ---- accroche : le signal d'alerte, une barre rouge et deux mots blancs
    fa, sa = fit(ACCROCHE, largeur - 26, start=(corps_accroche or 76), lo=26)
    wa, ha = mesure(ACCROCHE, fa, 4)
    d.rectangle([x, y - 1, x + 7, y + ha + 1], fill=ROUGE + (250,))
    texte(base, ACCROCHE, fa, x + 22, y, BLANC, tracking=4)
    y += ha + 30

    # ---- le mot-code, monumental
    sc, wc, hc = mot_code(base, x - 8, y, largeur)
    y += hc

    # ---- filet d'accent, puis la phrase du thème
    yl = y + 20
    d.line([(x, yl), (x + min(196, wc), yl)], fill=ROUGE + (238,), width=4)
    y = yl + 24

    fp = T.font(TEXTE, corps_phrase, "SemiBold")
    choix = None
    for essai in CESURES:
        if all(fp.getlength(l) <= largeur for l in essai):
            choix = list(essai)
            break
    lignes = choix or retours(PHRASE, fp, largeur)
    for i, ligne in enumerate(lignes):
        texte(base, ligne, fp, x, y + i * round(corps_phrase * 1.24), BLANC, tracking=1)
    y += len(lignes) * round(corps_phrase * 1.24)

    # ---- l'orateur, en pied de colonne
    if orateur:
        yb = y + 26
        d.line([(x, yb), (x + 96, yb)], fill=ACIER + (120,), width=1)
        fl = T.font(TEXTE, 13, "SemiBold")
        texte(base, "PRÉDICATEUR", fl, x, yb + 14, ACIER, tracking=6, ombre=False, alpha=225)
        fn = T.font(TEXTE, 25, "SemiBold")
        texte(base, orateur, fn, x, yb + 38, BLANC, tracking=1)
        y = yb + 70
    return y


def vignettage(base):
    base.alpha_composite(T.vgrad(W, H, [(0.0, (0, 0, 0, 0)), (0.88, (0, 0, 0, 0)),
                                        (1.0, (2, 6, 18, 92))]))


# --------------------------------------------------------------------------- variantes
PHOTO = "orateurs/ap-enock-3458-detourage.png"   # _DSC3458 — pupitre, Bible et écran hors cadre
HAUTEUR_SUJET = 662


def poser_sujet(base, sub):
    """Le sujet est posé **entier**, ancré au bord bas : la photo `_DSC3458` s'arrête sur le
    costume, juste au-dessus de la barre du pupitre (détourage, `cutout_ap_3458.py`). Aucun
    fondu sur son bord, aucune coupe dans le corps."""
    x = W - 40 - sub.width
    y = H - sub.height
    sh = Image.new("RGBA", (sub.width + 200, sub.height + 120), (0, 0, 0, 0))
    sil = sub.split()[3].point(lambda v: int(v * 0.34))
    sh.paste(Image.new("RGBA", sub.size, (2, 6, 24, 255)), (100, 30), sil)
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(38)), (x - 100, y - 30))
    base.alpha_composite(sub, (x, y))
    return x


def rendu_ap(out, fond26=False):
    base = AP._reconstruire_26() if fond26 else AP.fond_bleu6()
    sub = AP.prepare_subject(PHOTO, HAUTEUR_SUJET)
    x_sujet = poser_sujet(base, sub)
    colonne = x_sujet - AP.MARGE - 30
    bloc_titre(base, AP.MARGE, 48, colonne, orateur=ORATEUR,
               corps_accroche=64, corps_phrase=31)
    vignettage(base)
    return base, sub, x_sujet


def rendu_theme(out):
    base = TH.fond_bleu("fonds/f06-bleu-acier-texture.jpg")
    bloc_titre(base, 56, 46, 604, corps_accroche=68, corps_phrase=33)

    # le motif du thème : la clé filaire, et les cinq clés comptées en pastilles
    kw, kh = 466, 192
    k = TH.cle(kw, kh, ep=13).rotate(-15, resample=Image.BICUBIC, expand=True)
    kx, ky = 1216 - k.width, 176
    glow = k.filter(ImageFilter.GaussianBlur(20))
    rgl = Image.new("RGBA", glow.size, ROUGE + (0,))
    rgl.putalpha(glow.getchannel("A").point(lambda v: int(v * 0.5)))
    base.alpha_composite(rgl, (kx - 8, ky - 8))
    base.alpha_composite(k, (kx, ky))

    d = ImageDraw.Draw(base, "RGBA")
    yc = ky + k.height + 52
    for i in range(5):
        cx = kx + 30 + i * 40
        d.ellipse([cx - 7, yc - 7, cx + 7, yc + 7], fill=ROUGE + (245,))
        d.ellipse([cx - 3, yc - 3, cx + 3, yc + 3], fill=BLANC + (200,))
    vignettage(base)
    return base


def rendu_visuel(out):
    """Le visuel des cinq clés : le bloc rectifié à gauche, l'acrostiche détaillé à droite."""
    base = TH.fond_bleu("fonds/f06-bleu-acier-texture.jpg")
    d = ImageDraw.Draw(base, "RGBA")

    bloc_titre(base, 58, 44, 400, corps_accroche=52, corps_phrase=25)

    # séparateur vertical entre les deux colonnes
    d.line([(492, 92), (492, 668)], fill=ACIER + (34,), width=1)

    X0, X1 = 536, 1224
    TOP, BOT = 96, 660
    pas = (BOT - TOP) / 5.0

    for i, (ch, verbe, glose, ref) in enumerate(CLE):
        y = TOP + i * pas
        d.line([(X0, y), (X1, y)], fill=ACIER + (60,), width=1)

        # lettre-clé, rouge, dégradée
        f = T.font(DISPLAY, 54)
        ml = T.text_mask(ch, f, 1)
        lay = T.fill_gradient(ml, ROUGE_CLAIR, ROUGE)
        T.paste_left(base, T.drop(lay, 14, 120, (3, 5), (4, 6)), X0 + 6, y + 20)
        T.paste_left(base, lay, X0 + 2, y + 16)

        fv = T.font(DISPLAY, 33)
        texte(base, verbe, fv, X0 + 66, y + 16, BLANC, tracking=2)
        fg = T.font(TEXTE, 22, "Regular")
        texte(base, glose, fg, X0 + 68, y + 62, ACIER, ombre=False)

        frf = T.font(TEXTE, 21, "SemiBold")
        mr = T.text_mask(ref, frf, 1)
        layr = Image.new("RGBA", mr.size, (236, 245, 255, 255))
        layr.putalpha(mr)
        T.paste_right(base, layr, X1, y + 34)

    d.line([(X0, BOT), (X1, BOT)], fill=ACIER + (110,), width=1)
    # légende de la figure : ce que la colonne de droite est, en trois mots
    fleg = T.font(TEXTE, 14, "Medium")
    texte(base, "ACROSTICHE  ·  CINQ CLÉS", fleg, 58, 640, ACIER, tracking=3,
          ombre=False, alpha=210)
    vignettage(base)
    return base


def main(variante, out):
    if variante == "theme":
        base = rendu_theme(out)
    elif variante in ("ap", "ap-fond26"):
        base, sub, x_panel = rendu_ap(out, fond26=(variante == "ap-fond26"))
        print(f"  sujet {sub.width}×{sub.height} à x={x_panel}")
    elif variante == "visuel":
        base = rendu_visuel(out)
    else:
        raise SystemExit("variante inconnue : theme | ap | ap-fond26 | visuel")
    base.convert("RGB").save(out, quality=94, subsampling=1, optimize=True)
    print("écrit", out, "· variante", variante)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
