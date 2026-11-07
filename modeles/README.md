# /modeles — visuels de référence

Déposer ici les visuels dont l'agent doit **extraire un style** : structure, ambiance, effets.

## Convention de nommage

```text
<usage>-<ambiance>-<numero>.jpg     ex. youtube-priere-01.jpg
                                    ex. flyer-convention-02.jpg
                                    ex. story-jeunesse-01.jpg
```

Usages : `youtube`, `flyer`, `affiche`, `story`, `carre`.

## Ce que l'agent en retient

| Élément | Ce qu'on imite | Ce qu'on ne copie jamais |
|---|---|---|
| Structure | place du titre, place du portrait, blocs d'information | la mise en page au pixel |
| Ambiance | température du bleu, contraste, densité, texture | le sujet exact, le texte |
| Effets | halo, profondeur, lueur, vignettage, grain | l'interface (durée, barre de progression, logos) |

## Règles

- Privilégier **2 à 4 modèles** très différents plutôt que dix variantes du même style.
- Si un modèle contient une interface de plateforme (badge de durée, boutons), elle est **ignorée**
  à la lecture : le modèle documente un style, pas un écran.
- Signaler dans le brief ce qui plaît précisément (structure ? ambiance ? effets ?) : cela évite
  d'imiter le mauvais axe.
