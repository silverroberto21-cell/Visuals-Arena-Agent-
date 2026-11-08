# Note de livraison — flyer « Les Bonnes nouvelles du royaume »

- **Fichiers** :
  - [`2026-11-07-flyer-les-bonnes-nouvelles-du-royaume-1920x1080-paysage.jpg`](2026-11-07-flyer-les-bonnes-nouvelles-du-royaume-1920x1080-paysage.jpg) — **version paysage 16:9, retenue** (écran, projection, bannière)
  - [`2026-11-07-flyer-les-bonnes-nouvelles-du-royaume-a5-paysage-2480x1748.jpg`](2026-11-07-flyer-les-bonnes-nouvelles-du-royaume-a5-paysage-2480x1748.jpg) — A5 paysage print 2480 × 1748 @ 300 dpi
  - [`2026-11-07-flyer-les-bonnes-nouvelles-du-royaume-1080x1350.jpg`](2026-11-07-flyer-les-bonnes-nouvelles-du-royaume-1080x1350.jpg) — portrait 4:5 (première version, conservée)
  - [`2026-11-07-flyer-les-bonnes-nouvelles-du-royaume-a5-1748x2480.jpg`](2026-11-07-flyer-les-bonnes-nouvelles-du-royaume-a5-1748x2480.jpg) — A5 portrait @ 300 dpi (première version, conservée)
- **Livré le** : 2026-11-07 · script `scripts/render_bonnes_nouvelles_f13.py`
- **Demande** : « Un flyer avec le texte “Les Bonnes nouvelles du royaume” avec le fond f13
  uniquement, change de police, la date est négligeable. »

## Choix retenus

| Élément | Choix |
|---|---|
| Fond | **FOND 13 uniquement** → `fonds/f13-bleu-nuit-vagues.jpg`, **aucune image ajoutée** — pas de photo, pas de motif, pas de texture : seuls voiles de lisibilité et lumière |
| Palette | 60 % bleus mesurés sur f13 (`#0155FB` 22 %, `#012AE0` 21 %, `#011BD0` 16 %, `#0136E9` 15 %, `#0182FE` 25 %) · 30 % blanc bleuté `#F7FAFE` · 10 % or pâle `#F0CD82` |
| Typographie | **changement demandé** : **Cormorant Garamond** (titre) + **Jost** (marque) — nouveau duo, ni Anton (Maintiens le CAP) ni Playfair (Atmosphère de prière) — fiche : `themes/les-bonnes-nouvelles-du-royaume.md` |
| Texte | « **Les Bonnes nouvelles du royaume** » seul, deux corps. Portrait : trois lignes (Les Bonnes / nouvelles / du royaume). **Paysage : deux lignes** (Les Bonnes nouvelles / du royaume) pour garder la même masse optique sans écraser la hauteur |
| Marque | « ICC PAHOU » en haut, sous l'équerre gauche |
| Pied | filet or seul — **aucune date, aucune heure, aucun lieu inventés** |

## Version paysage (2026-11-07, demande « je le veux en mode paysage »)

- Même fond, même palette, même duo de polices, mêmes marges proportionnelles : **seule la
  disposition change**. Le fond n'est pas pivoté, il est **recadré** dans le 16:9 (fond abstrait,
  aucun sens naturel perdu — `specs/formats.md` §3bis).
- Titre sur **deux lignes** (188 px / 113 px en 1920 × 1080), centré, filet or et équerres à la
  même place relative que la version portrait.
- Aucune date, aucun texte ajouté : le pied reste un filet.

## Écarts assumés

- **Date non composée** : le commanditaire la juge négligeable. Je n'écris pas « date à confirmer »
  à sa place, je ne laisse pas non plus un trou visible : le pied est simplement un filet.
- **Aucune photo d'orateur** : la demande ne mentionne ni orateur ni photo, et le fond devait
  rester seul en scène.
- **Deux dimensions pour un même rendu** : le flyer existe en 4:5 numérique (usage story/feed) et
  en A5 print 300 dpi, mis à l'échelle depuis la même maquette (facteur `k`), pour éviter deux
  compositions divergentes.
- **Fond agrandi** : f13 est un 734 × 402 — agrandi à 1080 × 1350 puis à 1748 × 2480. En A5 print
  l'agrandissement est visible de près ; pour un tirage exigeant, fournir un f13 plus grand.

## En attente

Rien de bloquant. Si une date, un lieu ou un orateur doivent finalement figurer, ils se posent en
pied, sous le filet or, sans toucher au titre.
