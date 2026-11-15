# Note de livraison — miniature « ALERTE CODE R.O.U.G.E » **avec AP · FOND 26** (v2)

- **Fichier** : [`2026-11-07-miniature-alerte-code-rouge-avec-ap-v2-fond26-1280x720.jpg`](2026-11-07-miniature-alerte-code-rouge-avec-ap-v2-fond26-1280x720.jpg)
- **Format** : miniature YouTube **1280 × 720** · livrée le 2026-11-07
- **Demande** : rectification du thème appliquée à la 2ᵉ miniature, celle qui utilise le **fond
  bleu / rouge fourni** (`FOND 26.jpeg`)
- Script : `scripts/render_alerte_code_rouge.py ap-fond26 <sortie.jpg>`

## Ce qui a été utilisé

| Élément | Choix |
|---|---|
| Modèle | **M01 · bleu nuit, titre coupé** — même grille que la v1 |
| Fond | **FOND 26** fourni → `fonds/f27-bleu-magenta-rouge.jpg` (626 × 357), **ramené au bleu** |
| Palette | bleus + acier + cramoisi + ROUGE en accent — mesuré : **79,8 % de bleu**, 13,2 % de rouge, 4,0 % de teintes violettes résiduelles |
| Typographie | **Anton** + **Jost** — duo du thème, identique aux autres sorties |
| Textes | « ALERTE CODE » · « R.O.U.G.E » · « les 5 clés pour vivre / une chrétienne victorieuse » · « PRÉDICATEUR / AP Enock MISSIMAHOU » |
| Sujet | même détourage validé : 549 × 690, à droite, ancré au bord bas |

## Le fond fourni, et ce qu'il a fallu lui faire

`FOND 26` est une **diagonale bleu → magenta → rouge** avec trame de points et stries : mesuré
**34 % de bleu, 27 % de magenta, 39 % de rouge**. Tel quel il viole la règle absolue de palette (le
bleu reste dominant, le magenta est hors charte) et il est noté dans la note comme « fond non bleu
ramené au bleu ». Traitement, inchangé depuis la v1 :

1. **l'axe du fond est conservé** — bleu en haut à gauche, rouge en bas à droite — et sa diagonale
   de lumière aussi : c'est sa signature, elle n'est pas effacée ;
2. sa **luminance** est réutilisée, sa couleur remplacée par un dégradé de la palette (bleu nuit
   `#051226` → indigo → cramoisi → rouge profond) ;
3. **scrim** vertical + halo cyan en haut ;
4. **la diagonale rouge est rallumée par canaux** (R monte, G et B baissent sur la moitié droite) —
   **jamais** par un rouge translucide superposé : un rouge en transparence sur du bleu donne
   exactement le magenta à éviter ;
5. résultat mesuré : plus de magenta perceptible (4,0 % de teintes violettes, résidu
   d'anti-aliasing sous le seuil de perception).

Si le rouge doit être **plus franc** ou plus discret, c'est un réglage de deux coefficients dans
`_reconstruire_26()` (`scripts/render_rouge_5cles_ap.py`, repris par le rendu rectifié) : je réédite.

## Différences avec la v1

| | v1 (FOND 6) | v2 (FOND 26) |
|---|---|---|
| Fond | texture acier bleu, lumière rasante en haut à droite | diagonale bleu nuit → cramoisi, trame de points, stries |
| Dominante mesurée | 84,6 % bleu | 79,8 % bleu |
| Accent rouge | mot-code + souffle diffus en bas à gauche | mot-code + diagonale rouge à droite, derrière le sujet |
| Composition, polices, textes, sujet | — | **identiques** |

## Outil IA

**Aucun outil génératif.** Le fond est **reconstruit par composition** à partir de la luminance du
fichier fourni (dégradé de palette, scrim, halos, correction de la diagonale par canaux) : le rendu
est rejouable. Texte en couche de design, sujet détouré à la main et vérifié au zoom.

## À vérifier

1. **La phrase de la source** est recopiée telle quelle : « les 5 clés pour vivre **une** chrétienne
   victorieuse ». Si le mot « vie » a été omis par inadvertance, une ligne à changer.
2. Photo d'origine déjà coupée en bas, ancrée au bord bas du cadre.
3. Droits de diffusion de la photo et du fond (relèvent du commanditaire).
