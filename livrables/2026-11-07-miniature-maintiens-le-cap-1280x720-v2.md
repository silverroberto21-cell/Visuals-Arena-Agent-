# Note de livraison — miniature « Maintiens le CAP » **v2, sans photo**

- **Fichier** : [`2026-11-07-miniature-maintiens-le-cap-1280x720-v2.jpg`](2026-11-07-miniature-maintiens-le-cap-1280x720-v2.jpg)
- **Format** : miniature 1280 × 720 (YouTube) · livrée le 2026-11-07 · **v2** (remplace la v1 dans le choix d'ICC Pahou)
- **Demande** : « Thème : Maintiens le CAP, sa Gloire se manifestera — Prédicateur : AP Enock MISSIMAHOU —
  Date : Dimanche 8 Novembre 2026 — Fond : f07 — **N'utilisez pas la photo de AP. C'est juste une
  image de fond avec le thème.** »
- Script : `scripts/render_cap_f07_texte.py`

## Ce qui change par rapport à la v1

| | v1 | **v2 (celle-ci)** |
|---|---|---|
| Photo de l'orateur | portrait en panneau à droite | **aucune photo, aucune silhouette, aucun détourage** |
| Structure | colonne de titre + portrait | **composition typographique seule**, deux colonnes : titre à gauche, date à droite |
| Date | « AUJOURD'HUI » (non fournie) | **DIMANCHE 8 NOVEMBRE 2026**, fournie par la demande |
| Motif | — | **rose des vents filaire** (écho au CAP, sans imager un bateau ni une scène) |
| Fond / palette / polices | inchangés | **inchangés** |

## Ce qui a été utilisé

| Élément | Choix |
|---|---|
| Fond | **FOND 7** → `fonds/f07-bleu-nuit-bokeh.jpg` (1377 × 736, recadré à 1280 × 720), assombri et légèrement accentué, bokeh conservé |
| Structure | affiche typographique : titre en deux lignes à gauche, rose des vents au centre-droit, bloc date aligné à droite en pied, prédicateur en pied à gauche |
| Typographie | **Anton** (titre, capitales condensées très grasses) + **Montserrat** SemiBold / Medium / Bold (signalétique) — duo du thème, `themes/maintiens-le-cap.md` |
| Palette | 60 % bleus mesurés sur f07 (`#0A398F` 22 %, `#0D56B1` 20 %, `#0B3AC8` 17 %, `#0D6FC5` 16 %, `#071C9B` 13 %, `#0D89D2` 12 %) · 30 % acier `#B0D6F6` · 10 % accent or pâle `#E8C87A` |
| Textes | recopiés exactement : « Maintiens le CAP, sa Gloire se manifestera » (titre + sous-titre), « AP Enock MISSIMAHOU », « Dimanche 8 Novembre 2026 », « ICC Pahou » |

## Hiérarchie et lisibilité

1. **MAINTIENS / LE CAP** — 152 px et 190 px de corps, `CAP` en or : le mot d'accroche tient
   même à 360 px de large (vérifié en réduction).
2. **sa Gloire se manifestera** — une seule ligne, `Gloire` en or (l'accent du thème).
3. **DIMANCHE 8 NOVEMBRE 2026** — bloc aligné à droite sous un filet or.
4. **PRÉDICATEUR / AP Enock MISSIMAHOU** — en pied à gauche, casse du nom respectée.

## Écarts assumés

- **Aucune photo** : demandé explicitement. Le visuel est donc porté par le fond et la
  typographie ; aucun espace n'est laissé vide comme s'il attendait un portrait.
- **Pas d'élément d'interface** (badge de durée, coins arrondis, chrome YouTube) : non reproduit.
- **Heure, lieu, contacts** non fournis : non inventés, non affichés.

## En attente

Rien de bloquant. Si l'heure et le lieu arrivent, ils se posent sous le bloc date, même colonne.
