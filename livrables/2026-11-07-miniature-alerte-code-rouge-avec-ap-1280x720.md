# Note de livraison — miniature « ALERTE CODE R.O.U.G.E » **avec AP** (FOND 6)

- **Fichier** : [`2026-11-07-miniature-alerte-code-rouge-avec-ap-1280x720.jpg`](2026-11-07-miniature-alerte-code-rouge-avec-ap-1280x720.jpg)
- **Format** : miniature YouTube **1280 × 720** · livrée le 2026-11-07
- **Demande** : rectification du thème (« ALERTE CODE R.O.U.G.E : les 5 clés pour vivre une
  chrétienne victorieuse ») appliquée à la miniature **avec AP Enock MISSIMAHOU**, photo
  `_DSC3532.jpg.jpeg`
- Script : `scripts/render_alerte_code_rouge.py ap <sortie.jpg>`
- Sujet : [`orateurs/ap-enock-missimahou-podium-detourage.png`](../orateurs/ap-enock-missimahou-podium-detourage.png)
  (détourage inchangé, `orateurs/DETOURAGES.md`)

## Ce qui a été utilisé

| Élément | Choix |
|---|---|
| Modèle | **M01 · bleu nuit, titre coupé** — repris de la miniature du thème : même grille de lecture |
| Fond | **FOND 6** → `fonds/f06-bleu-acier-texture.jpg`, identique à la miniature du thème (×0,86, scrim, halo cyan, souffle rouge bas gauche) |
| Palette | bleus f06 + acier `#B0D6F6` + **ROUGE** `#DE2638` — mesuré : **84,6 % de bleu**, 9,9 % de rouge |
| Typographie | **Anton** (accroche, mot-code) + **Jost** (phrase, prédicateur) — duo du thème |
| Textes | « ALERTE CODE » · « R.O.U.G.E » · « les 5 clés pour vivre / une chrétienne victorieuse » · « PRÉDICATEUR / AP Enock MISSIMAHOU » · `ICC PAHOU` |
| Sujet | **549 × 690**, à `x = 678`, tête entière, micro et main intacts, **ancré au bord bas** |

## Le sujet : découpe vérifiée, aucun membre rogné

La photo (4206 × 3822) est un plan poitrine **coupé en bas à la source** : elle est donc ancrée au
bord bas du visuel, sans bande de fond sous la coupure et sans membre inventé. Le détourage est
**repris tel quel** de la livraison validée du même jour (`scripts/cutout_ap_podium.py`,
`orateurs/ap-enock-missimahou-podium-detourage.png`) : **aucune nouvelle découpe n'a été faite pour
cette rectification**, donc aucun risque de rogner AP.

Contrôles repassés au zoom sur le rendu de cette variante : crâne, oreilles, lunettes, barbe, cou,
les deux épaules, les deux bras, la main et ses cinq doigts, le micro de la capsule au sommet —
**aucune coupure**.

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
