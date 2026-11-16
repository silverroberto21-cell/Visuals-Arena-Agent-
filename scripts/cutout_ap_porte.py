#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Détourage de `_DSC3532` (AP Enock MISSIMAHOU devant une porte) — méthode en deux temps.

1. **Familles de couleurs mesurées** sur la photo : tunique bleu marine, peau (chaude, saturée,
   claire), micro (gris sombre désaturé). Elles donnent des graines **sûres**, pas la silhouette.
2. **grabCut contraint** : graines premier plan = intérieur érodé des familles, graines fond =
   bords de l'image + mur/porte. Le bord du masque est donc celui de grabCut, jamais un
   rétrécissement : la silhouette n'est pas rongée.
3. **Post-traitement prudent** : on garde les composantes reliées au sujet (les reflets de la
   porte qui flottent s'en vont), on rebouche les verres des lunettes et la grille du micro,
   on adoucit 0,8 px de contour et on **décontamine** le liseré de fond sur 2 px.

Aucune génération, aucune retouche du visage, de la peau ou de la tenue : uniquement masque,
contour et lumière.

    python3 scripts/cutout_ap_porte.py <photo> <sortie.png> [--apercu f.jpg]
"""
import argparse

import cv2
import numpy as np

# micro tenu devant la tunique : rectangle protégé (relatif)
MIC = (0.432, 0.594, 0.500, 0.852)


def familles(sm):
    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[:, :, 0].astype(int), hsv[:, :, 1].astype(int), hsv[:, :, 2].astype(int)
    tunique = (H >= 97) & (H <= 142) & (S >= 80) & (V >= 12)
    peau = ((H <= 25) | (H >= 168)) & (S >= 95) & (S <= 205) & (V >= 150)
    micro = (V < 75) & (S < 130)
    return tunique | peau | micro, peau


def masque(bgr, s=0.45):
    h, w = bgr.shape[:2]
    sm = cv2.resize(bgr, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
    fg, peau = familles(sm)

    fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg, 8)
    fg = (lab == (1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])))).astype(np.uint8)
    fg = cv2.dilate(fg, np.ones((9, 9), np.uint8))

    mask = np.full(fg.shape, cv2.GC_PR_BGD, np.uint8)
    mask[fg > 0] = cv2.GC_PR_FGD
    mask[cv2.erode(fg, np.ones((21, 21), np.uint8)) > 0] = cv2.GC_FGD
    b = 40                                   # bords = fond sûr
    mask[:b, :] = mask[-b:, :] = mask[:, :b] = mask[:, -b:] = cv2.GC_BGD

    # micro : région « probablement sujet » pleine (il est tenu devant le torse)
    mh, mw = mask.shape
    mask[int(MIC[1] * mh):int(MIC[3] * mh), int(MIC[0] * mw):int(MIC[2] * mw)] = cv2.GC_FGD

    cv2.grabCut(sm, mask, None, np.zeros((1, 65), np.float64),
                np.zeros((1, 65), np.float64), 6, cv2.GC_INIT_WITH_MASK)
    sujet = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    mh, mw = sujet.shape

    # 1. composantes : la principale + ce qui la touche (aucun membre isolé perdu) ;
    #    les reflets de porte qui flottent s'en vont
    n, lab, st, _ = cv2.connectedComponentsWithStats(sujet, 8)
    if n > 1:
        principal = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        garde = (lab == principal).astype(np.uint8)
        dil = cv2.dilate(garde, np.ones((5, 5), np.uint8))
        for i in range(1, n):
            if i == principal or st[i, cv2.CC_STAT_AREA] < 200:
                continue
            if (dil[lab == i] > 0).mean() > 0.02:
                garde[lab == i] = 1
        sujet = garde * 255

    # 2. trous intérieurs d'abord : verres des lunettes, corps du micro, plis entre les doigts
    ff = sujet.copy()
    m2 = np.zeros((ff.shape[0] + 2, ff.shape[1] + 2), np.uint8)
    cv2.floodFill(ff, m2, (0, 0), 255)
    sujet = cv2.bitwise_or(sujet, cv2.bitwise_not(ff))

    # 3. ENSUITE les reflets de la porte rattachés au contour : ni tunique (bleu marine
    #    saturé) ni peau (chaude, saturée, claire), et au contact de la transparence.
    #    Un verre de lunettes est entouré de monture, jamais au contact du vide : protégé.
    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
    Hh, Ss, Vv = hsv[:, :, 0].astype(int), hsv[:, :, 1].astype(int), hsv[:, :, 2].astype(int)
    tunique = (Hh >= 92) & (Hh <= 148) & (Ss >= 70)
    peau = ((Hh <= 26) | (Hh >= 168)) & (Ss >= 108) & (Vv >= 118)
    cheveux = (Vv <= 115) & (Ss <= 175)
    autre = (~tunique) & (~peau) & (~cheveux) & (sujet > 0)
    bord = cv2.dilate((sujet < 40).astype(np.uint8) * 255, np.ones((21, 21), np.uint8))
    reflet = cv2.bitwise_and(autre.astype(np.uint8) * 255, bord)
    reflet = cv2.morphologyEx(reflet, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(reflet, 8)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] < 900:
            continue
        sel = cv2.dilate((lab == i).astype(np.uint8) * 255, np.ones((11, 11), np.uint8)) > 0
        sujet[sel] = 0

    sujet = cv2.medianBlur(sujet, 5)
    alpha = cv2.resize(sujet, (w, h), interpolation=cv2.INTER_LINEAR)
    alpha = cv2.GaussianBlur(alpha, (0, 0), 0.9)
    return alpha, peau


def decontaminer(bgr, alpha, px=3):
    """Remplace le liseré de fond (mur clair, porte acajou) par la couleur du sujet voisin.

    On ne retire rien : on remplace la couleur des pixels de bord, dont l'alpha est partiel,
    par celle du pixel de sujet le plus proche — c'est ce qui évite la frange claire.
    """
    a = alpha.astype(np.float32) / 255.0
    bord = (a > 0.03) & (a < 0.97)
    coeur = a >= 0.97
    if not coeur.any():
        return bgr
    # propagation de la couleur du cœur vers la bordure
    _, labels = cv2.distanceTransformWithLabels((~coeur).astype(np.uint8), cv2.DIST_L2, 5,
                                                labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.where(coeur)
    table = np.zeros((labels.max() + 1, 3), np.float32)
    table[labels[coeur]] = bgr[coeur]
    remplacement = table[labels[bord]].reshape(-1, 3)
    out = bgr.copy()
    out[bord] = remplacement.astype(np.uint8)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("sortie")
    ap.add_argument("--apercu", default=None)
    a = ap.parse_args()

    bgr = cv2.imread(a.photo, cv2.IMREAD_COLOR)
    alpha, _ = masque(bgr)
    clean = decontaminer(bgr, alpha)
    bgra = np.dstack([clean, alpha])
    cv2.imwrite(a.sortie, bgra)

    if a.apercu:
        vis = cv2.resize(bgr, (int(bgr.shape[1] * 0.22), int(bgr.shape[0] * 0.22)))
        al = cv2.resize(alpha, (vis.shape[1], vis.shape[0]))
        vis[al < 20] = (255, 0, 255)
        cv2.imwrite(a.apercu, vis)

    ys, xs = np.where(alpha > 20)
    print(f"{a.sortie} — {bgr.shape[1]}×{bgr.shape[0]}")
    print(f"boîte du sujet : x {xs.min()}..{xs.max()} · y {ys.min()}..{ys.max()}")
    print("bords touchés : "
          f"haut {ys.min() < 4} · bas {ys.max() > bgr.shape[0] - 5} · "
          f"gauche {xs.min() < 4} · droite {xs.max() > bgr.shape[1] - 5}")


if __name__ == "__main__":
    main()
