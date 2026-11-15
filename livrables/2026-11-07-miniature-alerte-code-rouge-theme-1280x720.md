# Note de livraison — miniature YouTube « ALERTE CODE R.O.U.G.E » (thème seul)

- **Fichier** : [`2026-11-07-miniature-alerte-code-rouge-theme-1280x720.jpg`](2026-11-07-miniature-alerte-code-rouge-theme-1280x720.jpg)
- **Format** : miniature YouTube **1280 × 720** · livrée le 2026-11-07
- **Demande** : « il y a une rectification au niveau du thème — voici le thème à rectifier :
  *ALERTE CODE R.O.U.G.E : les 5 clés pour vivre une chrétienne victorieuse* »
- Script : `scripts/render_alerte_code_rouge.py theme <sortie.jpg>` (variante `theme`)
- Fiche : [`themes/alerte-code-rouge.md`](../themes/alerte-code-rouge.md)

## La rectification, à la lettre

| | Avant | Après (source) |
|---|---|---|
| Accroche | « LES 5 CLÉS » | « **ALERTE CODE** » |
| Mot-acrostiche | « ROUGE » | « **R.O.U.G.E** » — **avec ses points** |
| Phrase | « pour vivre **une vie** chrétienne victorieuse » | « les 5 clés pour vivre **une** chrétienne victorieuse » |

Aucune autre modification : la source ne dit rien d'autre, rien n'est ajouté, rien n'est corrigé en
silence. L'absence du mot « vie » dans la phrase est **recopiée telle quelle** — voir « À vérifier ».

## Ce qui a été utilisé

| Élément | Choix |
|---|---|
| Modèle | **M01 · bleu nuit, titre coupé** (`modeles/m01-bleu-nuit-titre-coupe.jpg`) — titre monumental à gauche, zone calme à droite, même énergie que la miniature précédente |
| Fond | **FOND 6** → `fonds/f06-bleu-acier-texture.jpg` : texture toile bleu acier, lumière rasante en haut à droite, assombrie ×0,86, scrim vertical, halo cyan, souffle rouge diffus en bas à gauche |
| Palette | bleus mesurés sur f06 (`#046398` / `#02446A` / `#058BBE` / `#0AB0D9`) + acier `#B0D6F6` + **ROUGE** `#DE2638` en accent — mesuré sur le rendu : **89,7 % de bleu**, 6,0 % de rouge, 2,5 % de teintes violettes résiduelles (anti-aliasing, sous le seuil de perception) |
| Typographie | **Anton** (accroche, mot-code) + **Jost** (phrase du thème) — duo du thème, inchangé |
| Textes | « ALERTE CODE » · « R.O.U.G.E » · « les 5 clés pour vivre / une chrétienne victorieuse » · `ICC PAHOU` — **rien d'autre** |
| Motif | clé filaire acier (466 × 192, rotation −15°, liseré et halo rouges) + cinq pastilles rouges : les cinq clés, sans un mot |

## Mise en page

- **Colonne de gauche** : marque, accroche précédée d'une **barre d'alerte rouge** (le signal),
  mot-code monumental, filet d'accent, phrase du thème. Rien ne touche les bords : marge de
  sécurité de 56 px respectée.
- **Césure à la frontière de sens** : « les 5 clés pour vivre » / « une chrétienne victorieuse » —
  décidée après mesure des deux lignes, pas au hasard du retour à la ligne.
- **Le mot-code porte l'affiche** : Anton, dégradé rouge clair → rouge foncé, ombre portée ; les
  points sont resserrés de 2 px pour que les cinq lettres se lisent comme **un seul code**.
- **Zone calme** : le coin inférieur droit reste vide, le badge de durée YouTube ne tombe sur rien.
- **Test à 160 px** : « R.O.U.G.E » reste lisible ; la dominante bleue tient.

## Outil IA

**Aucun outil génératif.** Texte composé en couche de design (Pillow + polices du dépôt),
motif de la clé tracé vectoriellement, fond pris tel quel dans `/fonds` et réglé par courbes et
voiles. Les modèles image (Qwen-Image, FLUX.2 klein, Z-Image) ne sont pas installés ici et aucun
n'est nécessaire : le rendu est **rejouable** à l'identique en une commande.

## À vérifier

1. **La phrase de la source** — « les 5 clés pour vivre **une** chrétienne victorieuse » — est
   recopiée à la lettre. Si le mot « vie » manquait par inadvertance (« pour vivre une vie
   chrétienne victorieuse »), dis-le : c'est une ligne à changer, je réédite les quatre sorties.
2. **Aucune date** n'est fournie pour ce visuel : elle n'est pas inventée.
