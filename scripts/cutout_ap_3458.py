#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Détourage de `_DSC3458` — AP Enock au micro, plan large avec pupitre, écran et bannière.

La photo n'est pas un plan poitrine : le prédicateur est debout **derrière un pupitre** (barre
laquée, Bible ouverte), devant un écran qui rediffuse une image de lui et une bannière bleue.
Deux exigences : **« le pupitre ne doit pas sortir »** et la silhouette entière (AGENT.md § 5ter)
— tête, deux bras, deux mains, cinq doigts, micro compris.

Aucun modèle génératif : segmentation classique, vérifiée au zoom.

1. **Couleur** — trois familles mesurées sur le fichier : peau chaude (H ≤ 26 | H ≥ 163, S ≥ 70),
   tunique marine (H 92-132, S ≥ 95, **V ≤ 145** : c'est ce plafond de valeur qui sépare la tenue
   de la bannière, de même teinte mais bien plus claire), et cheveux/barbe/monture (V < 105,
   seulement dans la fenêtre de la tête — ailleurs, ce seuil attraperait les câbles et le pupitre).
2. **Micro** — polygone mesuré, forcé : capsule, cylindre et bague bleue restent entiers.
3. **Enveloppe** — la silhouette de l'orateur ; l'écran (à gauche du crâne) et la bannière
   (à droite de la manche) sont géométriquement dehors.
4. **Trous internes rebouchés** — les verres, le liseré blanc de la tunique et les reflets sont
   intérieurs : on garde tout ce qui n'est pas relié au bord du cadre.
5. **Coupe franche au-dessus de la barre du pupitre** (``Y_COUPE``) : barre, Bible, pied du pupitre
   et bannière sous la silhouette sont hors du détourage.
6. **Frange** colorisée par propagation depuis l'intérieur, alpha strictement conservé.

    python3 scripts/cutout_ap_3458.py <photo> <sortie.png> [--apercu apercu.jpg]
"""
import sys

import cv2
import numpy as np
from PIL import Image

# --- géométrie mesurée sur le fichier (5906 × 3937) ---------------------------------------
Y_COUPE = 3285                     # ~40 px au-dessus de la barre du pupitre (dessus y ≈ 3325)
FENETRE_TETE = (2250, 1250, 2850, 2150)      # x0, y0, x1, y1 : fenêtre du crâne et de la barbe
SEED = (2500, 1600)                # un point sûr : la joue
# Le biseau sombre du bord droit de l'écran longe le crâne de (2790, 700) à (2960, 1570) : il
# finit par se souder aux cheveux. On le retire par une coupe qui suit son axe, à quelques pixels
# près — le museau de cheveux mordu fait moins de 2 px à l'échelle du visuel.
BISEAU = [(2785, 700), (2815, 900), (2845, 1100), (2875, 1300), (2905, 1450), (2930, 1540),
          (2960, 1570), (3170, 1570), (3170, 700)]

MICRO = [(2530, 1930), (2610, 1950), (2618, 2150), (2600, 2400), (2610, 2700),
         (2615, 2990), (2530, 2990), (2500, 2700), (2510, 2350), (2520, 2100)]

ENVELOPPE = [
    (2620, 700), (2450, 900), (2400, 1150), (2410, 1400), (2430, 1650), (2400, 1850),
    (2320, 2000), (2200, 2200), (2130, 2450), (2110, 2700), (2150, 2950), (2260, 3150),
    (2320, Y_COUPE),                                             # jusqu'à la coupe
    (3760, Y_COUPE), (3765, 3150), (3990, 3060), (4065, 2900),   # poignet : le poignet droit
    (4120, 2700), (4140, 2500),                                  # s'arrête au-dessus du torse
    (3900, 2350), (3700, 2200), (3450, 2050), (3150, 1900),      # épaule
    (3010, 1750), (2975, 1500), (2950, 1200), (2905, 950),       # crâne
    (2810, 800), (2700, 730),
]


def poly(shape, pts, e=1.0):
    m = np.zeros(shape, np.uint8)
    cv2.fillPoly(m, [np.array([[int(x * e), int(y * e)] for x, y in pts], np.int32)], 1)
    return m


def masque(sm, e):
    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[:, :, 0].astype(int), hsv[:, :, 1].astype(int), hsv[:, :, 2].astype(int)
    peau = ((h <= 26) | (h >= 163)) & (s >= 70) & (v >= 55)
    # V ≤ 120 : la tenue est sous-exposée (médiane 70-98) ; la bannière, de même teinte, est
    # mesurée à 141-221 dans les mêmes bleus. C'est ce plafond qui sépare la tunique du décor.
    tunique = (h >= 95) & (h <= 130) & (s >= 90) & (v >= 10) & (v <= 120)
    fen = np.zeros_like(peau)
    x0, y0, x1, y1 = FENETRE_TETE
    fen[int(y0 * e):int(y1 * e), int(x0 * e):int(x1 * e)] = True
    cheveux = (v < 105) & fen
    MICRO_M = poly(peau.shape, MICRO, e)          # polygone mesuré du micro, forcé
    m = ((peau | tunique | cheveux) | (MICRO_M > 0)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    env = poly(m.shape, ENVELOPPE, e)
    m = (m & env & (1 - poly(m.shape, BISEAU, e))).astype(np.uint8)

    # on garde les composantes qui contiennent le visage **ou** le micro mesuré : le micro n'est
    # pas une couleur qu'on sait isoler du décor, il est posé à la géométrie.
    n, lab = cv2.connectedComponents(m, 8)
    seed = lab[int(SEED[1] * e), int(SEED[0] * e)]
    if seed == 0:                                  # le point tombe dans un pli : on cherche autour
        for r in range(4, 200, 4):
            bloc = lab[max(0, int(SEED[1] * e) - r):int(SEED[1] * e) + r,
                       max(0, int(SEED[0] * e) - r):int(SEED[0] * e) + r]
            vals = bloc[bloc > 0]
            if vals.size:
                seed = np.bincount(vals).argmax()
                break
    suj = (lab == seed).astype(np.uint8)
    mic_labels = np.unique(lab[MICRO_M.astype(bool)])
    suj = np.isin(lab, [seed] + [v for v in mic_labels if v > 0]).astype(np.uint8)

    # structures fines retirées : le biseau sombre du bord de l'écran passe juste derrière le
    # crâne et se soude aux cheveux — une ouverture le sépare, et le micro est protégé.
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
    fins = (suj & (1 - cv2.morphologyEx(suj, cv2.MORPH_OPEN, k))).astype(np.uint8)
    protege = cv2.dilate(poly(suj.shape, MICRO, e), np.ones((25, 25), np.uint8))
    suj = (suj & (1 - (fins & (1 - protege)))).astype(np.uint8)
    suj = cv2.morphologyEx(suj, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))

    # trous internes rebouchés (le cadre extérieur reste à zéro)
    ff = suj.copy()
    cv2.floodFill(ff, np.zeros((ff.shape[0] + 2, ff.shape[1] + 2), np.uint8), (0, 0), 1)
    suj = (suj | (ff == 0).astype(np.uint8))
    suj[int(Y_COUPE * e):, :] = 0

    # ---- 4bis. éclats de décor restés dans l'enveloppe. Retirés par leur couleur **dans des
    # cadres mesurés vides de corps** — jamais sur toute l'image : le verre de la montre est gris
    # neutre, la bague du micro bleu vif, et une règle globale les mangerait.
    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
    hh, ss, vv = hsv[:, :, 0].astype(int), hsv[:, :, 1].astype(int), hsv[:, :, 2].astype(int)
    decor = np.zeros_like(suj)
    for (bx0, by0, bx1, by1), regle in (
            ((2190, 700, 2540, 1010), (ss <= 70) & (vv >= 100) & (vv <= 200)),       # support gris
            ((2230, 1860, 2560, 2150), ((hh >= 88) & (hh <= 138) & (ss >= 105) & (vv >= 125))
                                        | ((vv >= 148) & (ss <= 95))),                # éclats bleus
            # écran : ses teintes sont celles de la bannière (H 94-99, S 111-144, V 181-206),
            # mesurées à trois endroits ; la peau de la joue et de la mâchoire est en H ≈ 8.
            ((2140, 1750, 2620, 2145), (hh >= 88) & (hh <= 138) & (ss >= 100) & (vv >= 115)),
            ((3520, 3080, 4020, 3280), ((hh >= 88) & (hh <= 138) & (ss >= 110) & (vv >= 130))
                                        | ((hh >= 14) & (hh <= 42) & (ss >= 110)))):  # bannière
        # on ne retire **que** les pixels de la couleur mesurée, dans le cadre — jamais le cadre
        cadre = decor[int(by0 * e):int(by1 * e), int(bx0 * e):int(bx1 * e)]
        decor[int(by0 * e):int(by1 * e), int(bx0 * e):int(bx1 * e)] = regle[
            int(by0 * e):int(by1 * e), int(bx0 * e):int(bx1 * e)].astype(np.uint8)
    suj = (suj & (1 - decor.astype(np.uint8))).astype(np.uint8)
    suj = cv2.morphologyEx(suj, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8))
    n, lab = cv2.connectedComponents(suj, 8)
    seed = lab[int(SEED[1] * e), int(SEED[0] * e)]
    suj = (lab == seed).astype(np.uint8)
    suj[int(Y_COUPE * e):, :] = 0

    # échardes restées hors des deux amorces (fragments de bannière, points de l'écran) : une
    # composante isolée de moins de 0,2 % de l'aire du sujet ne peut pas être un membre — la
    # plus petite main de ce détourage en occupe cinquante fois plus.
    n, lab, st, _ = cv2.connectedComponentsWithStats(suj, 8)
    if n > 1:
        aire = st[1:, 4]
        garde = [i for i in range(1, n) if st[i, 4] >= 0.002 * aire.max()]
        suj = np.isin(lab, garde).astype(np.uint8)
    return suj


def detourer(photo, sortie, apercu=None):
    im = cv2.imread(photo)
    H, W = im.shape[:2]
    e = 0.5
    sm = cv2.resize(im, None, fx=e, fy=e, interpolation=cv2.INTER_AREA)
    suj = masque(sm, e)

    a = cv2.medianBlur(suj * 255, 5)
    a = cv2.GaussianBlur(a, (0, 0), 1.0)
    a = np.where(a > 118, 255, np.clip((a.astype(np.int16) - 46) * 2.2, 0, 255)).astype(np.uint8)
    alpha = cv2.resize(a, (W, H), interpolation=cv2.INTER_LINEAR)
    alpha[alpha < 14] = 0

    bx, by, bw, bh = cv2.boundingRect((alpha > 8).astype(np.uint8))
    rgba = cv2.cvtColor(im, cv2.COLOR_BGR2RGBA)
    rgba[:, :, 3] = alpha
    pil = Image.fromarray(rgba).crop((bx, by, bx + bw, by + bh))

    # frange : la couleur vient de l'intérieur du sujet, l'alpha reste identique au pixel
    arr = np.asarray(pil).astype(np.float32)
    rgb, al = arr[:, :, :3], arr[:, :, 3] / 255.0
    connu = (al >= 0.985).astype(np.float32)
    front = ((al > 0) & (al < 0.985)).astype(np.float32)
    coul = rgb * connu[..., None]
    m = connu.copy()
    for _ in range(14):
        cb, mb = cv2.blur(coul, (5, 5)), cv2.blur(m, (5, 5))
        dispo = (mb > 1e-4) & (front > 0)
        if not dispo.any():
            break
        coul[dispo] = cb[dispo] / mb[dispo][:, None]
        m[dispo] = 1.0
        front[dispo] = 0.0
    # ---- 7bis. franges du décor restées **opaques** : le lettrage magenta de la bannière passe
    # juste derrière le poignet droit et laisse deux taches roses sur le bord du costume ; un
    # fragment du pied de micro traîne à gauche de la capsule. Retirés par couleur et par fenêtre
    # mesurées — la peau (H ≈ 8) et la tunique (H ≈ 107) ne sont jamais dans ces plages.
    rgb8 = np.dstack([np.clip(coul, 0, 255), arr[:, :, 3]]).astype(np.uint8)
    hsv8 = cv2.cvtColor(rgb8[:, :, :3], cv2.COLOR_RGB2HSV)
    hh, ss, vv = hsv8[:, :, 0].astype(int), hsv8[:, :, 1].astype(int), hsv8[:, :, 2].astype(int)
    magenta = (hh >= 140) & (hh <= 175) & (ss >= 110) & (vv >= 120)
    fen = np.zeros(magenta.shape, bool)
    fen[1330:1480, 1670:1786] = True                      # poignet droit, bord du costume
    tache = magenta & fen
    if tache.any():
        # la couleur de remplacement vient de la tunique **autour** de la tache : on propage par
        # moyenne pondérée en partant du voisinage connu, jamais d'un gris inventé.
        rgb_f = rgb8[:, :, :3].astype(np.float32)
        connu = (~tache).astype(np.float32)
        coul_p = rgb_f * connu[..., None]
        for _ in range(12):
            moy = cv2.blur(coul_p, (13, 13))
            cnt = cv2.blur(connu, (13, 13))
            ok = tache & (cnt > 1e-3)
            if not ok.any():
                break
            rgb_f[ok] = moy[ok] / cnt[ok][:, None]
            coul_p[ok] = rgb_f[ok]
            connu[ok] = 1.0
            tache &= ~ok
        rgb8[:, :, :3] = np.clip(rgb_f, 0, 255).astype(np.uint8)
    out = Image.fromarray(rgb8, "RGBA")
    out.save(sortie)
    print(f"écrit {sortie} · {out.width}×{out.height} · opaque {100 * (al > 0.5).mean():.1f} % "
          f"· coupe pupitre y={Y_COUPE}")

    if apercu:
        plateau = Image.new("RGBA", out.size, (233, 32, 176, 255))
        plateau.alpha_composite(out)
        plateau.convert("RGB").resize((720, round(720 * out.height / out.width)),
                                      Image.LANCZOS).save(apercu, quality=93)
        print("aperçu", apercu)
    return out


if __name__ == "__main__":
    ap = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--apercu" else None
    detourer(sys.argv[1], sys.argv[2], ap)
