# /orateurs — détourages archivés

Les **photos** d'orateurs restent dans `/orateurs` au format `nom-prenom.jpg` (règle du README).
Ce fichier-ci ne fait que tenir le registre des **détourages PNG** — un détourage est un fichier
dérivé, jamais la photo d'archive : c'est lui qui rend un visuel rejouable.

| Détourage | Source | Usage | Contrôle |
|---|---|---|---|
| `ap-enock-missimahou-detourage.png` | `_MG_2958.jpg` (fournie le 2026-11-07) | miniature « Maintiens le CAP » | bras restauré, vérifié au zoom |
| `ap-enock-missimahou-podium-detourage.png` | `_DSC3532.jpg.jpeg` (fournie le 2026-11-07) | miniatures « Les 5 clés : ROUGE » (titre précédent) | tête, deux bras, main + cinq doigts, micro : entiers |
| `ap-enock-3458-detourage.png` | `_DSC3458.jpg.jpeg` (fournie le 2026-11-07) | miniatures « ALERTE CODE R.O.U.G.E » avec AP — **version en service** | tête, deux bras, deux mains, cinq doigts, micro entier ; **pupitre, Bible et écran hors cadre** |

Le deuxième est un **plan poitrine coupé en bas à la source** : il s'ancre au bord bas du gabarit, et
ne se rogne jamais davantage.

## `ap-enock-3458-detourage.png` — le détail

- **Source** : `_DSC3458.jpg.jpeg`, 5906 × 3937, plan large. Le prédicateur est debout derrière un
  pupitre ; l'écran qui rediffuse une image de lui est à sa gauche, la bannière bleue derrière lui.
- **Détourage** : `scripts/cutout_ap_3458.py` (~3 s, sans modèle génératif).
  Trois familles de couleur mesurées sur le fichier — peau chaude (H ≤ 26 | H ≥ 163, S ≥ 70),
  tunique marine (H 95-130, S ≥ 90, **V ≤ 120**), cheveux dans la fenêtre du crâne (V < 105) —
  plus le micro posé à la géométrie, une enveloppe mesurée, et le rebouchage des trous internes.
  Le biseau de l'écran, qui longe le crâne et se soude aux cheveux, est retiré par une coupe
  parallèle à son axe ; les éclats de décor (support gris du micro, écran, bannière) sont retirés
  par couleur **dans des cadres mesurés vides de corps** — jamais par une règle globale, qui
  mangerait le verre de la montre et la bague bleue du micro.
- **Le pupitre ne sort pas** : coupe franche à `y = 3285`, soit ~40 px au-dessus de la barre
  laquée. Barre, Bible ouverte et pied du pupitre sont hors du PNG ; le costume s'arrête sur le
  bord bas du fichier, comme une sortie de cadre assumée.
- **Ce qui est entier** : crâne et cheveux, oreilles, lunettes (verres rebouchés), barbe, les deux
  bras, les deux mains et leurs cinq doigts, le micro de la capsule au cylindre, la montre.
- **Frange** : colorisée par propagation depuis l'intérieur du sujet (alpha strictement conservé) ;
  deux taches du lettrage magenta de la bannière, restées opaques sur le bord du poignet droit,
  sont effacées par propagation de la couleur de la tunique autour d'elles.
- **Format** : 1786 × 1979, 63,3 % de pixels opaques.

Script de rendu : `scripts/render_alerte_code_rouge.py` (variantes `ap` et `ap-fond26`).
