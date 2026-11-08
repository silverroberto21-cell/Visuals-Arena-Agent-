# /polices — polices embarquées

Les seules polices dont l'agent a besoin pour reproduire la typographie de la vignette de
référence. Toutes deux sous **licence OFL** (fichier de licence à côté de chaque fichier) :
usage commercial autorisé, y compris en miniature YouTube.

## Ce qui est là

| Fichier | Famille | Usage | Licence |
|---|---|---|---|
| `playfair-display-italic-var.ttf` | Playfair Display **Black Italic** (variable) | **titres** — la face de la vignette de référence | OFL 1.1 → `OFL-playfair-display.txt` |
| `montserrat-var.ttf` | Montserrat **SemiBold** (variable) | **signalétique** : ligne de rattachement, date, mentions, accents | OFL 1.1 → `OFL-montserrat.txt` |

## Pourquoi ces deux-là

La vignette envoyée par ICC Pahou utilise une **Didone italique** très grasse pour le titre :
contraste fort, empattements fins, oblique marquée. Playfair Display Black Italic en est la
transposition libre la plus proche ; le reste de la vignette est en sans-serif géométrique
espacée, d'où Montserrat.

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
