# Fonds portrait — pivot, recadrage, prolongement

Un fond fourni est très souvent en **portrait** (fonds d'écran, images de téléphone), alors que la
miniature YouTube est en **paysage**. On ne l'écrase pas, on ne l'étire pas : on choisit l'un des
trois cas ci-dessous.

## 1. Arbre de décision

```text
Le gabarit est-il vertical ?  (story 1080×1920 · A5/A4 portrait · 1080×1350)
├── OUI → fond utilisé TEL QUEL (recadrage léger autorisé, jamais de pivot)
└── NON → le fond est-il aisément classable ?
    ├── ABSTRAIT (dégradé, texture, halo, lumière diffuse, aplat)
    │   └── PIVOT 90° : rotation exacte, sans déformation
    └── SENS NATUREL (horizon, ciel, architecture, perspective, motif directionnel, texte)
        ├── la zone utile contient le sujet et la résolution suffit → RECADRAGE horizontal
        └── sinon → PROLONGEMENT par dégradé bleu dans l'axe du fond
```

## 2. Classer le fond : abstrait ou à sens naturel ?

| Indice | Verdict |
|---|---|
| Dégradé, bokeh, grain, halos, lumière douce sans direction identifiable | **abstrait** |
| Horizon, mer, ciel avec nuages définis, montagne | **sens naturel** |
| Bâtiment, fenêtre, arche, colonne, perspective, fuite | **sens naturel** |
| Motif directionnel (rayons, bandes obliques, tissu plissé) | **sens naturel** |
| Texte, logo, chiffre incrusté | **sens naturel** (un texte pivoté est illisible) |
| Personne ou silhouette identifiable | **sens naturel** (une personne couchée est un contresens) |
| Ombres portées franches donnant une direction de lumière | **sens naturel** |

Doute persistant → traiter comme **sens naturel** (la solution prudente).

## 3. Cas 1 — Pivot 90° (fonds abstraits)

1. Rotation **exacte** de 90° (ou 270°), jamais un angle libre, jamais une rotation suivie d'un
   étirement.
2. Conserver la résolution d'origine : un pivot ne crée pas de pixels.
3. Vérifier que la **source lumineuse** reste plausible après rotation (une lueur « basse » qui
   devient latérale est souvent acceptable ; une ombre projetée vers le haut ne l'est pas).
4. Recaler la dominante bleue si le pivot met en tête une zone trop claire ou trop sombre : les
   textes doivent rester sur la zone dense.
5. Noter dans la note : « fond pivoté 90° ».

## 4. Cas 2a — Recadrage horizontal (fonds à sens naturel)

1. Identifier la **zone utile** : la partie qui porte l'ambiance (ciel + horizon, façade, texture).
2. Recadrer au ratio exact du gabarit (16:9, 4:5, 1:1…) en gardant l'axe naturel : horizon
   horizontal, perspective crédible.
3. Vérifier la résolution après recadrage : la zone conservée doit couvrir la largeur cible
   (1280 px pour une miniature, 2480 px pour un A4 à 300 dpi). Sinon → cas 2b.
4. Ne pas recadrer dans une zone où un élément identifiable est tronqué (moitié de visage, moitié
   de logo).

## 5. Cas 2b — Prolongement par dégradé bleu

1. Étendre le canevas jusqu'au ratio cible, **du côté le moins chargé** du fond.
2. Échantillonner la couleur des **bords** du fond (haut et bas, ou gauche et droite) et prolonger
   le dégradé **dans son axe** : on continue la pente existante, on ne crée pas une nouvelle
   direction de lumière.
3. Aucun motif dupliqué, aucune symétrie visible : si un élément se répète (nuage identique,
   colonne répétée), on l'atténue ou on le masque par le dégradé.
4. Fondre la jonction : dégradé de raccord de 80 à 200 px, léger flou local, grain cohérent.
5. Vérifier la **couture à 100 %** de zoom, puis à 25 % : aucune ligne franche ne doit apparaître.
6. Recompter le bleu : après prolongement, la dominante doit toujours être ≥ 60 % (le prolongement
   ajoute du bleu, il ne dilue pas l'ambiance).
7. Noter dans la note : « fond prolongé en dégradé bleu ».

## 6. Cas 3 — Gabarits verticaux : fond tel quel

- Story 1080×1920, flyer A5/A4 portrait, post 1080×1350 : le fond portrait est utilisé **tel quel**.
- Recadrage léger et repositionnement vertical autorisés pour placer le bloc titre.
- Zones d'interface toujours respectées (haut 250 px / bas 320 px en story).
- Aucun pivot, même sur un fond abstrait : il n'y a aucune raison de coucher un fond qui convient.

## 7. Contrôles (à passer avant livraison)

- [ ] Le cas appliqué est le bon (abstrait / sens naturel / gabarit vertical).
- [ ] Aucune déformation : rapport hauteur/largeur des éléments respecté.
- [ ] Aucun pivot sur un fond à sens naturel, aucun pivot sur la photo de l'orateur.
- [ ] Source lumineuse cohérente après pivot.
- [ ] Aucune couture visible après prolongement (contrôle à 100 % et 25 %).
- [ ] Aucun motif dupliqué, aucun élément identifiable tronqué par le recadrage.
- [ ] Résolution suffisante pour le format final.
- [ ] Bleu ≥ 60 % après traitement.
- [ ] Traitement mentionné dans la note (ligne 1), en trois mots : « fond pivoté », « fond recadré »,
      « fond prolongé ».

## 8. Interdits

- Étirer un fond pour remplir un cadre (déformation du dégradé et du motif).
- Pivoter un ciel, une architecture, un texte ou une personne.
- Recadrer « au centre » sans regarder ce qu'on coupe.
- Prolonger en créant une seconde direction de lumière ou en dupliquant un motif.
- Traiter la photo de l'orateur comme un fond : elle n'est ni pivotée, ni étirée, ni prolongée.
