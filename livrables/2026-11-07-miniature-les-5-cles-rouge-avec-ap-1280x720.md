# Note de livraison — miniature « Les 5 clés… : ROUGE » **avec AP** (FOND 6)

- **Fichier** : [`2026-11-07-miniature-les-5-cles-rouge-avec-ap-1280x720.jpg`](2026-11-07-miniature-les-5-cles-rouge-avec-ap-1280x720.jpg)
- **Format** : miniature YouTube **1280 × 720** · livrée le 2026-11-07
- **Demande** : « Intègre la photo de AP à la miniature. Si possible utilise le fond bleu rouge pour une 2ᵉ miniature. »
  — photo fournie : `_DSC3532.jpg.jpeg` · fond fourni : `FOND 26.jpeg` · miniature de référence :
  `2026-11-07-miniature-les-5-cles-rouge-1280x720.jpg`
- Scripts : `scripts/render_rouge_5cles_ap.py` (rendu) · `scripts/cutout_ap_podium.py` (détourage)
- Fiche : [`themes/les-5-cles-rouge.md`](../themes/les-5-cles-rouge.md)

## Ce qui a été utilisé

| Élément | Choix |
|---|---|
| Fond | **FOND 6** → `fonds/f06-bleu-acier-texture.jpg` — celui de la miniature du thème, **inchangé** (assombri ×0,86, scrim vertical, halo cyan, souffle rouge diffus en bas à gauche) |
| Palette | bleus de f06 + acier `#B0D6F6` + **ROUGE** `#DE2638` en accent — mesuré sur le rendu : **88 % de bleu**, 8 % de rouge |
| Typographie | **Anton** (accroche, mot-acrostiche) + **Jost** (phrase du thème, prédicateur) — duo du thème |
| Textes | « LES 5 CLÉS » · « ROUGE » · « pour vivre une vie chrétienne victorieuse » · « PRÉDICATEUR / AP Enock MISSIMAHOU » — **rien d'autre, rien de réécrit** |
| Sujet | **AP Enock MISSIMAHOU détouré**, à droite, tête entière, micro et main intacts |
| Marque | `ICC PAHOU` (forme courte réservée aux miniatures 1280×720) |

## Le sujet : découpe vérifiée, aucun membre rogné

La photo (4206 × 3822) est un plan poitrine **coupé en bas à la source**. Le détourage a été refait
à zéro (`scripts/cutout_ap_podium.py`, reproductible en ~14 s) :

| Étape | Règle |
|---|---|
| Base | `grabCut` contraint, 8 itérations sur une réduction à 45 %, amorces premier plan / fond |
| Bloc de porte derrière l'oreille + reflet d'épaule | retirés par **rectangle vérifié vide de corps**, filtré sur la couleur « porte » — aucune règle de couleur ne les sépare du visage, qui est dans la même plage de teinte |
| Fente bras / buste | retirée à la couleur (mur gris peu saturé + bois), **garde-fou** : aucun pixel de peau ni de tunique touché ; la fente reste **transparente** |
| Éclat de bois sur l'épaule | règle **géométrique + couleur** : seuls les amas *chauds* **entièrement contenus** dans un quadrilatère mesuré sont retirés. La peau appartient à une composante qui déborde du cadre → elle ne peut pas être retirée |
| Visage | verres des lunettes et barbe rebouchés **à l'intérieur de l'enveloppe de la tête seulement** |
| Encoches de la mâchoire | fermeture morphologique **bornée à la bande de la tête** — jamais de balayage ligne par ligne, qui coupait la joue au couteau |
| Trous internes | rebouchés, **sauf dans la fente** qui est une découpe volontaire |
| Couleur de bord | **décontamination** : la frange prend la couleur de l'intérieur du sujet, l'alpha reste identique au pixel — plus de liseré bois sur la manche |

**Contrôles au zoom sur le rendu final** : crâne, oreilles, lunettes, barbe, cou, les deux épaules,
les deux bras, la main et ses cinq doigts, le micro de la capsule au pied — **aucune coupure**.
Le bas de la photo (torse) est **ancré au bord bas du visuel** : pas de bande de fond sous la
coupure, pas de membre inventé.

## Mise en page

- **Texte à gauche, sujet à droite** : même origine de lecture que la miniature du thème
  (accroche → mot-acrostiche → phrase → prédicateur) ; le prédicateur prend la place de la clé filaire.
- **Tête dégagée** : sujet réduit (549 × 690), le crâne ne touche jamais le bord haut.
- **Coin inférieur droit laissé calme** : le badge de durée YouTube ne tombe sur aucun élément.
- **Test à 160 px** : « LES 5 CLÉS » et « ROUGE » restent lisibles, la dominante bleue tient.

## Outil IA

**Aucun outil génératif n'a touché le visage ni le corps.** Détourage manuel et assisté (masque,
seuils HSV vérifiés, `grabCut`, morphologie bornée) : les modèles de suppression de fond et
d'édition (Qwen-Image-Edit, FLUX.2 klein) ne sont **pas installés** ici, aucune clé n'est
configurée. Texte composé en couche de design (Pillow + polices du dépôt), fond non généré.
Détourage archivé : [`orateurs/ap-enock-missimahou-podium-detourage.png`](../orateurs/ap-enock-missimahou-podium-detourage.png).

## Écarts assumés

- **Le prédicateur remplace la clé filaire** (demandé). La clé et les cinq pastilles restent sur la
  miniature du thème.
- **Aucune date** : elle n'est pas fournie pour ce visuel ; je ne l'invente pas.

## En attente

Rien de bloquant. **À vérifier** : photo d'origine déjà coupée en bas, ancrée au bord bas du cadre ;
droits de diffusion de la photo (relève du commanditaire).
