#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Affiche « Camp des Femmes Afrique de l'Ouest 2026 — Seigneur, j'ai soif ! » en PAYSAGE.

Reprise **en paysage** du visuel portrait fourni par le client : mêmes textes, même hiérarchie,
même ambiance (bleu pétrole + cyan clair), recomposée pour le 16:9. Rien n'est inventé : le
verset, les noms, les rôles, les dates et l'adresse sont recopiés à la lettre.

Trois partis pris imposés par le passage au paysage :
1. accroche, titre, verset et noms tiennent la colonne de gauche ;
2. les deux intervenantes, détourées du visuel fourni, occupent la moitié droite, en pied de
   cadre ;
3. le bandeau date + lieu court sur toute la largeur et passe **devant** les silhouettes,
   exactement comme sur l'original.

    python3 scripts/render_camp_femmes_2026.py <sortie.jpg> [paysage|a5-paysage]
"""
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

sys.path.insert(0, "scripts")
import render_cap_f07_texte as T  # noqa: E402  (bibliothèque partagée du dépôt)

SIZES = {
    "paysage": (1920, 1080),      # 16:9 — référence écran, demandée en premier
    "a5-paysage": (2480, 1748),   # A5 paysage 300 dpi — impression
}

DISPLAY = "polices/montserrat-var.ttf"   # titraille : géométrique très grasse, comme l'original
TEXTE = "polices/jost-var.ttf"           # texte : géométrique, lisible en petit
ASSETS = "themes/assets-camp-femmes/"
DUO = ASSETS + "duo-habi-nadine.png"
LOGO_FI = ASSETS + "logo-femmes-impact.png"
LOGO_CF = ASSETS + "logo-camp-des-femmes.png"

# 60 % — bleu pétrole relevé sur le visuel fourni
NUIT = (1, 20, 30)
PETROLE = (1, 48, 63)
LAGON = (42, 109, 125)
# 30 % — secondaire
CYAN = (115, 220, 241)
BLANC = (235, 253, 254)
# 10 % — accent
CYAN_PALE = (188, 240, 250)

VERSET_A = [("“ La femme lui dit : Seigneur, ", "Regular"),
            ("donne-moi cette eau", "SemiBold"),
            (", afin que", "Regular")]
VERSET_B = [("je n'aie plus soif", "SemiBold"),
            (", et que je ne vienne plus puiser ici. ” ", "Regular"),
            ("Jean 4 : 15", "SemiBold")]

PERS = [("HABI", "CASTANOU", ["PASTEUR ASSOCIÉ - IMPACT", "CENTRE CHRÉTIEN"]),
        ("NADINE", "NGBANDA", ["PASTEUR IMPACT CENTRE", "CHRÉTIEN - BÉNIN"])]

DATE_1, DATE_AU, DATE_2 = "18", "au", "21 NOV. 2026"
LIEU = "ICC COTONOU - CENTRE SION"
ADRESSE = ["Route des Pêches - Axe Fidjrossè, fin pavés",
           "Togbin rue pavée station JNP à droite - 1ère rue",
           "à gauche"]
MENTION = "*OUVERT A TOUTES LES FEMMES"
CREDIT = "IMPACT CENTRE CHRÉTIEN BÉNIN"


# --------------------------------------------------------------------------- outils
def diag_band(w, h, cx, cy, angle, length, width, color, peak):
    """Bande lumineuse diagonale floutée : la lumière rase du visuel d'origine."""
    big = int(max(w, h) * 1.6)
    lay = Image.new("L", (big, big), 0)
    ImageDraw.Draw(lay).line(
        [(big // 2 - length // 2, big // 2), (big // 2 + length // 2, big // 2)],
        fill=peak, width=width)
    lay = lay.rotate(angle, resample=Image.BICUBIC, center=(big // 2, big // 2))
    lay = lay.filter(ImageFilter.GaussianBlur(width * 0.55))
    lay = lay.crop((big // 2 - cx, big // 2 - cy,
                    big // 2 - cx + w, big // 2 - cy + h))
    out = Image.new("RGBA", (w, h), tuple(color) + (0,))
    out.putalpha(lay)
    return out


def fond(w, h):
    base = Image.new("RGB", (w, h), NUIT).convert("RGBA")
    base.alpha_composite(T.vgrad(w, h, [
        (0.00, (2, 16, 24, 255)),
        (0.26, (2, 34, 46, 255)),
        (0.60, (1, 26, 36, 255)),
        (1.00, (1, 12, 19, 255)),
    ]))
    base.alpha_composite(T.radial(w, h, w * 0.44, h * 0.20, w * 0.44, (46, 132, 150), 118, 130))
    base.alpha_composite(T.radial(w, h, w * 0.72, h * 0.55, w * 0.30, (26, 96, 116), 74, 120))
    base.alpha_composite(diag_band(w, h, w * 0.28, h * 0.30, -26, int(w * 0.95),
                                   int(h * 0.22), (90, 200, 220), 42))
    base.alpha_composite(T.vgrad(w, h, [
        (0.00, (1, 12, 20, 0)),
        (0.58, (1, 12, 20, 0)),
        (1.00, (1, 10, 16, 120)),
    ]))
    return base


def txt(base, s, font, x, y, color, tracking=0, ombre=False, droite=None, alpha=255):
    m = T.text_mask(s, font, tracking)
    lay = Image.new("RGBA", m.size, tuple(color) + (alpha,))
    lay.putalpha(m)
    if ombre:
        sh = T.drop(lay, 12, 115, (4, 6), (0, 8, 12))
        if droite is None:
            T.paste_left(base, sh, x + 2, y + 2)
        else:
            T.paste_right(base, sh, droite + 2, y + 2)
    if droite is None:
        T.paste_left(base, lay, x, y)
    else:
        T.paste_right(base, lay, droite, y)
    return m.width


def logo(base, path, w, x, y, droite=False):
    """Logo : masque de transparence blanc, posé sur le fond (pas de cartouche)."""
    lg = Image.open(path).convert("RGBA")
    lg = lg.resize((max(1, int(w)), max(1, int(lg.height * w / lg.width))), Image.LANCZOS)
    lg.putalpha(lg.getchannel("A").filter(ImageFilter.GaussianBlur(0.7)))
    white = Image.new("RGBA", lg.size, (255, 255, 255, 0))
    white.putalpha(lg.getchannel("A"))
    xx = x - lg.width if droite else x
    base.alpha_composite(white, (xx, y))
    return lg.width, lg.height


def drapeau(base, cx, cy, r):
    """Pastille drapeau du Bénin (vert / jaune / rouge), comme sur l'original."""
    S = 4 * r
    flag = Image.new("RGB", (S, S), (0, 0, 0))
    d = ImageDraw.Draw(flag)
    w3, h2 = S // 3, S
    d.rectangle([0, 0, w3, h2], fill=(0, 154, 68))
    d.rectangle([w3, 0, 2 * w3, h2 // 2], fill=(252, 209, 22))
    d.rectangle([2 * w3, 0, S, h2 // 2], fill=(232, 17, 45))
    d.rectangle([w3, h2 // 2, 2 * w3, h2], fill=(252, 209, 22))
    d.rectangle([2 * w3, h2 // 2, S, h2], fill=(232, 17, 45))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, S - 1, S - 1], fill=255)
    flag = flag.resize((2 * r, 2 * r), Image.LANCZOS)
    mask = mask.resize((2 * r, 2 * r), Image.LANCZOS)
    base.paste(flag, (cx - r, cy - r), mask)


def pin(base, x, y, s):
    """Pictogramme du lieu : carte pliée + repère, comme sur l'original."""
    lay = Image.new("RGBA", (int(s * 1.5), int(s * 1.6)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    W2, H2 = s, s * 0.84
    ox, oy = s * 0.12, s * 0.52
    pts = [(ox, oy + H2 * 0.16), (ox + W2 * 0.34, oy), (ox + W2 * 0.66, oy + H2 * 0.16),
           (ox + W2, oy), (ox + W2, oy + H2 * 0.84), (ox + W2 * 0.66, oy + H2),
           (ox + W2 * 0.34, oy + H2 * 0.84), (ox, oy + H2)]
    d.polygon(pts, fill=BLANC + (255,))
    for k, k2 in ((0.34, 0.0), (0.66, 0.16)):
        d.line([(ox + W2 * k, oy + H2 * k2), (ox + W2 * k, oy + H2 * (k2 + 0.84))],
               fill=(1, 74, 100, 230), width=max(2, int(s * 0.05)))
    cx, cy, rr = ox + W2 * 0.5, oy + H2 * 0.26, s * 0.18
    d.ellipse([cx - rr, cy - rr * 1.15, cx + rr, cy + rr * 0.85], fill=BLANC + (255,))
    d.polygon([(cx - rr * 0.70, cy + rr * 0.42), (cx + rr * 0.70, cy + rr * 0.42),
               (cx, cy + rr * 1.85)], fill=BLANC + (255,))
    d.ellipse([cx - rr * 0.34, cy - rr * 0.70, cx + rr * 0.34, cy + rr * 0.02],
              fill=(1, 74, 100, 255))
    base.alpha_composite(lay, (int(x), int(y)))


# --------------------------------------------------------------------------- rendu
def main(out, size="paysage"):
    W, H = SIZES[size]
    S = W / 1920.0
    px = lambda v: int(round(v * S))  # noqa: E731
    base = fond(W, H)
    d = ImageDraw.Draw(base, "RGBA")

    ML = px(88)
    MR = W - px(88)
    XL = px(940)                       # limite de la colonne de gauche

    # ---------------- logos
    logo(base, LOGO_CF, px(228), MR, px(42), droite=True)
    logo(base, LOGO_FI, px(212), ML, px(54))
    fcred = T.font(TEXTE, px(13), "Medium")
    txt(base, CREDIT, fcred, ML, px(112), CYAN_PALE, tracking=px(4), alpha=190)

    # ---------------- accroche : CAMP DES / FEMMES / AFRIQUE DE L'OUEST 2026
    fcamp, s_camp = T.fit_width(DISPLAY, "AFRIQUE", px(430), start=px(62), lo=px(34))
    try:
        fcamp.set_variation_by_name("Black")
    except Exception:
        pass
    y = px(150)
    wcamp = txt(base, "CAMP", fcamp, ML, y, BLANC, tracking=px(1), ombre=True)
    fdes = T.font(TEXTE, px(16), "Bold")
    chip = int(fdes.getlength("DES") + px(14))
    cxb = ML + wcamp + px(14)
    d.rectangle([cxb, y + px(8), cxb + chip, y + px(40)], fill=(1, 118, 154, 255))
    txt(base, "DES", fdes, cxb + px(7), y + px(12), BLANC, tracking=px(2))

    y += px(58)
    txt(base, "FEMMES", fcamp, ML, y, CYAN, tracking=px(1), ombre=True)

    y += px(58)
    txt(base, "AFRIQUE", fcamp, ML, y, BLANC, tracking=px(1), ombre=True)
    fde = T.font(TEXTE, px(16), "Bold")
    wde = fde.getlength("DE")
    xde = ML + fcamp.getlength("AFRIQUE") + px(22)
    txt(base, "DE", fde, xde, y + px(22), CYAN, tracking=px(2))
    xou = xde + wde + px(24)
    wou = txt(base, "L'OUEST", fcamp, xou, y, CYAN, tracking=px(1), ombre=True)

    # pastille « 2026 », collée au mot L'OUEST comme sur le visuel d'origine
    f26 = T.font(DISPLAY, px(18), "Black")
    w26 = int(f26.getlength("2026") + px(16))
    y26 = y + int(s_camp * 0.96)
    d.rectangle([xou + wou - w26, y26, xou + wou, y26 + px(27)],
                fill=(1, 58, 76, 245))
    txt(base, "2026", f26, xou + wou - w26 + px(8), y26 + px(4), BLANC, tracking=px(1))

    # ---------------- titre
    yt = y + px(96)
    ft1, s1 = T.fit_width(DISPLAY, "SEIGNEUR,", px(430), start=px(72), lo=px(40))
    try:
        ft1.set_variation_by_name("Black")
    except Exception:
        pass
    txt(base, "SEIGNEUR,", ft1, ML, yt, CYAN, tracking=px(1), ombre=True)

    yt2 = yt + px(78)
    ft2, s2 = T.fit_width(DISPLAY, "J'AI SOIF", px(760), start=px(180), lo=px(90))
    try:
        ft2.set_variation_by_name("Black")
    except Exception:
        pass
    w2 = txt(base, "J'AI SOIF", ft2, ML, yt2, BLANC, tracking=px(1), ombre=True)
    txt(base, "!", ft2, ML + w2 + px(4), yt2 + px(2), CYAN, tracking=0, ombre=True)
    h2 = ft2.size

    # ---------------- verset
    yv = yt2 + h2 + px(24)
    fv = T.font(TEXTE, px(21), "Regular")
    fvb = T.font(TEXTE, px(21), "SemiBold")
    for line, yy in ((VERSET_A, yv), (VERSET_B, yv + px(29))):
        x = ML
        for s, var in line:
            f = fv if var == "Regular" else fvb
            x += txt(base, s, f, x, yy, BLANC, tracking=0, alpha=245) - px(3)

    # ---------------- les deux intervenantes
    yn = yv + px(88)
    colw = px(408)
    for i, (prenom, nom, roles) in enumerate(PERS):
        xp = ML + i * colw
        fn, s_n = T.fit_width(DISPLAY, nom, colw - px(40), start=px(32), lo=px(18))
        try:
            fn.set_variation_by_name("Black")
        except Exception:
            pass
        txt(base, prenom, fn, xp, yn, CYAN, tracking=px(1), ombre=True)
        txt(base, nom, fn, xp, yn + px(30), CYAN, tracking=px(1), ombre=True)
        fr = T.font(TEXTE, px(13), "SemiBold")
        for k, r in enumerate(roles):
            txt(base, r, fr, xp, yn + px(66) + k * px(16), BLANC, alpha=230)
        drapeau(base, xp + px(11), yn + px(112), px(10))

    # ---------------- le duo, à droite, en pied de cadre
    grp = Image.open(DUO).convert("RGBA")
    gh = H - px(196)
    # le duo ne dépasse jamais 47 % de la largeur : en A5 paysage (plus étroit en proportion)
    # il rognerait sinon le titre, qui doit rester entier.
    gh = min(gh, int(0.47 * W * grp.height / grp.width))
    gw = int(grp.width * gh / grp.height)
    grp = grp.resize((gw, gh), Image.LANCZOS)
    grp = grp.filter(ImageFilter.UnsharpMask(radius=2, percent=55, threshold=2))
    gx = W - gw - px(8)
    # halo derrière les épaules : détache les costumes bleu nuit du fond
    base.alpha_composite(T.radial(W, H, gx + gw * 0.42, H * 0.50, W * 0.30, (66, 158, 180), 46, 120))
    base.alpha_composite(grp, (gx, H - gh))

    # ---------------- bandeau date + lieu
    BH = px(112)
    BY = H - px(58) - BH
    BX0, BX1 = ML, MR
    MID = BX0 + int((BX1 - BX0) * 0.655)
    d.rectangle([BX0, BY, MID, BY + BH], fill=BLANC + (255,))
    d.rectangle([MID, BY, BX1, BY + BH], fill=(1, 110, 146, 255))

    fdate, s_date = T.fit_width(DISPLAY, "18  au  21 NOV. 2026", px(760), start=px(64), lo=px(30))
    try:
        fdate.set_variation_by_name("Black")
    except Exception:
        pass
    yb = BY + int(BH * 0.5) - int(s_date * 0.68)
    wd = txt(base, DATE_1, fdate, BX0 + px(34), yb, (1, 28, 48), tracking=px(-1))
    cxp = BX0 + px(34) + wd + px(12)
    rr = px(15)
    d.ellipse([cxp, yb + int(s_date * 0.42), cxp + 2 * rr, yb + int(s_date * 0.42) + 2 * rr],
              fill=(1, 118, 154, 255))
    fau = T.font(TEXTE, px(11), "Bold")
    txt(base, DATE_AU, fau, cxp + px(5), yb + int(s_date * 0.50), BLANC, tracking=px(1))
    txt(base, DATE_2, fdate, cxp + 2 * rr + px(12), yb, (1, 28, 48), tracking=px(-1))

    pin(base, MID + px(26), BY + px(18), px(50))
    fl = T.font(DISPLAY, px(21), "ExtraBold")
    txt(base, LIEU, fl, MID + px(102), BY + px(16), BLANC, tracking=px(1))
    fa = T.font(TEXTE, px(14), "Medium")
    for k, a in enumerate(ADRESSE):
        txt(base, a, fa, MID + px(102), BY + px(48) + k * px(18), BLANC, alpha=240)

    # ---------------- mention, sous le bandeau, à gauche (zone sombre, hors du duo)
    fm = T.font(TEXTE, px(13), "SemiBold")
    txt(base, MENTION, fm, ML + px(2), BY + BH + px(14), CYAN_PALE, tracking=px(6), alpha=235)

    base.convert("RGB").save(out, quality=94, subsampling=1, optimize=True)
    print("écrit", out, W, "×", H, "· accroche", s_camp, "· titre", s1, s2)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "paysage")
