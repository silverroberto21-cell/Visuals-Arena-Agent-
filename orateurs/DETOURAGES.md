# /orateurs — détourages archivés

Les **photos** d'orateurs restent dans `/orateurs` au format `nom-prenom.jpg` (règle du README).
Ce fichier-ci ne fait que tenir le registre des **détourages PNG** — un détourage est un fichier
dérivé, jamais la photo d'archive : c'est lui qui rend un visuel rejouable.

| Détourage | Source | Usage | Contrôle |
|---|---|---|---|
| `ap-enock-missimahou-detourage.png` | `_MG_2958.jpg` (fournie le 2026-11-07) | miniature « Maintiens le CAP » | bras restauré, vérifié au zoom |
| `ap-enock-missimahou-podium-detourage.png` | `_DSC3532.jpg.jpeg` (fournie le 2026-11-07) | miniatures « Les 5 clés : ROUGE » (titre précédent) | tête, deux bras, main + cinq doigts, micro : entiers |
| `ap-enock-3458-detourage.png` | `_DSC3458.jpg.jpeg` (fournie le 2026-11-07) | miniatures « ALERTE CODE R.O.U.G.E » avec AP — **version en service** | tête, deux bras, deux mains, cinq doigts, micro entier, **corps jusqu'en bas** ; **barre, Bible et verre du pupitre conservés** |

Le deuxième est un **plan poitrine coupé en bas à la source** : il s'ancre au bord bas du gabarit, et
ne se rogne jamais davantage.

## `ap-enock-3458-detourage.png` — le détail

- **Source** : `_DSC3458.jpg.jpeg`, 5906 × 3937, plan large. Le prédicateur est debout derrière un
  pupitre ; l'écran qui rediffuse une image de lui est à sa gauche, la bannière bleue derrière lui.
- **Détourage** : `scripts/cutout_ap_3458.py` (~4 s, sans modèle génératif), **v2**.
- **Méthode v2 — on décrit le fond, pas le sujet.** La v1 seuillait la peau, la tunique et les
  cheveux : ces familles se recouvrent dans cette photo (le cuir chevelu éclairé a la teinte du
  mur clair, la tunique celle de la bannière), d'où des encoches dans le crâne et une marche en
  escalier sur la joue. La v2 mesure deux familles de **fond** (mur clair : H 85-132, S ≤ 80,
  V ≥ 118 · bannière et écran : H 88-126, S ≥ 15, V ≥ 120) et remplit depuis les quatre bords :
  le sujet est le complément, il garde donc ses cheveux rasés comme ses verres de lunettes.
  Jamais le bleu sombre (V < 118) dans le fond : c'est la tunique.
- **Le pupitre reste** (consigne du 2026-11-07, après une v1 qui coupait le corps à la hauteur de
  la barre) : barre laquée relevée colonne par colonne sur la photo, panneau de verre suspendu et
  ses attaches, Bible ouverte. Ces matières sont couleur de fond : le remplissage les aurait
  mangées, elles sont donc reposées à leur géométrie mesurée. Le **corps d'AP descend jusqu'au
  bord bas** de la photo : rien n'est coupé en travers du torse.
- **Écran de rediffusion** : retiré par couleur dans son cadre mesuré, bâton lumineux compris.
- **Décor retiré hors du corps mesuré** : aplat bleu et lettrage (magenta H 140-175, jaune
  H 24-45) de la bannière ; pied de micro qui traverse le plan à gauche ; fil du plafonnier
  au-dessus du crâne. La réserve du corps est **étroite** (5 px) : entre le bras et le torse, le
  lettrage affleure dans des fentes de quelques pixels qu'une dilatation de 13 px couvrait.
- **Pièges mesurés** : les lèvres et la peau sont en H 4-18 / S 86-165 — les lettres jaunes
  (H 25, S 219) tombaient dans l'ancienne règle « peau ≤ 26 » et étaient protégées à tort ; le
  ruban adhésif bleu du micro (H 100, S 255, V 250) a exactement la couleur de la bannière ;
  le lettrage magenta H 149-165 tombait dans l'ancienne borne « peau ≥ 163 ».
- **Ordre des passes** (il compte) : remplissage **avant** de poser le pupitre, sinon la barre
  referme une poche où le lettrage reste collé ; rebouchage des trous **sans** les pixels de décor
  déjà retirés, sinon il les remet ; pupitre reposé **en dernier**.
- **Ce qui est entier** : crâne et cheveux, oreilles, lunettes (verres rebouchés), barbe, les deux
  bras, les deux mains et leurs cinq doigts, le micro de la capsule au cylindre et son attache
  bleue, la montre.
- **Bord** : 1 px d'érosion puis adoucissement — pas de frange bleue sur la peau ; les franges
  vives restées opaques (magenta, jaune) sont retirées sur 7 px de bord seulement, alpha seul.
- **Format** : 3504 × 2639, 41,0 % de pixels opaques. Le sujet entre dans le gabarit à
  **929 × 700** (hauteur 700 px), ancré au bord bas droit.

Script de rendu : `scripts/render_alerte_code_rouge.py` (variantes `ap` et `ap-fond26`).
