# Note de livraison — miniature « ALERTE CODE R.O.U.G.E » **avec AP** (FOND 6)

- **Fichier** : [`2026-11-07-miniature-alerte-code-rouge-avec-ap-1280x720.jpg`](2026-11-07-miniature-alerte-code-rouge-avec-ap-1280x720.jpg)
- **Format** : miniature YouTube **1280 × 720** · livrée le 2026-11-07
- **Demande** : rectification du thème (« ALERTE CODE R.O.U.G.E : les 5 clés pour vivre une
  chrétienne victorieuse ») appliquée à la miniature **avec AP Enock**, photo
  `_DSC3458.jpg.jpeg`
- Scripts : `scripts/render_alerte_code_rouge.py ap <sortie.jpg>` · détourage : `scripts/cutout_ap_3458.py`
- Sujet : [`orateurs/ap-enock-3458-detourage.png`](../orateurs/ap-enock-3458-detourage.png)
  (détourage du 2026-11-07, `orateurs/DETOURAGES.md`)

## Ce qui a été utilisé

| Élément | Choix |
|---|---|
| Modèle | **M01 · bleu nuit, titre coupé** — repris de la miniature du thème : même grille de lecture |
| Fond | **FOND 6** → `fonds/f06-bleu-acier-texture.jpg`, identique à la miniature du thème (×0,86, scrim, halo cyan, souffle rouge bas gauche) |
| Palette | bleus f06 + acier `#B0D6F6` + **ROUGE** `#DE2638` — mesuré : **83,3 % de bleu**, 11,0 % de rouge |
| Typographie | **Anton** (accroche, mot-code) + **Jost** (phrase, prédicateur) — duo du thème |
| Textes | « ALERTE CODE » · « R.O.U.G.E » · « les 5 clés pour vivre / une chrétienne victorieuse » · « PRÉDICATEUR / AP Enock » · `ICC PAHOU` |
| Sujet | **597 × 662**, à `x = 643`, tête entière, les deux mains, cinq doigts et micro intacts, **ancré au bord bas** |

## Le sujet : la nouvelle photo, le pupitre dehors

La photo fournie (`_DSC3458`, 5906 × 3937) est un plan large : le prédicateur est **debout derrière
un pupitre**, l'écran qui rediffuse son image dans le dos à sa gauche, la bannière bleue derrière
lui. Deux exigences ont guidé le détourage — la silhouette entière (AGENT.md § 5ter) et la consigne
« **le pupitre ne doit pas sortir** ».

| Point | Traitement |
|---|---|
| Pupitre | **coupe franche** ~40 px au-dessus de la barre laquée : barre, Bible ouverte et pied du pupitre sont hors du PNG. Le costume s'arrête sur le bord bas, comme une sortie de cadre |
| Écran | exclu : biseau sombre séparé du crâne par une coupe parallèle à son axe, puis éclats de l'écran retirés par couleur |
| Bannière | exclue : enveloppe mesurée + retrait du bleu vif et de son lettrage **dans des cadres vides de corps** |
| Micro | **entier** (capsule, cylindre, bague bleue), posé à la géométrie : il traverse la silhouette |
| Tunique | discriminée de la bannière par sa **valeur** (V ≤ 120 contre 141-221) : même teinte, exposition différente |
| Bords | frange colorisée depuis l'intérieur du sujet, alpha inchangé ; deux taches du lettrage magenta effacées par propagation de la couleur de la tunique |

Contrôles au zoom sur le rendu : crâne, oreilles, lunettes (verres rebouchés), barbe, les deux
épaules, les deux bras, **les deux mains et leurs cinq doigts**, le micro de la capsule au cylindre,
la montre — **aucune coupure**, aucun fragment de décor collé à la silhouette.

Script de détourage rejouable : `scripts/cutout_ap_3458.py` (~3 s). Registre :
[`orateurs/DETOURAGES.md`](../orateurs/DETOURAGES.md).

## Mise en page

- **Texte à gauche, sujet à droite** : accroche → mot-code → phrase → prédicateur ; le prédicateur
  occupe la place laissée par la clé filaire de la miniature du thème.
- **Tête dégagée** : le crâne ne touche jamais le bord haut ; la barre d'alerte et le mot-code
  s'arrêtent à 26 px du panneau du sujet.
- **Coin inférieur droit laissé calme** pour le badge de durée.
- **Test à 160 px** : « ALERTE CODE » et « R.O.U.G.E » restent lisibles, la dominante bleue tient.

## Outil IA

**Aucun outil génératif sur le visage ou le corps** — détourage et lumière seulement. Texte composé
en couche de design (Pillow + polices du dépôt), fond du dépôt réglé par courbes et voiles. Les
modèles image (Qwen-Image, FLUX.2 klein, Z-Image) ne sont pas installés ici.

## À vérifier

1. **La phrase de la source** est recopiée telle quelle (« … pour vivre **une** chrétienne
   victorieuse ») : si le mot « vie » a été omis par inadvertance, une ligne à changer.
2. **Aucune date** fournie → non inventée.
3. Photo d'origine déjà coupée en bas, ancrée au bord bas du cadre ; droits de diffusion de la photo
   (relève du commanditaire).
