# Index des modèles

> Références de style fournies par **Impact Centre Chrétien Pahou** le 2026-11-07.
> Un modèle documente une **structure, un traitement de titre et des effets** — pas une palette à
> recopier. Aperçu : [`planche.jpg`](planche.jpg).

**5 modèles** · **aucune couleur reprise** (la palette est reconstruite à chaque visuel) · 4 avec
éléments d'interface à ignorer.

## 1. Correspondance

| Tu dis | Fichier | Fiche |
|---|---|---|
| **Modèle 1** | `m01-bleu-nuit-titre-coupe.jpg` | [`m01-bleu-nuit-titre-coupe.md`](m01-bleu-nuit-titre-coupe.md) |
| **Modèle 2** | `m02-rayures-prisme.jpg` | [`m02-rayures-prisme.md`](m02-rayures-prisme.md) |
| **Modèle 3** | `m03-degrade-violet-prisme.jpg` | [`m03-degrade-violet-prisme.md`](m03-degrade-violet-prisme.md) |
| **Modèle 4** | `m04-violet-titre-geant.jpg` | [`m04-violet-titre-geant.md`](m04-violet-titre-geant.md) |
| **Modèle 5** | `m05-noir-brush-colore.jpg` | [`m05-noir-brush-colore.md`](m05-noir-brush-colore.md) |

## 2. Vue d'ensemble

| N° | Dimensions | Couleurs du modèle *(ignorées)* | Interface | Structure en une ligne | Effet signature |
|---|---|---|---|---|---|
| **m01** | 1280×720 | bleu 85 % *(ignorées)* | ❌ aucune | titre fer à gauche, portrait centre-droit, bande basse nom + date | typographie fantôme + alternance menthe/blanc par ligne |
| **m02** | 720×409 | rouge/chaud, 12 % bleu *(ignorées)* | ⚠️ badge + coins | portrait gauche, texte aligné droite, nom sur plaque | rayures prisme verticales |
| **m03** | 562×355 | bleu-violet, 61 % bleu *(ignorées)* | ⚠️ badge + coins | portrait gauche, titre centré à droite, logo vertical | traînées arc-en-ciel + éclat derrière le portrait |
| **m04** | 573×385 | violet *(ignorées)* | ⚠️ badge + coins | titre géant pleine largeur, portrait petit en bas | mot-clé 3× plus gros + sous-titre script |
| **m05** | 553×354 | noir/violet/orange, 16 % bleu *(ignorées)* | ⚠️ badge + coins | titre centré 3 lignes, portrait bas centre | **un mot en brush coloré** + arc lumineux |

## 3. Doctrine : aucune couleur de modèle n'est reprise

Un modèle ne fournit **que trois choses** :

| Ce que le modèle fournit | Ce qu'il ne fournit jamais |
|---|---|
| La **structure** : grille, places, rythme | Ses **couleurs** — y compris quand il est bleu |
| La **typographie** : échelle, casse, traitement par mot | Ses dégradés (violet, orange, arc-en-ciel) |
| Le **traitement de l'image** : détourage, halo, fondu, profondeur | Son badge de durée, ses coins arrondis, son chrome YouTube |

La palette est **reconstruite pour chaque visuel** :

| Part | Source |
|---|---|
| ~60 % | nuances du **fond choisi** dans `fonds/INDEX.md` |
| ~30 % | couleur de la **tenue de l'orateur** (chemise, veste), échantillonnée sur la photo |
| ~10 % | **un** accent — `#68D8C0` (menthe) ou un dérivé du fond |

Conséquence pratique : **qu'un modèle soit bleu, violet ou arc-en-ciel ne change rien au choix.**
m02, m04 et m05 ne sont donc ni « interdits » ni « à éviter » : ils sont recolorés. Et m01 n'est pas
« le bon modèle » parce qu'il est bleu — il est bon parce que sa **structure** est la plus aboutie.

Les couleurs mesurées restent dans les fiches à titre documentaire (pour reconnaître un modèle d'un
coup d'œil), jamais comme consigne de production.

## 4. Combinaisons recommandées (pour la fusion de modèles)

| Fusion | Résultat attendu | Faisabilité palette |
|---|---|---|
| **m01 + m05** | bande basse nom/date de m01 + mot en brush de m05 | ✅ directe, entièrement en bleu |
| **m01 + m03** | hiérarchie de m01 + titre centré et éclat de m03 | ✅ simple recalage de teinte |
| **m01 + m04** | bande basse de m01 + échelle de titre de m04 | ⚠️ recolorer le violet, remplacer l'ombre par un voile |
| **m02 + m05** | grille portrait-gauche + brush | ⚠️ deux conversions couleur à faire |

## 5. Limites du lot

- **Un seul modèle est un export propre** (m01, 1280×720). Les quatre autres sont des **captures
  d'écran** : coins arrondis, badge de durée, parfois le titre de la vidéo sous l'image. Leur
  résolution (562 à 720 px de large) ne permet pas de les recopier au pixel — ils documentent une
  intention, pas une géométrie exacte.
- **Aucun modèle portrait** (story 1080×1920) ni **flyer** : les déclinaisons verticales restent à
  construire, par transposition des grilles ci-dessus.
- **Aucune photo d'orateur** n'est fournie à ce stade : `orateurs/` est encore vide.
