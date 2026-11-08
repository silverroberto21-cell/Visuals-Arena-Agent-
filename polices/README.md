# /polices — polices embarquées

Les polices embarquées, **toutes sous licence OFL** (fichier de licence à côté de chaque fichier) :
usage commercial autorisé, y compris en miniature YouTube.

## Ce qui est là

| Fichier | Famille | Usage | Licence |
|---|---|---|---|
| `playfair-display-italic-var.ttf` | Playfair Display **Black Italic** (variable) | **titres** — la face de la vignette de référence | OFL 1.1 → `OFL-playfair-display.txt` |
| `montserrat-var.ttf` | Montserrat **SemiBold** (variable) | **signalétique** : ligne de rattachement, date, mentions, accents | OFL 1.1 → `OFL-montserrat.txt` |
| `anton-regular.ttf` | Anton Regular | **titres** des thèmes d'exhortation / d'énergie : capitales condensées très grasses, lisibles en vignette | OFL 1.1 → `OFL-anton.txt` |

## Pourquoi ces deux-là

La vignette envoyée par ICC Pahou utilise une **Didone italique** très grasse pour le titre :
contraste fort, empattements fins, oblique marquée. Playfair Display Black Italic en est la
transposition libre la plus proche ; le reste de la vignette est en sans-serif géométrique
espacée, d'où Montserrat.

Anton n'est **pas** là pour imiter la vignette de référence : c'est la face des thèmes
d'exhortation (« Maintiens le CAP »), où le titre doit tenir en trois mots et rester lisible à
320 px de large. Un thème = un duo : la présence d'Anton ne change pas le duo des autres thèmes.

## Règles

- **On ne déforme pas une police pour imiter une autre.** Pas de faux italique sur une romaine,
  pas d'étirement : si la face exacte manque, on choisit la plus proche et on le dit.
- Les fichiers variables sont chargés avec leur **instance nommée** (`Black Italic`,
  `SemiBold`) — jamais l'instance par défaut, qui est trop maigre pour un titre de miniature.
- Une nouvelle police n'arrive ici que si elle sert réellement : fichier + son `OFL-*.txt`,
  ligne ajoutée au tableau ci-dessus.
- Aucune police payante, aucune police sans licence explicite.

## Formats

Les fichiers sont des TTF variables, exploitables directement par Pillow/ImageMagick. Pour la
gravure print, convertir en contours — ne pas envoyer le TTF à l'imprimeur sans l'intégrer.
