#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Miniatures 1280×720 — « Les 5 clés… : ROUGE » **avec l'orateur AP**.

Deux variantes, même composition (texte à gauche, sujet à droite) :

* ``rouge``   — **FOND 6**, celui de la miniature du thème : la clé filaire cède sa place au
  prédicateur, l'accent rouge reste sur le mot-acrostiche. C'est la miniature du thème, avec AP.
* ``fond26``  — le **FOND 26** fourni avec la demande (diagonale bleu → magenta → rouge), indexé
  ``fonds/f27-bleu-magenta-rouge.jpg`` et **ramené au bleu** comme l'exige la palette : son axe et sa
  diagonale sont conservés, son magenta recalé en indigo, la diagonale rouge rallumée **par canaux**
  (un rouge translucide sur du bleu donnerait du magenta — la couleur à éviter).

Règle de silhouette (AGENT.md § 3.9, `specs/photos-sujet.md`) : la photo fournie est **coupée en
bas à la source**. Aucun rognage supplémentaire, aucun complément inventé : le sujet est **ancré
au bord bas** du gabarit, le bord coupé de la photo touchant le bord du visuel.

    python3 scripts/render_rouge_5cles_ap.py <detourage.png> <sortie.jpg> [rouge|fond26] [fond]

``detourage.png`` : PNG transparent de l'orateur (`orateurs/ap-enock-missimahou-podium-detourage.png`).
"""
import sys

import cv2
import numpy as np

from PIL import Image, ImageChops, ImageDraw, ImageFilter

sys.path.insert(0, "scripts")
import render_cap_f07_texte as T  # noqa: E402  (bibliothèque partagée du dépôt : font, cover, radial…)

W, H = 1280, 720
DISPLAY = T.TITRE                  # Anton
TEXTE = "polices/jost-var.ttf"     # Jost — duo du thème ROUGE

FOND6 = "fonds/f06-bleu-acier-texture.jpg"
FOND26 = "fonds/f27-bleu-magenta-rouge.jpg"

# 60 % — bleus mesurés sur f06 (fiche du thème ROUGE)
NUIT = (4, 34, 58)
BLEU = (4, 99, 152)
CYAN = (10, 176, 217)
# 30 % — secondaire
ACIER = (176, 214, 246)
BLANC = (242, 249, 255)
# 10 % — accent : le ROUGE du thème
ROUGE = (222, 38, 56)
ROUGE_CLAIR = (255, 106, 96)
ROUGE_FONCE = (168, 16, 40)

MARGE = 56                 # marge de sécurité 60 px (specs/formats.md § 1), arrondie au filet
PANEL_W = 566              # largeur du panneau du sujet
RIGHT = 36
BAS = 0                    # photo coupée en bas À LA SOURCE → le bord coupé touche le bord du visuel


# --------------------------------------------------------------------------- outils
def texte(base, s, fnt, x, y, couleur, tracking=0, ombre=True, alpha=255):
    m = T.text_mask(s, fnt, tracking)
    lay = Image.new("RGBA", m.size, tuple(couleur) + (alpha,))
    lay.putalpha(m)
    if ombre:
        T.paste_left(base, T.drop(lay, 10, 95, (3, 5), (2, 8, 14)), x + 2, y + 3)
    T.paste_left(base, lay, x, y)
    return m.width


def fit(text, target, start=200, lo=40):
    return T.fit_width(DISPLAY, text, target, start=start, lo=lo)


# --------------------------------------------------------------------------- fonds
def fond_bleu6():
    """FOND 6 : même traitement que la miniature du thème (assombri, scrim, halo cyan)."""
    bg = T.cover(Image.open(FOND6).convert("RGB"), W, H)
    bg = bg.filter(ImageFilter.GaussianBlur(1.2))
    bg = bg.filter(ImageFilter.UnsharpMask(radius=3, percent=70, threshold=2))
    base = Image.eval(bg, lambda v: min(255, int(v * 0.86))).convert("RGBA")
    base.alpha_composite(T.vgrad(W, H, [
        (0.00, (4, 16, 32, 196)),
        (0.30, (4, 20, 40, 124)),
        (0.66, (4, 16, 32, 118)),
        (1.00, (3, 10, 22, 226)),
    ]))
    base.alpha_composite(T.radial(W, H, W * 0.90, H * 0.14, W * 0.44, (20, 170, 215), 52, 90))
    base.alpha_composite(T.radial(W, H, W * 0.16, H * 0.90, W * 0.30, ROUGE, 34, 110))
    return base


def _reconstruire_26():
    """FOND 26 reconstruit dans la palette : on garde **son axe** (bleu en haut à gauche → rouge en
    bas à droite), sa diagonale de lumière et sa trame de points ; on remplace seulement ses teintes
    magenta/violet par un dégradé bleu nuit → cramoisi. Le fond fourni dicte la lumière, la palette
    du dépôt dicte les couleurs."""
    src = T.cover(Image.open(FOND26).convert("RGB"), W, H)
    src = src.filter(ImageFilter.GaussianBlur(6.0))   # les stries dures du fichier source sont fondues

    # 1. carte de lumière : la luminance du fond, débarrassée de sa couleur
    lum = np.asarray(src.convert("L")).astype(np.float32) / 255.0
    lum = lum ** 0.92                                    # un peu plus de matière dans les ombres
    lum = lum * 0.82 + 0.18                              # jamais un noir absolu

    # 2. dégradé diagonal : bleu nuit → indigo → cramoisi (l'axe du fond d'origine)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    t = np.clip((xx / W) * 0.62 + (yy / H) * 0.38, 0, 1)[..., None]
    stops = [(0.00, (5, 18, 46)),      # bleu nuit
             (0.32, (9, 30, 78)),      # indigo profond
             (0.58, (20, 26, 72)),     # indigo, très sombre
             (0.80, (78, 16, 44)),     # cramoisi sombre
             (1.00, (168, 16, 32))]    # rouge de la diagonale
    grad = np.zeros((H, W, 3), np.float32)
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        m = (t[..., 0] >= p0) & (t[..., 0] <= p1)
        k = np.clip((t[..., 0] - p0) / max(1e-6, p1 - p0), 0, 1)[..., None]
        seg = np.array(c0, np.float32) * (1 - k) + np.array(c1, np.float32) * k
        grad[m] = seg[m]

    # 3. la lumière du fond module le dégradé : la diagonale reste visible, en clair
    out = grad * (0.66 + 0.52 * lum[..., None])   # la trame du fond module, sans créer de bandes
    out = np.clip(out, 0, 255).astype(np.uint8)
    base = Image.fromarray(out, "RGB").convert("RGBA")
    # aucun coin ne tombe au noir : le fond reste lisible derrière le sujet
    base = Image.blend(base, Image.new("RGBA", (W, H), (10, 26, 56, 255)), 0.10)

    # 4. contraste d'ambiance : scrim, halo cyan en haut
    base.alpha_composite(T.vgrad(W, H, [
        (0.00, (4, 12, 38, 96)),
        (0.42, (5, 16, 44, 74)),
        (0.78, (4, 10, 30, 112)),
        (1.00, (2, 6, 20, 176)),
    ]))
    base.alpha_composite(T.radial(W, H, W * 0.58, -H * 0.06, W * 0.42, CYAN, 26, 120))

    # 5. la diagonale rouge — par **canaux**, jamais par superposition d'un rouge translucide :
    #    un rouge en transparence sur du bleu donne du magenta, exactement la couleur à éviter.
    #    Ici on baisse G et B sur la moitié droite : la teinte part vers le cramoisi, la lumière
    #    du fond d'origine est conservée.
    arr = np.asarray(base.convert("RGB")).astype(np.float32)
    gx = np.clip((np.arange(W, dtype=np.float32) / W - 0.46) / 0.54, 0, 1)[None, :]
    gy = np.clip((np.arange(H, dtype=np.float32) / H - 0.05) / 0.95, 0, 1)[:, None]
    m = (np.clip(gx * (0.55 + 0.45 * gy), 0, 1) ** 1.15)[:, :, None]
    arr *= np.concatenate([1 + 0.62 * m, 1 - 0.72 * m, 1 - 0.58 * m], axis=2)
    arr[:, :, 0] = np.minimum(255, arr[:, :, 0])
    base = Image.fromarray(arr.clip(0, 255).astype(np.uint8), "RGB").convert("RGBA")
    return base


# --------------------------------------------------------------------------- sujet
def decontaminer(im, passes=14):
    """Frange du détourage : les pixels de bord (0 < alpha < 255) portent encore la couleur de la
    pièce (bois de la porte). On propage vers eux la couleur de l'intérieur du sujet, sans jamais
    toucher au contour lui-même : l'alpha reste **strictement identique**, seule la couleur change."""
    arr = np.asarray(im).astype(np.float32)
    rgb, al = arr[:, :, :3], arr[:, :, 3] / 255.0
    connu = (al >= 0.985).astype(np.float32)
    front = ((al > 0) & (al < 0.985)).astype(np.float32)
    coul = rgb * connu[..., None]
    m = connu.copy()
    for _ in range(passes):
        cb = cv2.blur(coul, (5, 5))
        mb = cv2.blur(m, (5, 5))
        dispo = (mb > 1e-4) & (front > 0)
        if not dispo.any():
            break
        coul[dispo] = cb[dispo] / mb[dispo][:, None]
        m[dispo] = 1.0
        front[dispo] = 0.0
    reste = (al > 0) & (front > 0)
    coul[reste] = rgb[reste]                     # au pire : la couleur d'origine
    out = np.dstack([np.clip(coul, 0, 255), arr[:, :, 3]]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def prepare_subject(path, hauteur):
    """Recadrage **d'aucune zone du corps** : seulement l'échelle, la lumière et l'accord d'ambiance."""
    im = Image.open(path).convert("RGBA")
    im = decontaminer(im)
    bb = im.split()[3].getbbox()
    if bb:
        im = im.crop(bb)
    h = hauteur
    w = round(im.width * h / im.height)
    im = im.resize((w, h), Image.LANCZOS)

    rgb = im.convert("RGB")
    rgb = Image.eval(rgb, lambda v: min(255, int(255 * (v / 255) ** 0.92)))          # + lumière
    rgb = Image.eval(rgb, lambda v: min(255, max(0, int((v - 128) * 1.06 + 130))))   # + contraste
    wash = Image.eval(Image.new("RGB", rgb.size, ACIER), lambda v: int(v * 0.5))
    rgb = Image.blend(rgb, ImageChops.screen(rgb, wash), 0.16)                        # accord, pas virage
    out = rgb.convert("RGBA")
    out.putalpha(im.split()[3])
    return out


def place_subject(base, sub):
    """Le sujet est posé tel quel : **aucun fondu sur son bord** — un dégradé de raccord rognerait
    l'avant-bras qui touche le bord gauche du panneau. Le contour vient du détourage, pas du fond."""
    panel = Image.new("RGBA", (PANEL_W, H), (0, 0, 0, 0))
    panel.alpha_composite(sub, (PANEL_W - sub.width, H - BAS - sub.height))

    # ombre portée douce : le sujet se détache du fond sans halo
    sh = Image.new("RGBA", (PANEL_W + 160, H + 80), (0, 0, 0, 0))
    sil = panel.split()[3].point(lambda v: int(v * 0.34))
    sh.paste(Image.new("RGBA", panel.size, (2, 6, 24, 255)), (86, 16), sil)
    x0 = W - PANEL_W - RIGHT
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(34)), (x0 - 80, -14))
    base.alpha_composite(panel, (x0, 0))
    return x0


# --------------------------------------------------------------------------- mise en page
def composition(base, x_panel):
    d = ImageDraw.Draw(base, "RGBA")
    colonne = W - PANEL_W - RIGHT - MARGE - 40        # largeur disponible pour le texte

    # ---- marque
    fm = T.font(TEXTE, 18, "SemiBold")
    texte(base, "ICC PAHOU", fm, MARGE, 48, ACIER, tracking=7, ombre=False)
    d.line([(MARGE, 84), (MARGE + 32, 84)], fill=ROUGE + (245,), width=3)
    d.line([(MARGE + 40, 84), (MARGE + 152, 84)], fill=ACIER + (95,), width=1)

    # ---- accroche
    yk = 128
    fk, sk = fit("LES 5 CLÉS", min(392, colonne), start=80)
    texte(base, "LES 5 CLÉS", fk, MARGE - 4, yk, BLANC, tracking=3)

    # ---- mot-acrostiche : le ROUGE, dégradé clair → foncé
    fr, sr = fit("ROUGE", min(452, colonne), start=280, lo=120)
    yR = yk + int(sk * 1.12) + 16
    largeur = [fr.getlength(c) for c in "ROUGE"]
    asc, desc = fr.getmetrics()
    L = Image.new("L", (int(sum(largeur)) + 40, asc + desc + 24), 0)
    dl = ImageDraw.Draw(L)
    xx = 8
    for c, cw in zip("ROUGE", largeur):
        dl.text((xx, 10), c, font=fr, fill=255)
        xx += cw - 1
    grad = T.fill_gradient(L, ROUGE_CLAIR, ROUGE_FONCE)
    T.paste_left(base, T.drop(grad, 28, 155, (6, 11), (24, 0, 6)), MARGE - 10, yR + 10)
    T.paste_left(base, grad, MARGE - 18, yR)
    hR = grad.getbbox()[3] - grad.getbbox()[1]

    # filet d'accent sous le mot-acrostiche
    yl = yR + hR + 12
    d.line([(MARGE, yl), (MARGE + 196, yl)], fill=ROUGE + (238,), width=4)

    # ---- phrase du thème
    ys = yl + 24
    fs = T.font(TEXTE, 33, "SemiBold")
    texte(base, "pour vivre une vie", fs, MARGE, ys, BLANC, tracking=1)
    texte(base, "chrétienne victorieuse", fs, MARGE, ys + 42, BLANC, tracking=1)

    # ---- l'orateur, en bas de la colonne de gauche
    yb = ys + 42 + 62
    d.line([(MARGE, yb), (MARGE + 96, yb)], fill=ACIER + (120,), width=1)
    fl = T.font(TEXTE, 13, "SemiBold")
    texte(base, "PRÉDICATEUR", fl, MARGE, yb + 14, ACIER, tracking=6, ombre=False, alpha=225)
    fn = T.font(TEXTE, 25, "SemiBold")
    texte(base, "AP Enock MISSIMAHOU", fn, MARGE, yb + 38, BLANC, tracking=1)

    # ---- vignettage bas : les deux bords bas restent lisibles sur mobile
    base.alpha_composite(T.vgrad(W, H, [(0.0, (0, 0, 0, 0)), (0.86, (0, 0, 0, 0)),
                                        (1.0, (2, 6, 18, 96))]))
    return sr


def main(photo, out, variante="rouge", fond=None):
    if variante == "fond26":
        base = _reconstruire_26()
        hauteur = 690
    else:
        base = fond_bleu6()
        hauteur = 690

    sub = prepare_subject(photo, hauteur)
    x_panel = place_subject(base, sub)
    sr = composition(base, x_panel)
    base.convert("RGB").save(out, quality=94, subsampling=1, optimize=True)
    print(f"écrit {out} · variante {variante} · ROUGE {sr} px · sujet {sub.width}×{sub.height} à x={x_panel}")


if __name__ == "__main__":
    v = sys.argv[3] if len(sys.argv) > 3 else "rouge"
    f = sys.argv[4] if len(sys.argv) > 4 else None
    main(sys.argv[1], sys.argv[2], v, f)
