#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Miniature YouTube 1280×720 — thème « Atmosphère de prière », orateur Enock MISSIMAHOU.

Structure empruntée au **modèle m01** (`modeles/m01-bleu-nuit-titre-coupe.jpg`) : titre en fer à
gauche sur trois lignes alternées, portrait détouré à droite, typographie fantôme derrière,
bande basse pour le nom. Aucune couleur du modèle n'est reprise : la palette est reconstruite.

Palette (60 / 30 / 10)
  60 %  bleus mesurés sur FOND 7 (f07) : #0A398F · #0D56B1 · #0B3AC8
  30 %  secondaire = couleur de la chemise de l'orateur, échantillonnée sur la photo
        (bleu ardoise à carreaux, médiane #4A6691 → déclinée en #7C9AC4 / #2E4A6E)
  10 %  accent = or pâle #E9CE93 (lumière de veilleuse, cohérent avec l'ambiance de prière)

Le prédicateur est **déjà coupé** dans la photo d'origine (buste coupé en bas, pouce droit contre le
bord, main levée sortante). Conformément à la règle 9 : photo gardée telle quelle, **ancrée sur les
bords du cadre** (bord droit de la photo = bord droit du visuel, bas de la photo = bas du visuel),
et signalée en « À vérifier ». Aucune IA générative, aucun étirement : le détourage fourni est
utilisé tel quel, seul un très léger réglage de lumière sépare la silhouette du fond.

    python3 scripts/render_priere_m01_ap.py livrables/<AAAA-MM-JJ>-miniature-atmosphere-de-priere.jpg
"""
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, "scripts")
import render_cap_f07_texte as T  # noqa: E402  (bibliothèque partagée du dépôt)

W, H = 1280, 720
TITRE = "polices/anton-regular.ttf"       # Anton — duo du thème
TEXTE = "polices/jost-var.ttf"            # Jost — duo du thème
FOND = "fonds/f07-bleu-nuit-bokeh.jpg"    # FOND 7
PORTRAIT = "orateurs/ap-enock-missimahou-detourage.png"

# 60 % — bleus mesurés sur f07
NUIT = (7, 26, 78)
BLEU = (13, 86, 177)
CYAN = (13, 137, 210)
# 30 % — secondaire : la chemise de l'orateur (bleu ardoise)
ARDOISE = (46, 74, 110)
ARDOISE_CLAIR = (124, 154, 196)
# 10 % — accent
OR = (233, 206, 147)
# neutres
BLANC = (242, 248, 255)
ACIER = (176, 214, 246)

ORATEUR = "Enock MISSIMAHOU"
MARQUE = "ICC PAHOU"

# portrait : échelle et ancrage (bord droit de la photo = bord droit du visuel)
PORTRAIT_SCALE = 0.505
PORTRAIT_RIGHT = W
PORTRAIT_BOTTOM = H


def fond_bleu(path):
    bg = T.cover(Image.open(path).convert("RGB"), W, H)
    bg = bg.filter(ImageFilter.GaussianBlur(3.2))
    bg = Image.eval(bg, lambda v: min(255, int(v * 0.82)))
    base = bg.convert("RGBA")
    # voile : haut dense (lisibilité du titre), bas dense (bande nom), respiration au centre droit
    base.alpha_composite(T.vgrad(W, H, [
        (0.00, (5, 18, 44, 208)),
        (0.34, (6, 24, 62, 132)),
        (0.58, (6, 22, 56, 118)),
        (0.78, (4, 14, 34, 186)),
        (1.00, (3, 10, 24, 236)),
    ]))
    # halo derrière le portrait : sépare la silhouette du fond sans la découper
    base.alpha_composite(T.radial(W, H, W * 0.80, H * 0.44, W * 0.34, CYAN, 46, 110))
    base.alpha_composite(T.radial(W, H, W * 0.10, H * 0.10, W * 0.30, BLEU, 40, 120))
    return base


def typo_fantome(base, texte, taille, x, y, couleur, alpha, largeur_max=None):
    """Typographie « fantôme » du modèle m01 : profondeur, jamais concurrence.

    Le mot est coupé avant le portrait (`largeur_max`) : une lettre qui dépasse sous la
    silhouette créerait un bord vertical visible.
    """
    m = T.text_mask(texte, T.font(TITRE, taille))
    lay = Image.new("RGBA", m.size, tuple(couleur) + (alpha,))
    lay.putalpha(m)
    bb = lay.getbbox()
    if largeur_max is not None:
        limite = max(0, largeur_max - x + bb[0])
        lay = lay.crop((0, 0, min(lay.width, limite), lay.height))
        # fondu progressif sur les 90 derniers pixels : aucune arête verticale visible
        fondu = Image.new("L", (lay.width, 1), 255)
        fd = ImageDraw.Draw(fondu)
        for i in range(90):
            xx = lay.width - 90 + i
            if 0 <= xx < lay.width:
                fd.point((xx, 0), int(255 * (1 - i / 90)))
        alpha = lay.split()[-1]
        alpha = Image.composite(alpha, Image.new("L", lay.size, 0), fondu.resize(lay.size))
        lay.putalpha(alpha)
    T.paste_left(base, lay, x, y)
    return lay


def ligne(base, s, path, taille, x, y, couleur, tracking=0, ombre=True, alpha=255):
    m = T.text_mask(s, T.font(path, taille), tracking)
    lay = Image.new("RGBA", m.size, tuple(couleur) + (alpha,))
    lay.putalpha(m)
    if ombre:
        sh = T.drop(lay, 14, 110, (4, 6), (2, 6, 16))
        T.paste_left(base, sh, x + 2, y + 3)
    T.paste_left(base, lay, x, y)
    return m


def nettoyer_contour(im):
    """Nettoie le contour du détourage fourni : garde l'anticrénelage, supprime le voile résiduel.

    Aucune génération, aucun lissage du sujet : on ne travaille que sur le canal alpha.
    """
    a = im.split()[-1]
    net = a.filter(ImageFilter.MedianFilter(3))
    net = net.filter(ImageFilter.GaussianBlur(0.6))
    out = im.copy()
    out.putalpha(net)
    return out


def halftone(base, pas=13, alpha=26, zone=(0.0, 0.30, 0.62, 0.92)):
    """Trame de points (m01) : texture, jamais un motif qui se lit."""
    w, h = base.size
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    x0, y0, x1, y1 = [int(v * (w if i % 2 == 0 else h)) for i, v in enumerate(zone)]
    for yy in range(y0, y1, pas):
        for xx in range(x0, x1, pas):
            r = 1.6
            d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=alpha)
    m = m.filter(ImageFilter.GaussianBlur(1.1))
    lay = Image.new("RGBA", (w, h), ACIER + (0,))
    lay.putalpha(m)
    base.alpha_composite(lay)
    return base


def grain(base, force=7):
    import random
    random.seed(7)
    px = base.load()
    w, h = base.size
    for y in range(0, h, 1):
        for x in range(0, w, 2):
            n = random.randint(-force, force)
            r, g, b, al = px[x, y]
            px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)),
                        max(0, min(255, b + n)), al)
    return base


def vignettage(base, force=120):
    w, h = base.size
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    d.ellipse([-w * 0.22, -h * 0.30, w * 1.22, h * 1.30], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(90)).point(lambda v: int(force * (1 - v / 255)))
    lay = Image.new("RGBA", (w, h), (2, 6, 16, 0))
    lay.putalpha(m)
    base.alpha_composite(lay)
    return base


def portrait(base):
    im = Image.open(PORTRAIT).convert("RGBA")
    im = nettoyer_contour(im)
    sw, sh = im.size
    nw, nh = round(sw * PORTRAIT_SCALE), round(sh * PORTRAIT_SCALE)
    im = im.resize((nw, nh), Image.LANCZOS)
    # léger réchauffement/froid de lumière : on ne touche ni au visage, ni à la tenue
    im = Image.eval(im, lambda v: v)
    x = PORTRAIT_RIGHT - nw
    y = PORTRAIT_BOTTOM - nh
    # ombre portée douce : profondeur, pas de liseré
    ombre = Image.new("RGBA", (nw + 200, nh + 200), (0, 0, 0, 0))
    m = im.split()[-1]
    teinte = Image.new("RGBA", im.size, (2, 8, 20, 150))
    ombre.paste(teinte, (100 + 16, 100 + 10), m)
    ombre = ombre.filter(ImageFilter.GaussianBlur(26))
    base.alpha_composite(ombre, (x - 100, y - 100))
    base.alpha_composite(im, (x, y))
    return (x, y, nw, nh)


def main(out, fond=FOND):
    base = fond_bleu(fond)

    # trame de points du modèle m01 (texture, pas de mot fantôme : il doublonnait le titre)
    halftone(base)

    d = ImageDraw.Draw(base)

    # sur-titre : filet + marque
    d.rectangle([88, 82, 88 + 64, 82 + 3], fill=OR + (235,))
    ligne(base, MARQUE, TEXTE, 23, 88, 98, OR, tracking=7, ombre=False)

    # titre en fer à gauche : trois lignes, interligne serré (m01)
    _, s1 = T.fit_width(TITRE, "Atmosphère", 600, start=150)
    s2 = round(s1 * 0.60)
    _, s3 = T.fit_width(TITRE, "prière", 610, start=230)

    def vis_h(texte, taille):
        bb = T.text_mask(texte, T.font(TITRE, taille)).getbbox()
        return bb[3] - bb[1]

    h1, h2, h3 = vis_h("Atmosphère", s1), vis_h("de", s2), vis_h("prière", s3)
    y1 = 142
    y2 = y1 + round(h1 * 0.94)
    y3 = y2 + h2 - 4
    ligne(base, "Atmosphère", TITRE, s1, 84, y1, BLANC)
    ligne(base, "de", TITRE, s2, 92, y2, ACIER, alpha=248)
    ligne(base, "prière", TITRE, s3, 82, y3, BLANC)
    bas_titre = y3 + h3

    # bande basse : filet accent + nom (m01, hiérarchie 2) — marge basse ≥ 60 px
    h_nom = vis_h(ORATEUR, 54)
    y_nom = 708 - 60 - h_nom
    # accent : barre verticale or devant le nom (repère d'identité, jamais un soulignement du titre)
    d.rectangle([70, y_nom - 4, 70 + 7, y_nom + h_nom + 4], fill=OR + (225,))
    ligne(base, ORATEUR, TITRE, 54, 92, y_nom, BLANC, tracking=1)
    bas_nom = y_nom + h_nom

    px, py, pw, ph = portrait(base)

    # fondu bas du portrait dans la bande (m01) : évite la coupure nette du buste
    base.alpha_composite(T.vgrad(W, H, [
        (0.00, (0, 0, 0, 0)),
        (0.84, (0, 0, 0, 0)),
        (0.92, (3, 10, 24, 80)),
        (1.00, (3, 10, 24, 156)),
    ]))

    vignettage(base, 110)
    grain(base, 6)

    base.convert("RGB").save(out, quality=94, subsampling=0)
    print("écrit :", out, f"{W}×{H}")
    print(f"portrait : {pw}×{ph} en ({px},{py}) — ancré à droite et en bas")
    print(f"titre : {s1}/{s2}/{s3} px · bas du titre y={bas_titre} · bas du nom y={bas_nom}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/priere.jpg",
         sys.argv[2] if len(sys.argv) > 2 else FOND)
