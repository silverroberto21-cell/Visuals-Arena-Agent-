#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Détourage du sujet (orateur) sur fond de studio clair — méthode du dépôt.

Trois garanties, dans cet ordre :
1. **Aucune érosion de la silhouette** : le contour du sujet est celui du grabCut, pas
   celui d'un rétrécissement. C'est le défaut qui « ronge » les bras et les mains.
2. **Décontamination de couleur** : le liseré blanc du studio est remplacé par la couleur
   du sujet la plus proche (propagation depuis l'intérieur), pas effacé.
3. **Zones protégées** : tête + lunettes (enveloppe convexe) et micro sont reconstruites
   avant tout nettoyage — sinon les verres et la grille du micro se confondent avec le mur.

    python3 scripts/cutout_sujet.py <photo.jpg> <sortie.png> [--box l,h,r,b] [--crop l,h,r,b]
"""
import argparse
import cv2
import numpy as np


def grabcut_alpha(bgr, seeds_fg, seeds_bg):
    H, W = bgr.shape[:2]
    mask = np.full((H, W), 2, np.uint8)
    for (y0, y1, x0, x1) in seeds_fg:
        mask[int(H * y0):int(H * y1), int(W * x0):int(W * x1)] = 1
    for (y0, y1, x0, x1) in seeds_bg:
        mask[int(H * y0):int(H * y1), int(W * x0):int(W * x1)] = 0
    bgd, fgd = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    cv2.grabCut(bgr, mask, None, bgd, fgd, 12, cv2.GC_INIT_WITH_MASK)
    return np.where((mask == 2) | (mask == 0), 0, 255).astype(np.uint8)


def protect_zones(bgr):
    """Tête + lunettes et micro : ce qui se confond avec le mur du studio."""
    H, W = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(np.int32)
    hh, ss, vv = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

    skin = (((hh <= 26) | (hh >= 166)) & (ss > 50) & (vv > 45))
    hair = (vv < 110)
    seed = ((skin | hair)).astype(np.uint8) * 255
    seed[int(H * 0.40):, :] = 0
    seed = cv2.morphologyEx(seed, cv2.MORPH_CLOSE, np.ones((31, 31), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(seed, 8)
    idx = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    head = np.where(lab == idx, 255, 0).astype(np.uint8)
    cnts, _ = cv2.findContours(head, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hull = cv2.convexHull(max(cnts, key=cv2.contourArea))
    headm = np.zeros((H, W), np.uint8)
    cv2.fillPoly(headm, [hull], 255)
    headm = cv2.erode(headm, np.ones((5, 5), np.uint8))

    # micro : il est TENU DEVANT la chemise — la zone qu'il occupe appartient donc au
    # sujet. On la protège en bloc (plutôt que d'espérer retrouver sa silhouette) : c'est
    # le seul moyen de ne pas percer le corps argenté quand il touche le blanc du studio.
    # bornes mesurées à la grille sur la photo : la grille du micro commence à y 0,50 et le
    # fut argenté s'arrête à x 0,545. Toute marge au-delà ramenait du studio avec elle.
    micm = np.zeros((H, W), np.uint8)
    cv2.rectangle(micm, (int(W * 0.435), int(H * 0.475)), (int(W * 0.548), int(H * 0.868)),
                  255, thickness=-1)   # rectangle PLEIN (thickness=-1)
    return headm, micm, hsv


def clean(bgr, alpha, headm, micm, vv, ss):
    """Nettoyage final. Aucune reconstruction de silhouette : le bras et les mains gardent
    exactement leur contour d'origine, on ne fait que retirer le mur du studio."""
    H, W = alpha.shape

    # le mur du studio : clair, neutre ET relié au bord de l'image. Le troisième critère
    # est décisif : un front ou une épaule très clairs ne sont jamais « reliés au bord »,
    # alors que le mur l'est toujours. Sans lui, on perçait le visage.
    studio = ((vv > 186) & (ss < 48)).astype(np.uint8)
    n, lab = cv2.connectedComponents(studio, 8)
    border = (set(lab[0, :]) | set(lab[-1, :]) | set(lab[:, 0]) | set(lab[:, -1])) - {0}
    studio = (np.isin(lab, list(border))).astype(np.uint8) * 255

    # 1. le micro est tenu devant la chemise : sa zone est pleine par construction
    alpha = cv2.bitwise_or(alpha, micm)

    # 2. le mur sort — sauf dans le micro
    alpha = cv2.bitwise_and(alpha, cv2.bitwise_not(
        cv2.bitwise_and(studio, cv2.bitwise_not(micm))))

    # 3. trous : SEULEMENT ceux qui sont intérieurs à une zone protégée, c'est-à-dire les
    #    verres des lunettes et la grille du micro. Ailleurs, une poche claire est le studio
    #    qu'on voit entre un bras et le buste : elle doit rester transparente. C'est la règle
    #    qui met fin aux taches blanches sur l'épaule et au voile du temple.
    ff = alpha.copy()
    m2 = np.zeros((H + 2, W + 2), np.uint8)
    cv2.floodFill(ff, m2, (0, 0), 255)
    holes = cv2.bitwise_not(ff)
    inside = cv2.bitwise_or(headm, micm)
    n, lab, st, _ = cv2.connectedComponentsWithStats(holes, 8)
    fill = np.zeros((H, W), np.uint8)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] >= 6000:
            continue
        sel = (lab == i)
        if float((inside[sel] > 0).mean()) < 0.5:
            continue
        fill[sel] = 255
    alpha = cv2.bitwise_or(alpha, fill)

    # 4. îlots parasites (branche de lunettes détachée, poussières)
    n, lab, st, _ = cv2.connectedComponentsWithStats(alpha, 8)
    keep = np.zeros((H, W), np.uint8)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 20000:
            keep[lab == i] = 255
    alpha = cv2.medianBlur(keep, 3)

    # 3bis. le mur qui s'est glissé entre deux doigts, ou entre le bras et le buste, est un
    #       fragment ENFERMÉ dans le sujet : sa couleur est celle du studio (blanc pur,
    #       désaturé), pas celle d'un reflet. On le retire uniquement s'il est petit et s'il
    #       touche une zone déjà transparente — c'est ce qui distingue une ouverture d'une
    #       tache de lumière sur la peau.
    pure = ((vv > 225) & (ss < 30)).astype(np.uint8) * 255
    pure = cv2.bitwise_and(pure, cv2.bitwise_not(micm))
    near = cv2.dilate((alpha < 40).astype(np.uint8) * 255, np.ones((15, 15), np.uint8))
    pure = cv2.bitwise_and(cv2.bitwise_and(pure, near), alpha)
    n, lab, st, _ = cv2.connectedComponentsWithStats(pure, 8)
    leak = np.zeros((H, W), np.uint8)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 9000:
            continue
        leak[lab == i] = 255
    alpha = cv2.bitwise_and(alpha, cv2.bitwise_not(leak))

    # 3ter. un morceau de décor sombre et FLOU (l'écran LED vu entre les doigts) n'est pas
    #       le sujet : la chemise est un vichy très contrasté, la peau est texturée, alors
    #       que ce fragment est lisse. On ne retire que les taches lisses, sombres, petites,
    #       hors zones protégées et en contact avec la transparence.
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    m1 = cv2.blur(g, (9, 9))
    sd = np.sqrt(np.maximum(cv2.blur(g * g, (9, 9)) - m1 * m1, 0))
    smooth = ((sd < 6.0) & (vv < 150)).astype(np.uint8) * 255
    smooth = cv2.bitwise_and(smooth, cv2.bitwise_not(cv2.bitwise_or(headm, micm)))
    smooth = cv2.bitwise_and(smooth, alpha)
    near = cv2.dilate((alpha < 40).astype(np.uint8) * 255, np.ones((15, 15), np.uint8))
    smooth = cv2.bitwise_and(smooth, near)
    smooth = cv2.morphologyEx(smooth, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(smooth, 8)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 25000:
            continue
        sel = (lab == i)
        sel = cv2.dilate(sel.astype(np.uint8) * 255, np.ones((5, 5), np.uint8)) > 0
        alpha[sel] = 0

    # 3quater. fragment d'écran resté entre deux doigts : bleu très saturé et sombre, petit,
    #          collé à la transparence et hors des zones protégées. La chemise, elle, est un
    #          vichy clair et saumoné : jamais ce bleu-là.
    hue = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)[:, :, 0].astype(np.int32)
    frag = ((hue > 100) & (hue < 132) & (ss > 130) & (vv < 150)).astype(np.uint8) * 255
    frag = cv2.bitwise_and(frag, cv2.bitwise_not(cv2.bitwise_or(headm, micm)))
    frag = cv2.bitwise_and(frag, alpha)
    near2 = cv2.dilate((alpha < 40).astype(np.uint8) * 255, np.ones((15, 15), np.uint8))
    frag = cv2.bitwise_and(frag, near2)
    frag = cv2.morphologyEx(frag, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(frag, 8)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 6000:
            continue
        sel = cv2.dilate((lab == i).astype(np.uint8) * 255, np.ones((5, 5), np.uint8)) > 0
        alpha[sel] = 0

    # 4bis. fuites résiduelles : blanc pur (V>228, S<26) en contact avec la transparence.
    #       C'est le mur qui reste collé à l'épaule et à la branche des lunettes après la
    #       première passe. Le verre teinté des verres, lui, ne tombe jamais dans ce seuil.
    pure = (((vv > 228) & (ss < 26)) | ((vv > 200) & (ss < 10))).astype(np.uint8) * 255
    pure = cv2.bitwise_and(pure, cv2.bitwise_not(micm))
    near = cv2.dilate((alpha < 40).astype(np.uint8) * 255, np.ones((13, 13), np.uint8))
    trial = cv2.bitwise_and(cv2.bitwise_and(pure, near), alpha)
    alpha = cv2.bitwise_and(alpha, cv2.bitwise_not(trial))

    # 5. un seul pixel retiré : le liseré studio part, la silhouette reste intacte.
    alpha = cv2.erode(alpha, np.ones((3, 3), np.uint8))
    alpha = cv2.bitwise_or(alpha, cv2.bitwise_and(micm, alpha))

    # 6. décontamination : seuls les pixels clairs du bord prennent la couleur du sujet
    img = bgr.astype(np.float32).copy()
    mask = (alpha > 127)
    for _ in range(8):
        acc = np.zeros_like(img)
        cnt = np.zeros((H, W, 1), np.float32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            sm = np.roll(np.roll(img, dy, 0), dx, 1)
            mk = np.roll(np.roll(mask, dy, 0), dx, 1)
            acc += sm * mk[:, :, None]
            cnt += mk[:, :, None]
        ok = (~mask) & (cnt[:, :, 0] > 0)
        img[ok] = acc[ok] / cnt[ok]
        mask = mask | ok
    rim = cv2.dilate(cv2.subtract(alpha, cv2.erode(alpha, np.ones((9, 9), np.uint8))),
                     np.ones((5, 5), np.uint8))
    bh = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    bright = ((bh[:, :, 2] > 165) & (bh[:, :, 1] < 60)).astype(np.uint8) * 255
    spill = cv2.bitwise_and(bright, rim)
    k = cv2.GaussianBlur((spill > 0).astype(np.float32), (0, 0), 1.2)[:, :, None]
    bgr = (bgr.astype(np.float32) * (1 - k) + img * k).astype(np.uint8)

    # 7. fuites de studio : un pixel de la couleur EXACTE du mur, collé à la transparence,
    #    est du mur. Le verre des lunettes est teinté, il n'est jamais blanc pur — c'est ce
    #    qui distingue le fond qu'on voit à travers la monture d'un vrai reflet.
    ref = np.median(bgr[studio > 0].reshape(-1, 3), axis=0) if (studio > 0).any() else None
    if ref is not None:
        d = np.linalg.norm(bgr.astype(np.float32) - ref[None, None, :], axis=2)
        pure = ((d < 24) & (vv > 240)).astype(np.uint8) * 255
        pure = cv2.bitwise_and(pure, cv2.bitwise_not(micm))
        near = cv2.dilate((alpha < 40).astype(np.uint8) * 255, np.ones((9, 9), np.uint8))
        n, lab, st, _ = cv2.connectedComponentsWithStats(pure, 8)
        leak = np.zeros((H, W), np.uint8)
        for i in range(1, n):
            if st[i, cv2.CC_STAT_AREA] > 12000:
                continue
            sel = (lab == i)
            if (near[sel] > 0).any():
                leak[sel] = 255
        alpha = cv2.bitwise_and(alpha, cv2.bitwise_not(leak))

    # 8. contour lissé : le grabCut laisse une dentelure sur le bord de la chemise (le
    #    vichy se confond avec l'écran sombre). On ferme, on ouvre, puis un flou + seuil
    #    arrondit la dentelure SANS déplacer la silhouette. Enfin 1 px de dégradé pour
    #    l'antialias.
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, k)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, k)
    a = cv2.GaussianBlur(alpha.astype(np.float32), (0, 0), 4.0)
    alpha = ((a > 127.5) * 255).astype(np.uint8)
    alpha = cv2.GaussianBlur(alpha, (0, 0), 0.9)
    return bgr, alpha


SEEDS_FG = [(0.02, 0.33, 0.33, 0.63), (0.33, 0.95, 0.23, 0.60), (0.60, 0.85, 0.50, 0.62),
            (0.72, 0.82, 0.71, 0.79), (0.55, 0.72, 0.63, 0.70)]
SEEDS_BG = [(0.00, 0.02, 0.00, 1.00), (0.00, 1.00, 0.00, 0.18), (0.44, 0.56, 0.80, 0.97),
            (0.60, 0.66, 0.72, 0.90), (0.00, 0.30, 0.68, 0.99), (0.86, 1.00, 0.80, 1.00),
            (0.02, 0.10, 0.66, 0.76)]


def main(src, dst, box=None, crop=None, work_w=1400):
    img = cv2.imread(src)
    if box:
        l, t, r, b = box
        h, w = img.shape[:2]
        img = img[int(h * t):int(h * b), int(w * l):int(w * r)]
    if crop:
        l, t, r, b = crop
        h, w = img.shape[:2]
        img = img[int(h * t):int(h * b), int(w * l):int(w * r)]
    H0, W0 = img.shape[:2]
    sc = work_w / W0
    img = cv2.resize(img, (int(W0 * sc), int(H0 * sc)), interpolation=cv2.INTER_AREA)

    alpha = grabcut_alpha(img, SEEDS_FG, SEEDS_BG)
    headm, micm, hsv = protect_zones(img)
    bgr, alpha = clean(img, alpha, headm, micm, hsv[:, :, 2], hsv[:, :, 1])

    rgba = np.dstack([bgr, alpha])
    ys, xs = np.where(alpha > 8)
    rgba = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    cv2.imwrite(dst, rgba)
    print("détouré", dst, rgba.shape[1], "×", rgba.shape[0])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--box")
    ap.add_argument("--crop")
    ap.add_argument("--work", type=int, default=1400)
    a = ap.parse_args()
    parse = lambda s: tuple(float(v) for v in s.split(",")) if s else None
    main(a.src, a.dst, parse(a.box), parse(a.crop), a.work)
