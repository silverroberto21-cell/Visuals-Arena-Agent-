# Note de livraison — flyer « Les Bonnes nouvelles du royaume »

- **Fichiers** :
  - [`2026-11-07-flyer-les-bonnes-nouvelles-du-royaume-1080x1350.jpg`](2026-11-07-flyer-les-bonnes-nouvelles-du-royaume-1080x1350.jpg) — flyer numérique 1080 × 1350 (4:5)
  - [`2026-11-07-flyer-les-bonnes-nouvelles-du-royaume-a5-1748x2480.jpg`](2026-11-07-flyer-les-bonnes-nouvelles-du-royaume-a5-1748x2480.jpg) — A5 print 1748 × 2480 @ 300 dpi
- **Livré le** : 2026-11-07 · script `scripts/render_bonnes_nouvelles_f13.py`
- **Demande** : « Un flyer avec le texte “Les Bonnes nouvelles du royaume” avec le fond f13
  uniquement, change de police, la date est négligeable. »

## Choix retenus

| Élément | Choix |
|---|---|
| Fond | **FOND 13 uniquement** → `fonds/f13-bleu-nuit-vagues.jpg`, **aucune image ajoutée** — pas de photo, pas de motif, pas de texture : seuls voiles de lisibilité et lumière |
| Palette | 60 % bleus mesurés sur f13 (`#0155FB` 22 %, `#012AE0` 21 %, `#011BD0` 16 %, `#0136E9` 15 %, `#0182FE` 25 %) · 30 % blanc bleuté `#F7FAFE` · 10 % or pâle `#F0CD82` |
| Typographie | **changement demandé** : **Cormorant Garamond** (titre) + **Jost** (marque) — nouveau duo, ni Anton (Maintiens le CAP) ni Playfair (Atmosphère de prière) — fiche : `themes/les-bonnes-nouvelles-du-royaume.md` |
| Texte | « **Les Bonnes nouvelles du royaume** » seul, composé en trois lignes : deux corps, le mot « royaume » plus petit pour tenir la colonne |
| Marque | « ICC PAHOU » en haut, sous l'équerre gauche |
| Pied | filet or seul — **aucune date, aucune heure, aucun lieu inventés** |

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
