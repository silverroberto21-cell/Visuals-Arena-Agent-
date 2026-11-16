# /livrables — visuels livrés

Un fichier par livraison, **jamais écrasé**. C'est la mémoire de ce qui est sorti : quel fond, quel
modèle, quelle composition, pour quel événement et à quelle date.

## Convention de nommage

```text
<AAAA-MM-JJ>-<format>-<theme>.jpg
```

```text
2026-11-07-miniature-atmosphere-de-priere-1280x720.jpg
2026-11-14-story-atmosphere-de-priere-1080x1920.jpg
```

- **date en tête** : tri chronologique naturel, et on retrouve un visuel par sa date ;
- **format** en clair : `miniature`, `story`, `carre`, `a5`, `a4`, `affiche`, `badge` ;
- **thème** en minuscules sans accents, mots séparés par des tirets ;
- dimensions en suffixe pour les formats qui en ont plusieurs ;
- une **variante** ajoute `-v2`, `-v3` — on ne réécrit pas la version livrée.

## Règles

- Ce dossier ne contient que des **sorties validées ou livrées**, pas des essais intermédiaires
  (les essais restent hors du dépôt).
- Aucune retouche n'est faite ici : si les textes évoluent, c'est un nouveau fichier daté.
- Chaque livraison est accompagnée, dans le même commit, de la note de livraison
  (fond utilisé, structure empruntée, palette) — voir `AGENT.md` §5.
- Les scriptes de rendu éventuels vont dans `scripts/`, jamais ici.
