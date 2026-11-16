# Note de livraison — miniature « Maintiens le CAP » avec l'orateur (AP)

- **Fichier** : [`2026-11-07-miniature-maintiens-le-cap-avec-ap-1280x720.jpg`](2026-11-07-miniature-maintiens-le-cap-avec-ap-1280x720.jpg)
- **Format** : miniature 1280 × 720 (YouTube) · livrée le 2026-11-07
- **Demande** : « Prends le flyer du thème (sans les points) et tu y incorpores AP de cette photo.
  Garde le même fond. » — photo fournie : `_MG_2958.jpg`
- Script : `scripts/render_cap_f07_ap.py`

## Ce qui a été utilisé

| Élément | Choix |
|---|---|
| Fond | **FOND 7** → `fonds/f07-bleu-nuit-bokeh.jpg` — **inchangé**, même traitement que le flyer du thème (assombrissement, voile, lueur) |
| Palette | 60 % bleus mesurés sur f07 · 30 % acier `#B0D6F6` · 10 % or pâle `#E8C87A` — identique au flyer |
| Typographie | **Anton** (titre, 152 / 190 px) + **Montserrat** (signalétique) — duo du thème, identique |
| Textes du flyer | « MAINTIENS LE CAP », « sa **Gloire** se manifestera », « ICC PAHOU » — inchangés, sans les trois points |
| Ajout demandé | **orateur découpé** de la photo fournie, placé à droite |
| Infos reprises | « DIMANCHE 8 NOVEMBRE 2026 » et « AP Enock MISSIMAHOU », déplacés sous le titre dans la colonne de gauche (la colonne de droite appartient au sujet) |

## Traitement du sujet — détourage repris, bras restauré

Le détourage précédent **rongeait le bras** et laissait un bord mou. Il est refait, avec une règle
par étape (script reproductible : [`scripts/cutout_sujet.py`](../scripts/cutout_sujet.py)) :

| Étape | Règle |
|---|---|
| Prise | photo d'origine, recadrage du cadre, largeur de travail 1400 px |
| Séparation | `grabCut` 12 itérations, amorces premier plan / arrière-plan |
| Zones protégées | enveloppe convexe de la tête (verres des lunettes) + **rectangle plein du micro** — bornes mesurées à la grille sur la photo : x 0,435–0,548, y 0,475–0,868 |
| Mur du studio | clair **et** neutre **et relié au bord de l'image** — sans ce troisième critère, un front clair était percé |
| Trous | rebouchés **uniquement** à l'intérieur d'une zone protégée : ailleurs, une poche claire est le studio qu'on voit entre le bras et le buste |
| Fragments | mur blanc pur, écran bleu sombre coincé entre deux doigts : retirés seulement s'ils sont petits et collés à la transparence |
| Silhouette | **aucune érosion de la forme** : 1 px de liseré, puis contour lissé (fermeture + ouverture + flou/seuil) — le bras garde son contour réel |
| Couleur | décontamination du liseré studio par propagation depuis l'intérieur : plus de frange blanche sur l'épaule ni sur le bras |

Composition inchangée (`PANEL_W=500`, `TOP=30`, `RIGHT=34`, `BOTTOM_FADE=76`, ombre douce, fondu bas,
étalonnage identique). **Fond, textes, polices, couleurs et disposition sont ceux du visuel validé** :
seul le détourage du sujet a changé.

Le détourage est conservé dans le dépôt — [`orateurs/ap-enock-missimahou-detourage.png`](../orateurs/ap-enock-missimahou-detourage.png) —
pour que le visuel se re-rende à l'identique (`python3 scripts/render_cap_f07_ap.py <détourage> <sortie>`).

## Écarts assumés

- **La date et le prédicateur ont changé de place** : ils étaient en pied de part et d'autre sur le
  flyer ; ici le sujet occupe cette zone, donc ils remontent sous le titre, dans la même colonne
  que lui (une seule origine de lecture, cf. `specs/formats.md` §4).
- **Les trois points ne sont pas repris** : demandé ainsi (« le flyer du thème, sans les points »).
  Le récapitulatif des trois points reste un visuel séparé
  (`2026-11-07-recap-maintiens-le-cap-3-points-1280x720.jpg`).
- **Aucune couleur de la photo d'origine n'est reprise** dans la palette : elle est reconstruite
  depuis f07, comme le veut la doctrine du dépôt.

## En attente

Rien de bloquant. Le **détourage** est archivé ; la **photo d'origine** ne l'est toujours pas —
dis-moi si tu veux que je l'enregistre (`orateurs/missimahou-enock.jpg`).
