#!/usr/bin/env python3
"""Détourage de `_DSC3458` — AP Enock debout, micro en main, **pupitre conservé**.

Deux consignes tenues à la lettre :

* **on ne rogne pas le prédicateur** : tête, deux épaules, deux bras, deux mains, cinq doigts,
  micro et montre sont entiers. Sa tunique descend jusqu'au bord bas de la photo : le détourage
  non plus ne s'arrête pas en travers du torse ;
* **la barre du pupitre reste** (après la v1 qui coupait le corps à sa hauteur) — barre laquée,
  panneau de verre suspendu, Bible ouverte. L'écran de rediffusion, lui, s'en va.

Aucune IA générative sur le visage ou le corps : le masque sort de mesures de couleur et de
remplissages géométriques.

Méthode (v2). La v1 décrivait le **sujet** par familles de couleur (peau / tunique / cheveux) :
ces familles se recouvrent dans cette photo — le cuir chevelu éclairé a la teinte du mur clair,
la tunique celle de la bannière — d'où les encoches dans le crâne et la marche sur la joue.
La v2 décrit le **fond**, puis prend le complément :

1. fond = deux familles mesurées, et **jamais** le bleu sombre (V < 118) : c'est la tunique.
   mur clair : S ≤ 80 & V ≥ 118 · bannière / écran bleu moyen : H 88-126, S ≥ 15, V ≥ 120 ;
2. remplissage depuis les quatre bords : le fond atteignable de l'extérieur est marqué, le reste
   est le sujet. Le liseré clair de la tunique et les verres des lunettes, enfermés par la
   silhouette, restent donc dedans ;
3. le pupitre est ré-injecté à la géométrie mesurée (barre, panneau de verre, Bible) : il est
   couleur de fond, le remplissage l'aurait mangé ;
4. l'écran de rediffusion est retiré par couleur dans son cadre mesuré ;
5. échardes < 0,05 % de la surface supprimées ; bord : 1 px d'érosion puis adoucissement,
   pour ne pas laisser de frange bleue sur la peau.

Usage :
    python scripts/cutout_ap_3458.py <photo> <sortie.png> [--apercu apercu.jpg]
"""

from __future__ import annotations

import argparse
import sys

import cv2
import numpy as np
from PIL import Image

# --------------------------------------------------------------------------------------
# Repères mesurés sur la photo (5906 × 3937)
# --------------------------------------------------------------------------------------
#: écran de rediffusion « IMPACT CENTRE » (à gauche du crâne) : cadre du retrait par couleur
ECRAN = (2120, 1280, 2790, 2210)

#: barre laquée du pupitre — polygone relevé sur la photo, bout arrondi à gauche (x ≈ 2790)
#: relevé colonne par colonne sur la photo (arête neutre sombre, V < 112) : le dessus de la barre
#: monte de 3378 à 3326 puis redescend, le dessous court de 3420 à 3400
BARRE = [(2790, 3386), (2900, 3378), (3400, 3370), (3600, 3364), (3900, 3326),
         (4300, 3331), (4500, 3351), (4640, 3343), (4640, 3418), (4500, 3410),
         (4400, 3399), (4000, 3404), (3600, 3410), (2900, 3419), (2790, 3420)]

#: panneau de verre suspendu : arête gauche inclinée, débordant sur le bas de la photo
VERRE = [(3796, 3305), (4638, 3305), (4638, 3937), (3930, 3937), (3796, 3430)]

#: Bible ouverte posée sur la barre (pages crème : le remplissage les prendrait pour du mur)
BIBLE = (3975, 3250, 4640, 3350)

#: micro tenu par AP : capsule, cylindre et bague — protégé du retrait des structures fines
MICRO = [(2395, 1930), (2560, 1950), (2565, 2100), (2560, 2300), (2545, 2505),
         (2440, 2515), (2378, 2405), (2385, 2200), (2390, 2050)]

#: zone du micro et de l'attache bleue, réservée au corps
MICRO_ZONE = [(2370, 1920), (2700, 1920), (2700, 2560), (2370, 2560)]

#: pied de micro qui passe derrière l'épaule gauche : ni le prédicateur ni le pupitre
PIED_MICRO = [(1990, 1995), (2200, 2010), (2380, 2000), (2420, 1955), (2430, 1900),
              (2400, 1880), (2200, 1945), (2000, 1990), (1975, 2020), (1990, 2030)]

#: fenêtre de la tête : protégée du retrait des structures fines (les cheveux rasés sont fins)
FENETRE_TETE = (2230, 1300, 3010, 2150)

#: amorce du sujet : la joue
SEED = (2500, 1600)


def familles(hsv):
    """Les deux familles de fond mesurées — jamais le bleu sombre de la tunique."""
    h = hsv[:, :, 0].astype(np.int16)
    s = hsv[:, :, 1].astype(np.int16)
    v = hsv[:, :, 2].astype(np.int16)
    # Le mur clair garde la teinte bleue du lieu (H ≈ 100, S 12-63) : la condition de teinte est
    # indispensable, sinon les reflets du front et de la pommette (H ≈ 2, S 57, V 153) passent pour
    # du mur et percent le visage.
    mur = (h >= 85) & (h <= 132) & (s <= 80) & (v >= 118)
    bleu_moyen = (h >= 88) & (h <= 126) & (s >= 15) & (v >= 120)
    return (mur | bleu_moyen).astype(np.uint8)


def remplir(bgpix: np.ndarray) -> np.ndarray:
    """Marque le fond atteignable depuis les quatre bords de l'image."""
    m = bgpix.copy()
    h, w = m.shape
    ff = np.zeros((h + 2, w + 2), np.uint8)
    for x in range(0, w, 2):
        for y in (0, h - 1):
            if m[y, x] == 1:
                cv2.floodFill(m, ff, (x, y), 2)
    for y in range(0, h, 2):
        for x in (0, w - 1):
            if m[y, x] == 1:
                cv2.floodFill(m, ff, (x, y), 2)
    return (m == 2).astype(np.uint8)


def poly(shape, pts, e=1.0):
    m = np.zeros(shape, np.uint8)
    cv2.fillPoly(m, [np.array([[int(x * e), int(y * e)] for x, y in pts], np.int32)], 1)
    return m


def pupitre(shape, e):
    """Barre + verre + Bible, à la géométrie mesurée."""
    return poly(shape, BARRE, e) | poly(shape, VERRE, e) | bible(shape, e)


def bible(shape, e):
    m = np.zeros(shape, np.uint8)
    x0, y0, x1, y1 = BIBLE
    m[int(y0 * e):int(y1 * e), int(x0 * e):int(x1 * e)] = 1
    return m


def corps_mesure(hsv):
    """Peau et tunique : ce qui ne doit jamais être pris pour du décor."""
    h = hsv[:, :, 0].astype(np.int16)
    s = hsv[:, :, 1].astype(np.int16)
    v = hsv[:, :, 2].astype(np.int16)
    # Peau et lèvres mesurées : H 4-18, S 86-165. Deux voisins trompeurs, écartés par les bornes :
    # le lettrage magenta de la bannière (H 149-165), et le lettrage jaune (H 24-30, S 219-255 —
    # une saturation qu'aucune peau de cette photo n'atteint).
    peau = (h <= 20) & (s >= 45) & (s <= 195) & (v >= 35)
    tunique = (h >= 92) & (h <= 135) & (s >= 90) & (v <= 140)
    return (peau | tunique).astype(np.uint8)


def detourer(im, e=0.5):
    H, W = im.shape[:2]
    sm = cv2.resize(im, None, fx=e, fy=e, interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
    hh = hsv[:, :, 0].astype(np.int16)
    ss = hsv[:, :, 1].astype(np.int16)
    vv = hsv[:, :, 2].astype(np.int16)

    # 1 — remplissage de fond, **avant** tout ajout du pupitre : sinon la barre referme une poche
    # au-dessus d'elle où le lettrage de la bannière restait collé à la silhouette.
    fond = remplir(familles(hsv))
    sujet = (1 - fond).astype(np.uint8)
    pup = pupitre(sujet.shape, e)

    # 2 — écran de rediffusion : tout l'écran, pas seulement le haut de son cadre
    ex0, ey0, ex1, ey1 = [int(v * e) for v in ECRAN]
    ecran = ((hh >= 86) & (hh <= 132) & (ss >= 55) & (ss <= 175) & (vv >= 105) & (vv <= 228))
    zone = np.zeros(sujet.shape, bool)
    zone[ey0:ey1, ex0:ex1] = True
    # le bâton lumineux vert posé sur le pupitre de l'écran : teinte et saturation mesurées
    zone[int(2090 * e):int(2190 * e), int(2490 * e):int(2570 * e)] = True
    baton = (hh >= 95) & (hh <= 118) & (ss >= 190) & (vv <= 135)
    decor = (ecran & zone) | (baton & zone)

    # 3 — décor retiré partout **sauf** dans le corps mesuré (peau + tunique) : le lettrage
    # magenta de la bannière, son bleu d'aplat et les restes de l'écran ne peuvent pas survivre,
    # et le verre du pupitre (même bleu que la tunique) est protégé.
    banniere = (hh >= 92) & (hh <= 122) & (ss >= 105) & (vv >= 128)
    lettrage = (((hh >= 140) & (hh <= 178)) | ((hh >= 24) & (hh <= 45))) & (ss >= 130) & (vv >= 145)
    corps_net = corps_mesure(hsv)
    corps = cv2.dilate(corps_net, np.ones((13, 13), np.uint8))
    # réserve plus étroite pour la règle de décor : entre le bras et le torse, le lettrage de la
    # bannière affleure dans des fentes de quelques pixels — une dilatation de 13 px les couvrait
    # et les taches magenta restaient collées au poignet.
    corps_fin = cv2.dilate(corps_net, np.ones((5, 5), np.uint8))
    # le micro et son attache bleue restent protégés même par la réserve étroite : leur bleu
    # (H 100, S 255, V 250) est exactement celui de la bannière.
    protege_micro = cv2.dilate(poly(sujet.shape, MICRO, e), np.ones((15, 15), np.uint8)) \
        | poly(sujet.shape, MICRO_ZONE, e)
    corps_fin = (corps_fin.astype(bool) | (protege_micro > 0)).astype(np.uint8)
    # le micro tenu par AP est protégé : son corps aluminium prend des reflets chauds (H 20-40)
    # que la règle du lettrage prendrait pour du jaune de bannière.
    # Toute la zone du micro, attaches bleues comprises : le ruban adhésif bleu du micro a la
    # teinte de la bannière (H 98-105, S 255, V 250) — sans cette réserve, le fond le traversait
    # et laissait un trou dans l'instrument.
    corps |= cv2.dilate(poly(sujet.shape, MICRO, e), np.ones((15, 15), np.uint8))
    corps |= poly(sujet.shape, MICRO_ZONE, e)
    decor |= (banniere | lettrage) & (corps_fin == 0)
    # le pied de micro qui traverse la scène (tige gris-bleu, anneau vert) n'est ni AP ni le
    # pupitre : il est retiré à sa géométrie, sinon il traverse la silhouette de l'épaule.
    decor = decor | ((poly(sujet.shape, PIED_MICRO, e) > 0) & (corps_fin == 0))
    # toute la règle est bornée par le corps mesuré : le halo de l'écran qui effleure le crâne
    # ne doit pas manger la ligne de cheveux.
    decor &= (corps_fin == 0)
    sujet = (sujet & (1 - decor.astype(np.uint8))).astype(np.uint8)

    # 4 — la silhouette qui contient l'amorce (la joue)
    n, lab = cv2.connectedComponents(sujet, 8)
    amorce = lab[int(SEED[1] * e), int(SEED[0] * e)]
    suj = (lab == amorce).astype(np.uint8)

    # 5 — trous intérieurs rebouchés (verres, liseré de la tunique, reflets) — mais **pas** les
    # pixels de décor qu'on vient de retirer : sans cette réserve, le rebouchage les remettait
    # aussitôt (c'est ainsi que le lettrage de la bannière revenait dans les poches fermées,
    # entre le bras, la barre et le bord de la silhouette).
    sil = suj.copy()                      # silhouette du corps, avant le pupitre
    vide = (1 - suj).astype(np.uint8)
    cv2.floodFill(vide, np.zeros((vide.shape[0] + 2, vide.shape[1] + 2), np.uint8), (0, 0), 2)
    trous = (vide == 0) & (decor == 0)
    suj |= trous.astype(np.uint8)

    # 6 — structures fines : câbles et longerons passent par-dessus le remplissage parce qu'ils
    # sont sombres. Une ouverture de 25 px les retire ; le micro d'AP est protégé (c'est un volume).
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    fins = (suj & (1 - cv2.morphologyEx(suj, cv2.MORPH_OPEN, k))).astype(np.uint8)
    protege = cv2.dilate(poly(suj.shape, MICRO, e), np.ones((25, 25), np.uint8))
    protege[int(FENETRE_TETE[1] * e):int(FENETRE_TETE[3] * e),
            int(FENETRE_TETE[0] * e):int(FENETRE_TETE[2] * e)] = 1
    suj = (suj & (1 - (fins & (1 - protege)))).astype(np.uint8)
    # le fil noir du plafonnier qui pend au-dessus du crâne : un trait d'une vingtaine de pixels
    # qui a survécu à l'ouverture (il est large à la base). Il ne touche pas la silhouette ;
    # retiré dans la bande haute, sans risque pour les cheveux protégés par FENETRE_TETE.
    suj[:int(1300 * e), :] = 0

    # 7 — composantes : on ne garde que ce qui tient au corps ou au pupitre. Un fragment de
    # bannière détaché (lettrage jaune au-dessus de la barre) passait le seuil de surface et
    # restait flotter dans le vide : il ne recouvre ni la silhouette ni le pupitre, il tombe.
    n, lab, st, _ = cv2.connectedComponentsWithStats(suj, 8)
    ancre = (sil | pup).astype(bool)
    seuil = 0.0005 * st[1:, 4].sum()
    garde = []
    for i in range(1, n):
        aire = st[i, cv2.CC_STAT_AREA]
        part_ancree = ancre[lab == i].mean() if aire else 0.0
        if part_ancree >= 0.5 or (aire >= seuil and part_ancree > 0.0):
            garde.append(i)
    suj = np.isin(lab, garde).astype(np.uint8)

    # 8 — le pupitre est reposé en dernier : barre, verre, Bible, tels quels
    suj |= pup

    # 8bis — la bannière passe juste derrière le pupitre et sa barre laquée est un miroir qui
    # laisse voir son aplat et son lettrage (« …NOSIS) de Dieu »). Tout ce qui est **au-dessus**
    # de l'arête mesurée de la barre, entre la manche et le bord droit, est du fond : on le perce.
    # Sur la face de la barre, seules les lettres sont retirées, par leur couleur (bannière ou
    # lettrage) — le miroir, lui, garde ses reflets sombres.
    arase = {}
    poly_barre = poly(suj.shape, BARRE, e)
    for x in range(suj.shape[1]):
        col = np.where(poly_barre[:, x])[0]
        if col.size:
            arase[x] = col[0]
    # pages de la Bible : crème, chaudes et claires (mesurées H 12-45, S 45-100, V 150-250)
    creme = (hh >= 10) & (hh <= 55) & (ss >= 45) & (ss <= 110) & (vv >= 145)
    lettres = lettrage | banniere
    for x in range(int(3560 * e), min(int(4660 * e), suj.shape[1])):
        haut = arase.get(x, int(3330 * e))
        # à droite de x = 3800, la manche est finie : la réserve « corps » n'y protège plus rien
        libre = lambda y: corps[y, x] == 0 or x > int(3800 * e)
        # les pages de la Bible reposent sur la barre : on garde leur épaisseur (≈ 34 px au-dessus
        # de l'arête) et, au-delà, les seules taches crème. Le reste est du fond.
        epaisseur = int(34 * e) if x >= int(3850 * e) else 0
        for y in range(int(3180 * e), min(haut, suj.shape[0])):
            if libre(y) and not creme[y, x] and y < haut - epaisseur:
                suj[y, x] = 0
        for y in range(haut, min(int(3416 * e), suj.shape[0])):
            if lettres[y, x] and libre(y):
                suj[y, x] = 0
    # au-dessus de la barre, à droite du corps : de la bannière seule, rien d'autre.
    vide = np.zeros(suj.shape, bool)
    vide[int(3120 * e):int(3272 * e), int(3880 * e):int(4670 * e)] = True
    suj = (suj & (1 - vide.astype(np.uint8))).astype(np.uint8)

    # 8quater — franges du décor restées **opaques** sur les bords, après l'adoucissement :
    # le lettrage magenta et jaune de la bannière affleure sur le bord de la manche et près de
    # la Bible. Retirés par couleur, uniquement sur les pixels de bord (7 px), et seulement
    # s'ils sont vifs : la peau (H 4-18, S ≤ 165) et la tunique (V ≤ 140) ne sont jamais dans
    # ces plages. L'alpha seul change ; aucune couleur n'est repeinte.
    bord = suj & (1 - cv2.erode(suj, np.ones((15, 15), np.uint8)))
    vif = (((hh >= 138) & (hh <= 180)) | ((hh >= 20) & (hh <= 50))) & (ss >= 110) & (vv >= 120)
    suj = (suj & (1 - (bord & vif).astype(np.uint8))).astype(np.uint8)

    # 8ter — le pied de micro qui traverse le plan (tige sombre, anneau vert) n'appartient ni au
    # prédicateur ni au pupitre : il est retiré en dernier, à sa géométrie, sans toucher la peau
    # ni la tunique mesurées.
    suj = (suj & (1 - (poly(suj.shape, PIED_MICRO, e) > 0).astype(np.uint8))).astype(np.uint8)

    # 9 — contours adoucis
    a = cv2.medianBlur(suj * 255, 5)
    a = cv2.GaussianBlur(a, (0, 0), 1.0)
    a = np.where(a > 118, 255, np.clip((a.astype(np.int16) - 46) * 2.2, 0, 255)).astype(np.uint8)
    alpha = cv2.resize(a, (W, H), interpolation=cv2.INTER_LINEAR)
    alpha[alpha < 14] = 0
    return alpha


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("photo")
    ap.add_argument("sortie")
    ap.add_argument("--apercu", default=None)
    a = ap.parse_args()

    im = cv2.imread(a.photo)
    if im is None:
        print(f"photo illisible : {a.photo}", file=sys.stderr)
        return 1
    H, W = im.shape[:2]
    print(f"photo {W} x {H}")

    alpha = detourer(im)

    bx, by, bw, bh = cv2.boundingRect((alpha > 8).astype(np.uint8))
    print(f"boîte du sujet : ({bx},{by}) → ({bx + bw},{by + bh})  = {bw} x {bh}")

    rgba = cv2.cvtColor(im, cv2.COLOR_BGR2RGBA)
    rgba[:, :, 3] = alpha
    pil = Image.fromarray(rgba).crop((bx, by, bx + bw, by + bh))

    # frange : couleur prise à l'intérieur du sujet, alpha du pixel inchangé
    arr = np.asarray(pil).astype(np.float32)
    al = arr[:, :, 3] / 255.0
    connu = (al >= 0.985).astype(np.float32)
    front = ((al > 0) & (al < 0.985)).astype(np.float32)
    coul = arr[:, :, :3] * connu[..., None]
    for _ in range(14):
        cb, mb = cv2.blur(coul, (5, 5)), cv2.blur(connu, (5, 5))
        dispo = (mb > 1e-4) & (front > 0)
        if not dispo.any():
            break
        coul[dispo] = cb[dispo] / mb[dispo][:, None]
        connu[dispo] = 1.0
        front[dispo] = 0.0
    arr[:, :, :3] = coul
    out = Image.fromarray(np.dstack([np.clip(arr[:, :, :3], 0, 255),
                                     arr[:, :, 3]]).astype(np.uint8), "RGBA")
    out.save(a.sortie)
    print(f"écrit {a.sortie} · {out.width}×{out.height} · opaque {100 * (al > 0.5).mean():.1f} %")

    if a.apercu:
        plateau = Image.new("RGBA", out.size, (233, 32, 176, 255))
        plateau.alpha_composite(out)
        plateau.convert("RGB").resize((760, round(760 * out.height / out.width)),
                                      Image.LANCZOS).save(a.apercu, quality=93)
        print("aperçu", a.apercu)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
