#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Détourage de `_DSC3532` (AP Enock MISSIMAHOU, plan poitrine devant une porte) — chaîne validée.

Suite de [`cutout_ap_porte.py`] : ce script reprend son masque de base (grabCut contraint) et
applique les **quatre corrections vérifiées à la main** qui ont donné la silhouette livrée. Chaque
correction est bornée par un rectangle ou une règle mesurée sur la photo — aucune n'est un balayage
de silhouette, aucune ne touche au visage.

1. **Bloc de porte derrière l'oreille** et **reflet d'épaule** : de la teinte de la peau
   (H 9-16, S 60-190, V 140-200), donc aucune règle de couleur ne les sépare du visage. Ils sont
   retirés par **rectangle vérifié vide de corps**, filtré sur la couleur « porte » uniquement.
2. **Fente bras / buste** : mur gris peu saturé + bois de porte, retirés à la couleur **avec
   garde-fou** — un pixel de peau ou de tunique n'est jamais touché.
3. **Trous internes** (verres des lunettes, barbe) : rebouchés **à l'intérieur de l'enveloppe
   convexe de la tête seulement**.
4. **Encoches de la mâchoire** : fermeture morphologique bornée à la bande de la tête — c'est elle
   qui remplace l'ancien balayage ligne par ligne, lequel coupait la joue au couteau.

    python3 scripts/cutout_ap_podium.py <photo> <sortie.png> [--apercu a.jpg] [--hauteur 1600]
"""
import argparse
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cutout_ap_porte as base  # noqa: E402  (masque de base : grabCut contraint)

# rectangles « décor » vérifiés vides de corps, en relatif (x0, x1, y0, y1)
RECTS_PORTE = [
    (0.548, 0.640, 0.215, 0.335),   # bloc de porte derrière l'oreille droite
    (0.672, 0.780, 0.400, 0.500),   # reflet de porte sur l'épaule / le bras
]
# fente entre le bras et le buste
RECT_FENTE = (0.235, 0.415, 0.545, 0.845)
# bande de la tête : enveloppe convexe, trous internes, encoches
BANDE_TETE = (0.33, 0.63, 0.10, 0.46)


def trous_de_tete(sujet, sm):
    """Rebouche les trous internes de la tête (verres, barbe) sans jamais déborder dehors."""
    mh, mw = sujet.shape
    x0, x1, y0, y1 = BANDE_TETE
    bande = np.zeros((mh, mw), np.uint8)
    bande[int(y0 * mh):int(y1 * mh), int(x0 * mw):int(x1 * mw)] = 255

    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[:, :, 0].astype(int), hsv[:, :, 1].astype(int), hsv[:, :, 2].astype(int)
    tete = (((H <= 32) | (H >= 160)) & (S >= 90) & (V >= 45)) | ((V <= 110) & (S <= 200))
    tete = cv2.bitwise_and((tete.astype(np.uint8) * 255), bande)

    n, lab, st, _ = cv2.connectedComponentsWithStats(tete, 8)
    if n < 2:
        return sujet
    tete = ((lab == (1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])))).astype(np.uint8) * 255)
    cnts, _ = cv2.findContours(tete, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hull = cv2.convexHull(max(cnts, key=cv2.contourArea))
    hullm = np.zeros((mh, mw), np.uint8)
    cv2.fillPoly(hullm, [hull], 255)
    hullm = cv2.erode(hullm, np.ones((7, 7), np.uint8))

    # on ne remplit QUE les trous intérieurs de l'enveloppe : jamais l'extérieur
    ff = hullm.copy()
    m2 = np.zeros((mh + 2, mw + 2), np.uint8)
    cv2.floodFill(ff, m2, (0, 0), 255)
    trous = cv2.bitwise_not(ff)
    return cv2.bitwise_or(sujet, trous)


def retirer_fente(sujet, sm):
    """Fente bras / buste : mur gris peu saturé + bois de porte, avec garde-fou peau + tunique."""
    mh, mw = sujet.shape
    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[:, :, 0].astype(int), hsv[:, :, 1].astype(int), hsv[:, :, 2].astype(int)
    chemise = (H >= 85) & (H <= 165) & (S >= 50)
    peau = ((H <= 25) | (H >= 165)) & (S >= 110) & (V >= 105)
    mur = (S <= 50) & (V >= 125)
    bois = ((H <= 18) | (H >= 168)) & (S >= 170) & (V >= 50) & (V <= 120)
    decor = mur | bois

    x0, x1, y0, y1 = RECT_FENTE
    zone = np.zeros((mh, mw), bool)
    zone[int(y0 * mh):int(y1 * mh), int(x0 * mw):int(x1 * mw)] = True
    garde = cv2.dilate(((peau | chemise).astype(np.uint8)) * 255,
                       np.ones((5, 5), np.uint8)) > 0
    cible = zone & decor & (sujet > 20) & (~garde)
    # le mur clair et neutre (S très bas) ne peut pas être ni la peau ni la tunique : il part
    # même dans le voisinage protégé — c'est lui qui laissait une bande beige entre bras et buste
    cible |= zone & (S <= 65) & (V >= 115) & (sujet > 20)
    sujet = sujet.copy()
    sujet[cible] = 0

    # les poussières de porte restantes dans la fente : ouverture bornée à la zone
    ouv = cv2.morphologyEx((sujet > 127).astype(np.uint8) * 255, cv2.MORPH_OPEN,
                           np.ones((5, 5), np.uint8))
    sujet[(ouv == 0) & zone] = 0
    return sujet


def retirer_rectangles(sujet, sm):
    """Les deux blocs de porte : rectangle borné × couleur « porte » uniquement."""
    mh, mw = sujet.shape
    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[:, :, 0].astype(int), hsv[:, :, 1].astype(int), hsv[:, :, 2].astype(int)
    porte = (((H <= 25) | (H >= 165)) & (S >= 50) & (V >= 60) & (V <= 215)) | \
            ((S <= 70) & (V >= 120) & (V <= 215))
    sujet = sujet.copy()
    total = 0
    for x0, x1, y0, y1 in RECTS_PORTE:
        zone = np.zeros((mh, mw), bool)
        zone[int(y0 * mh):int(y1 * mh), int(x0 * mw):int(x1 * mw)] = True
        cible = zone & porte & (sujet > 20)
        total += int(cible.sum())
        sujet[cible] = 0
    print(f"  rectangles de porte : {total} px retirés")
    return sujet


def retirer_mur_attache(sujet, sm):
    """Le mur beige resté dans la fente entre le bras et le buste.

    Il a la même *teinte* que la porte (chaude), d'où l'échec des seuils de saturation : ce qui le
    sépare de la peau, c'est **l'écart R-G**. La peau du visage et de la main est franchement rouge
    (R-G ≈ 75-95) ; le mur beige est presque neutre (R-G ≈ 20). La tunique, elle, a B > R.
    On retire donc : chaud (R > B), peu rouge (R-G < 45), clair (V ≥ 100) — borné à la fente,
    et jamais au contact d'un pixel de peau."""
    arr = sm.astype(int)
    B, G, R = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
    S, V = hsv[:, :, 1].astype(int), hsv[:, :, 2].astype(int)
    mh, mw = sujet.shape
    zone = np.zeros((mh, mw), bool)
    x0, x1, y0, y1 = RECT_FENTE
    zone[int(y0 * mh):int(y1 * mh), int(x0 * mw):int(x1 * mw)] = True

    peau = ((R - G) >= 55) & (R > 120)
    mur = (R > B) & ((R - G) < 45) & (V >= 95) & (S <= 150)
    garde = cv2.dilate((peau.astype(np.uint8)) * 255, np.ones((5, 5), np.uint8)) > 0
    cible = zone & mur & (sujet > 20) & (~garde)
    sujet = sujet.copy()
    sujet[cible] = 0
    print(f"  mur beige dans la fente : {int(cible.sum())} px retirés")
    return sujet


def retirer_eclats_bord(sujet, sm):
    """Écharde de bois de la porte sur la ligne d'épaule (x 0,30-0,38 · y 0,39-0,46 de la photo).

    Le morceau est **chaud** (R > B) alors que la tunique est froide (B > R). On retire les
    **petits amas** chauds de ce quadrilatère — jamais une grande trame, jamais le cou ni la peau :
    un amas de plus de 800 px n'est pas une écharde, c'est un morceau du sujet."""
    arr = sm.astype(int)
    B, G, R = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    mh, mw = sujet.shape
    zone = np.zeros((mh, mw), bool)
    x0, x1, y0, y1 = 0.300, 0.380, 0.385, 0.465
    zone[int(y0 * mh):int(y1 * mh), int(x0 * mw):int(x1 * mw)] = True
    chaud = (R > B + 15) & (R > 90) & (sujet > 20) & zone
    n, lab, st, _ = cv2.connectedComponentsWithStats(chaud.astype(np.uint8), 8)
    sujet = sujet.copy()
    total = 0
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 800:
            continue
        total += int(st[i, cv2.CC_STAT_AREA])
        sujet[lab == i] = 0
    print(f"  écharde sur le bord d'épaule : {total} px retirés")
    return sujet


def nettoyer(bgr, s=0.45):
    mh, mw = int(bgr.shape[0] * s), int(bgr.shape[1] * s)
    sm = cv2.resize(bgr, (mw, mh), interpolation=cv2.INTER_AREA)
    alpha, _ = base.masque(bgr, s)
    sujet = (cv2.resize(alpha, (mw, mh), interpolation=cv2.INTER_AREA) > 127).astype(np.uint8) * 255

    sujet = retirer_rectangles(sujet, sm)
    sujet = retirer_fente(sujet, sm)
    sujet = retirer_mur_attache(sujet, sm)
    sujet = retirer_eclats_bord(sujet, sm)
    sujet = trous_de_tete(sujet, sm)

    # encoches de la mâchoire : fermeture bornée à la bande de la tête
    x0, x1, y0, y1 = BANDE_TETE
    bande = np.zeros((mh, mw), np.uint8)
    bande[int(y0 * mh):int(y1 * mh), int(x0 * mw):int(x1 * mw)] = 255
    ferme = cv2.morphologyEx(sujet, cv2.MORPH_CLOSE,
                             cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
    sujet = np.where(bande > 0, ferme, sujet).astype(np.uint8)
    # rebouchage des trous internes : une transparence que le fond extérieur ne rejoint pas est un
    # trou dans le sujet (col, pli, verre) — jamais une découpe volontaire. C'est ce qui répare les
    # crans laissés par un retrait trop gourmand.
    ff = sujet.copy()
    m2 = np.zeros((mh + 2, mw + 2), np.uint8)
    cv2.floodFill(ff, m2, (0, 0), 255)
    trous = cv2.bitwise_not(ff)
    # la fente bras / buste est une découpe VOLONTAIRE : on ne la rebouche jamais
    x0, x1, y0, y1 = RECT_FENTE
    fente = np.zeros((mh, mw), np.uint8)
    fente[int(y0 * mh):int(y1 * mh), int(x0 * mw):int(x1 * mw)] = 255
    trous = cv2.bitwise_and(trous, cv2.bitwise_not(fente))
    avant = int(((trous > 0) & (sujet == 0)).sum())
    sujet = cv2.bitwise_or(sujet, trous)
    print(f"  trous internes rebouchés : {avant} px")

    sujet = cv2.medianBlur(sujet, 7)

    # une seule silhouette : la composante principale (les poussières détachées s'en vont)
    n, lab, st, _ = cv2.connectedComponentsWithStats((sujet > 127).astype(np.uint8), 8)
    principal = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    sujet = ((lab == principal).astype(np.uint8)) * 255

    alpha = cv2.resize(sujet, (bgr.shape[1], bgr.shape[0]), interpolation=cv2.INTER_LINEAR)
    return cv2.GaussianBlur(alpha, (0, 0), 1.0)


def retirer_bois_final(bgra):
    """Dernier nettoyage, dans l'espace du détourage (après recadrage) : l'éclat de bois de la porte
    posé sur la ligne d'épaule.

    Règle **géométrique + couleur**, sans jamais toucher au corps : on prend les pixels *chauds*
    (R > B, donc ni la tunique bleue, ni le fond) du quadrilatère, et on ne retire que les amas
    **entièrement contenus** dans ce quadrilatère. La peau du visage et du cou appartient à une
    composante bien plus grande qui déborde du cadre : elle ne peut donc jamais être retirée, même
    si elle est chaude.
    """
    h, w = bgra.shape[:2]
    img = bgra[:, :, :3].astype(int)
    B, R = img[:, :, 0], img[:, :, 2]
    alpha = bgra[:, :, 3]

    x0, x1, y0, y1 = 0.570, 0.670, 0.280, 0.340
    px0, px1 = int(x0 * w), int(x1 * w)
    py0, py1 = int(y0 * h), int(y1 * h)

    chaud = ((R > B + 18) & (alpha > 40)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(chaud, 8)
    total = 0
    for i in range(1, n):
        x, y, ww, hh, ar = st[i]
        dedans = (x >= px0) and (y >= py0) and (x + ww <= px1) and (y + hh <= py1)
        if not dedans:
            continue
        total += int(ar)
        bgra[lab == i, 3] = 0
    print(f"  éclat de bois sur l'épaule : {total} px retirés")
    return bgra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("sortie")
    ap.add_argument("--apercu", default=None)
    ap.add_argument("--hauteur", type=int, default=1600)
    a = ap.parse_args()

    bgr = cv2.imread(a.photo, cv2.IMREAD_COLOR)
    print("1/3 masque de base (grabCut contraint)…")
    alpha = nettoyer(bgr)
    print("2/3 décontamination du liseré…")
    clean = base.decontaminer(bgr, alpha)
    bgra = np.dstack([clean, alpha])

    print("3/3 recadrage + échelle…")
    ys, xs = np.where(alpha > 8)
    bgra = bgra[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h = a.hauteur
    w = round(bgra.shape[1] * h / bgra.shape[0])
    bgra = cv2.resize(bgra, (w, h), interpolation=cv2.INTER_AREA)
    bgra = retirer_bois_final(bgra)
    cv2.imwrite(a.sortie, bgra)

    if a.apercu:
        vis = cv2.resize(bgr, (int(bgr.shape[1] * 0.22), int(bgr.shape[0] * 0.22)))
        al = cv2.resize(alpha, (vis.shape[1], vis.shape[0]))
        vis[al < 60] = (255, 0, 255)
        cv2.imwrite(a.apercu, vis)

    print(f"écrit {a.sortie} — {bgra.shape[1]}×{bgra.shape[0]}")
    print(f"alpha : {(alpha > 250).mean() * 100:.1f} % opaque · {(alpha < 5).mean() * 100:.1f} % transparent")
    print(f"bords touchés : bas {(alpha[-3:] > 200).any()} (photo coupée à la source → à ancrer)")


if __name__ == "__main__":
    main()
