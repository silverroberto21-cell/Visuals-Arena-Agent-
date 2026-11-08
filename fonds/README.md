# /fonds — images de fond

Les fonds sont la **référence couleur** de tous les visuels : le bleu et ses dégradés y dominent.
Ce dossier contient **24 fonds uniques** fournis par la structure (2 lots), indexés et mesurés.

📌 **Commencer par [`INDEX.md`](INDEX.md)** : pour chaque fond, dimensions, teintes mesurées,
type (abstrait / sens naturel), pivot autorisé ou non, conformité palette, agrandissement nécessaire.
Version machine : [`index.yaml`](index.yaml). Aperçu visuel de tous les fonds : [`planche.jpg`](planche.jpg).

## Convention de nommage

```text
f<NN>-<ambiance>-<variante>.jpg      ex. f03-bleu-cyan-diagonal.jpg
                                     ex. f01-bleu-nuit-halo-cyan.jpg

_hors-charte/f<NN>-<ambiance>.jpg    fonds non bleus, jamais utilisés tels quels
```

**`<NN>` est le numéro d'origine** : `FOND 3.jpg` est devenu `f03-bleu-cyan-diagonal.jpg`. Le numéro
reste en tête pour que tes repères ne se perdent pas — « FOND 3 », « f03 » ou « le fond cyan en
diagonale » désignent le même fichier. Correspondance complète des 20 numéros (dont les 2 doublons)
dans [`INDEX.md`](INDEX.md) § 1 et dans [`index.yaml`](index.yaml).

## Contenu actuel

| Catégorie | Nombre | Fichiers |
|---|---|---|
| Abstraits conformes | 17 | bokeh (nuit / électrique / clair), halo cyan, vagues, texture acier, faisceaux, carreaux, diagonales, bleu clair strié, indigo, **halftone coins** (f21), **dégradé cyan** (f22), **rayures bleu nuit** (f24), **rayures indigo** (f25) |
| Cyan / turquoise appuyés | 2 | `f08`, `f16` |
| À recaler | 3 | `f05` (taches rose), `f23` (vert dans la lumière), `f26` (typographie incrustée) |
| À ramener au bleu | 1 | `f11` (bande végétale) |
| Sens naturel (aucun pivot) | 2 | `f11` (horizon), `f17` (scène de louange) |
| Hors charte | 1 | `_hors-charte/f18` (violet/magenta/orange) |

## Qualité attendue

- Résolution suffisante pour le plus grand format servi. **État du lot actuel : aucun fond n'est
  natif pour l'impression** (largeur maximale 1591 px) — voir `INDEX.md` § 4 pour les cibles et les
  parades (prolongement en dégradé bleu, reconstruction du dégradé, agrandissement raisonné).
- **Pas de texte incrusté** ni de logo dans le fond.
- Dégradé lisible : on doit pouvoir prélever 3 à 5 nuances distinctes (ombre, médian, lumière).
- Pas de personne identifiable, sauf fond de scène assumé (`bleu-scene-louange`) et autorisé.

## Ce que l'agent fait du fond

1. Extrait 3 à 5 nuances (hex) qui deviennent la base de la palette — les mesures sont déjà dans
   `INDEX.md` § 2 : l'agent les **reprend** au lieu de les redeviner.
2. Conserve l'axe du dégradé pour que la lumière du visuel reste cohérente.
3. Applique la règle d'orientation (`specs/fonds.md`) : `pivot = oui` → rotation 90° · `pivot = non`
   → recadrage ou prolongement en dégradé bleu · gabarit vertical → fond tel quel.
4. Si le fond n'est pas franchement bleu : le ramène au bleu et le signale dans la note, ligne 1.
5. Ne sélectionne **jamais** un fichier de `_hors-charte/` sans traitement.

## Formats de référence

| Usage | Ratio | Taille mini |
|---|---|---|
| Miniature YouTube | 16:9 | 1280×720 |
| Post / flyer numérique | 4:5 | 1080×1350 |
| Story | 9:16 | 1080×1920 |
| Carré | 1:1 | 1080×1080 |
| Flyer A5 print | 1:1.414 | 1748×2480 |
| Flyer A4 print | 1:1.414 | 2480×3508 |

## Priorités pour compléter le dossier

1. **Fonds print** : 2 à 3 fonds en 2480×3508 px (aucun aujourd'hui).
2. **Fonds portrait** : le lot est entièrement en paysage ; les stories se construisent par
   prolongement.
3. **Droits** : confirmer l'origine des images (banque ? création interne ?).
