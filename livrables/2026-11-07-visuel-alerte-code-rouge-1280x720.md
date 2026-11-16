# Note de livraison — visuel « ALERTE CODE R.O.U.G.E » (les cinq clés)

- **Fichier** : [`2026-11-07-visuel-alerte-code-rouge-1280x720.jpg`](2026-11-07-visuel-alerte-code-rouge-1280x720.jpg)
- **Format** : 1280 × 720 (visuel de message, déclinable miniature) · livré le 2026-11-07
- **Demande** : rectification du thème — « ALERTE CODE R.O.U.G.E : les 5 clés pour vivre une
  chrétienne victorieuse » — appliquée au visuel qui porte l'acrostiche détaillé
- Script : `scripts/render_alerte_code_rouge.py visuel <sortie.jpg>`
- Fiche : [`themes/alerte-code-rouge.md`](../themes/alerte-code-rouge.md)

## Ce qui a été utilisé

| Élément | Choix |
|---|---|
| Modèle | **M01 · bleu nuit, titre coupé** + grille du visuel précédent (deux colonnes séparées d'un filet) |
| Fond | **FOND 6** → `fonds/f06-bleu-acier-texture.jpg`, assombri ×0,86, scrim vertical, halo cyan |
| Palette | bleus f06 + acier `#B0D6F6` + **ROUGE** `#DE2638` en accent — mesuré : **92,1 % de bleu**, 3,1 % de rouge |
| Typographie | **Anton** (accroche, mot-code, verbes-clés) + **Jost** (phrase, gloses, références) |
| Textes | le titre rectifié **et** les cinq clés recopiées à la lettre (verbe, glose, référence) — rien d'autre |

## Structure

- **Colonne de gauche** : `ICC PAHOU`, barre d'alerte + « ALERTE CODE », mot-code `R.O.U.G.E`,
  filet d'accent, « les 5 clés pour vivre / une chrétienne victorieuse », et en pied la légende
  « ACROSTICHE · CINQ CLÉS ».
- **Colonne de droite** : les cinq clés, une par rangée, séparées par un filet acier — **lettre
  rouge** + **verbe** en Anton + glose en acier + **référence biblique** alignée à droite.

| Lettre | Verbe | Glose | Référence |
|---|---|---|---|
| R | RECHERCHER | Continuellement la présence de Dieu. | Psaume 105:4 |
| O | OBÉIR | À la Parole de Dieu. | Josué 1:8 |
| U | UTILISER | Les armes spirituelles. | Éphésiens 6:11-18 |
| G | GARDER | Son cœur et sa foi. | Proverbes 4:23 |
| E | ENDURER | Jusqu'à la fin dans la foi. | Matthieu 24:13 |

- **Filet vertical** entre les deux colonnes ; aucun encadré, aucune icône, aucun élément d'interface.
- **Ponctuation des gloses conservée** (point final de chaque phrase fournie) ; accents vérifiés un
  par un (`Éphésiens`, `Josué`, `É` de `Éphésiens`, `œ` de `cœur`).

## Décisions assumées

- **« R.O.U.G.E » avec ses points**, comme la source : les points ne sont pas un ornement, ils font
  le « code ». Ils sont resserrés de 2 px pour que le mot reste un bloc lisible en vignette.
- **Le titre rectifié prend la place du titre précédent** : même hiérarchie (accroche → code →
  phrase), même duo, même palette. Aucune autre décision de composition n'est rouverte.
- **Le rouge reste un accent** : mot-code, lettres-clés, filets. Le bleu du fond garde la dominante
  mesurée à 92 %.
- **Aucune date, aucun lieu, aucun orateur** sur ce visuel : la source n'en donne pas.

## Outil IA

**Aucun outil génératif.** Texte et filets composés en couche de design (Pillow + polices du dépôt),
fond du dépôt réglé par courbes et voiles. Les modèles image ne sont pas installés ici ; le rendu est
rejouable en une commande.

## À vérifier

1. **La phrase de la source** : « les 5 clés pour vivre **une** chrétienne victorieuse ». Recopiée à
   la lettre, sans ajouter « vie ». Si l'omission est involontaire, une ligne à changer — je réédite
   les quatre sorties dans le même passage.
2. **Aucune date** fournie → non inventée ; elle se posera en pied de colonne droite quand elle
   arrivera.
3. Casse de « Dieu » dans les gloses : composée « Dieu » comme dans la demande, tandis que les verbes
   restent en capitales.
