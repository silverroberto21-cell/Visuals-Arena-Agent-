# /modeles — visuels de référence

Déposer ici les visuels dont l'agent doit **extraire un style** : structure, traitement du titre,
effets, lumière. Un modèle **n'est pas** un gabarit à recopier, ni une palette à réutiliser.

📌 **Commencer par [`INDEX.md`](INDEX.md)** : correspondance « Modèle n → fichier », verdict palette,
éléments d'interface à ignorer, combinaisons de fusion recommandées.
Aperçu : [`planche.jpg`](planche.jpg). Fiches détaillées : un `.md` par modèle.

## Convention de nommage

```text
m<NN>-<ambiance>-<structure>.jpg       ex. m01-bleu-nuit-titre-coupe.jpg
m<NN>-<ambiance>-<structure>.md        fiche de description (même nom)
modele-fusion-<slug>.jpg / .md         modèle créé par fusion (voir specs/modeles-fusion.md)
```

**`<NN>` est le numéro d'origine** : « Modèle 3 » → `m03-…`. Le numéro reste en tête pour que les
repères du commanditaire ne se perdent pas — « Modèle 3 », « m03 » ou « le fond violet clair avec le
logo vertical » désignent le même fichier.

## Contenu actuel

| N° | Fichier | Couleurs *(ignorées)* | Interface | Ce qu'on en retient en priorité |
|---|---|---|---|---|
| m01 | `m01-bleu-nuit-titre-coupe` | bleu 85 % | ❌ aucune | bande basse nom + date, alternance de couleurs par ligne |
| m02 | `m02-rayures-prisme` | rouge/chaud, 12 % bleu | ⚠️ badge | grille portrait à gauche / texte à droite |
| m03 | `m03-degrade-violet-prisme` | bleu-violet, 61 % bleu | ⚠️ badge | titre centré bicolore, éclat derrière le portrait |
| m04 | `m04-violet-titre-geant` | violet | ⚠️ badge | échelle écrasante du mot-clé, script en sous-titre |
| m05 | `m05-noir-brush-colore` | noir/violet/orange | ⚠️ badge | un mot en brush coloré au milieu du titre |

## Doctrine : aucune couleur de modèle n'est reprise

Un modèle fournit la **structure**, la **typographie** et le **traitement de l'image**. Il ne fournit
**jamais** de couleur — même quand il est bleu : le bleu d'un modèle n'est pas celui du visuel.

| On reprend | On ne reprend jamais |
|---|---|
| Grille, place du portrait, rythme | Toute couleur du modèle (bleu compris) |
| Rapport d'échelle et de casse du titre | Dégradés violet / orange / arc-en-ciel |
| Traitement par mot (couleur, brush, script) | Badge de durée, coins arrondis, chrome YouTube |
| Effets de profondeur (halo, typo fantôme, arc) | Ombres portées colorées |

Palette reconstruite à chaque visuel : **bleu du fond (~60 %) + couleur de la chemise de l'orateur
(~30 %) + un accent (~10 %)**. Chaque fiche contient sa section **« Conversion pour ICC Pahou »**
quand le modèle est éloigné du bleu.

## Règles

- Privilégier **2 à 4 modèles** très différents plutôt que dix variantes du même style.
- Un modèle qui contient une interface de plateforme (badge de durée, boutons, coin arrondi) est lu
  **pour son style** : l'interface est ignorée.
- Signaler dans le brief ce qui plaît précisément (structure ? titre ? effets ?) : cela évite
  d'imiter le mauvais axe.
- **Fusion** : deux modèles peuvent être associés en un modèle original, sur demande explicite,
  avec 2 variantes puis enregistrement + fiche (`specs/modeles-fusion.md`).
