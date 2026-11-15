# Note de livraison — miniature « Les 5 clés… : ROUGE » **avec AP · FOND 26** (v2)

> **Titre remplacé le 2026-11-07.** Le thème s'intitule désormais « ALERTE CODE R.O.U.G.E :
> les 5 clés pour vivre une chrétienne victorieuse ». Cette livraison reste en place, non
> modifiée, comme mémoire du titre précédent ; les sorties à jour sont datées du même jour
> sous le nom `…-alerte-code-rouge-…` (fiche : [`themes/les-5-cles-rouge.md`](../themes/les-5-cles-rouge.md)).

- **Fichier** : [`2026-11-07-miniature-les-5-cles-rouge-avec-ap-v2-fond26-1280x720.jpg`](2026-11-07-miniature-les-5-cles-rouge-avec-ap-v2-fond26-1280x720.jpg)
- **Format** : miniature YouTube **1280 × 720** · livrée le 2026-11-07
- **Demande** : « Si possible utilise le fond bleu rouge pour une 2ᵉ miniature. » — fond fourni :
  `FOND 26.jpeg` (626 × 357)
- Script : `scripts/render_rouge_5cles_ap.py <detourage> <sortie> fond26`

## Ce qui a été utilisé

| Élément | Choix |
|---|---|
| Fond | **FOND 26** fourni → indexé `fonds/f27-bleu-magenta-rouge.jpg` (626 × 357), **ramené au bleu** |
| Palette | bleus + acier + cramoisi + ROUGE en accent — mesuré sur le rendu : **82 % de bleu**, 11 % de rouge |
| Typographie | **Anton** + **Jost** — duo du thème ROUGE, identique à la v1 |
| Textes | « LES 5 CLÉS » · « ROUGE » · « pour vivre une vie chrétienne victorieuse » · « PRÉDICATEUR / AP Enock MISSIMAHOU » |
| Sujet | même détourage validé : 549 × 690, à droite, ancré au bord bas |

## Le fond fourni, et ce qu'il a fallu lui faire

`FOND 26` est une **diagonale bleu → magenta → rouge** avec trame de points et stries : mesuré
**34 % de bleu, 27 % de magenta, 39 % de rouge**. Tel quel il viole la règle absolue de palette (le
bleu doit rester la dominante à ~60 %) et son magenta est hors charte. Traitement, annoncé en ligne 1
comme l'exige la règle « à ramener au bleu » :

1. **l'axe du fond est conservé** — bleu en haut à gauche, rouge en bas à droite — et sa diagonale de
   lumière aussi : c'est sa signature, elle n'est pas effacée ;
2. sa **luminance** est réutilisée, sa couleur remplacée par un dégradé de la palette (bleu nuit
   `#051226` → indigo → cramoisi → rouge profond) : la diagonale se voit toujours, en clair ;
3. **scrim** vertical + halo cyan en haut ;
4. **la diagonale rouge est rallumée par canaux** (R monte, G et B baissent sur la moitié droite) —
   **jamais** par un rouge translucide superposé : un rouge en transparence sur du bleu donne
   exactement le magenta à éviter. C'est ce point qui a demandé plusieurs passes ;
5. résultat mesuré : **plus de magenta perceptible** (3,8 % de teintes violettes, résidu
   d'anti-aliasing sous le seuil de perception).

## Différences avec la v1

| | v1 (FOND 6) | v2 (FOND 26) |
|---|---|---|
| Fond | texture acier bleu, lumière rasante en haut à droite | diagonale bleu nuit → cramoisi, trame de points, stries |
| Dominante mesurée | 88 % bleu | 82 % bleu |
| Accent rouge | titre + souffle diffus en bas à gauche | titre + diagonale rouge à droite, derrière le sujet |
| Composition, polices, textes, sujet | **identiques** | **identiques** |

## Outil IA

**Aucun outil génératif.** Le fond est **reconstruit par composition** à partir de la luminance du
fichier fourni (dégradé de palette, scrim, halos, correction de la diagonale par canaux) : les
modèles image (Qwen-Image, FLUX.2 klein, Z-Image) ne sont pas installés ici, et aucun n'est
nécessaire — la reconstruction est rejouable. Texte en couche de design, sujet détouré à la main et
vérifié au zoom.

## En attente

Rien de bloquant. **À vérifier** : (1) le magenta du fond d'origine a été ramené au bleu et la
diagonale rouge rallumée par canaux — si tu veux un rouge plus franc ou plus discret, c'est un
réglage de deux lignes (`_reconstruire_26()`), je réédite ; (2) photo d'origine déjà coupée en bas,
ancrée au bord bas du cadre ; (3) droits de diffusion de la photo.
