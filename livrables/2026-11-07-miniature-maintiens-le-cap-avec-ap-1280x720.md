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

## Traitement du sujet — recadrage + lumière uniquement

- Détourage sur la photo d'origine (5991 × 3994), pas de retouche du visage, de la tenue ni des
  proportions : recadrage du cadre studio noir, détourage, relève des tons moyens, très léger voile
  acier pour l'accord d'ambiance.
- Le contour a été **rongé puis adouci** et un anti-débordement a été appliqué : plus aucun liseré
  blanc du studio sur le bord.
- Fondu du bord gauche (le sujet sort du fond), fondu bas (le buste se dissout — pas de coupe au
  ras du cadre), ombre portée douce pour l'asseoir sur le bokeh.

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

Rien de bloquant. **Archivage de la photo** proposé (pas fait) : `orateurs/missimahou-enock.jpg`,
pour ne plus te la redemander — dis-moi si tu veux que je l'enregistre.
