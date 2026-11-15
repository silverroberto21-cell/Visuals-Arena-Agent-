# Note de livraison — miniature YouTube « Atmosphère de prière »

- **Fichier** : [`2026-11-07-miniature-atmosphere-de-priere-enock-missimahou-1280x720.jpg`](2026-11-07-miniature-atmosphere-de-priere-enock-missimahou-1280x720.jpg)
- **Format** : miniature YouTube **1280 × 720** · livrée le 2026-11-07
- **Demande** : « Miniature YouTube, thème *Atmosphère de prière*. Orateur : Enock MISSIMAHOU,
  date dispensable. Utilise un modèle de `/modeles` et un fond de `/fonds`, et cite-les. »
- Script : `scripts/render_priere_m01_ap.py` · fiche : [`themes/atmosphere-de-priere.md`](../themes/atmosphere-de-priere.md)

## Ce qui a été utilisé (règle 11 — les trois mentions)

| Élément | Choix |
|---|---|
| **Modèle** | **MODÈLE 1** → `modeles/m01-bleu-nuit-titre-coupe.jpg` : titre en fer à gauche sur lignes alternées, portrait détouré à droite, bande basse pour le nom, trame de points. **Aucune couleur du modèle reprise** (son bleu/cyan n'est pas celui du visuel). |
| **Fond** | **FOND 7** → `fonds/f07-bleu-nuit-bokeh.jpg` : flouté 3,2 px, assombri ×0,82, scrim vertical, halo cyan derrière le portrait. |
| **Outil IA** | **aucun, raison** : texte et mise en page composés en couche de design (Pillow + polices du dépôt), détourage fourni **nettoyé sur le seul canal alpha** — aucun modèle génératif n'a touché le visage, le corps ni la tenue (règle 9). |
| Typographie | **Anton** (titre, nom) + **Jost** (marque) — duo du thème, verrouillé |
| Palette | 60 % bleus de f07 (`#071A4E` → `#0D56B1` → `#0D89D2`) + 30 % bleu ardoise **de la chemise de l'orateur** (`#4A6691` → `#2E4A6E` / `#7C9AC4`) + 10 % or pâle `#E9CE93` en accent · texte `#F2F8FF` |
| Textes | « Atmosphère de prière » (le thème, rien de plus) · « Enock MISSIMAHOU » · « ICC PAHOU » |

## Portrait : photo déjà coupée à l'origine

La photo de `/orateurs` est **coupée dans la source** : buste arrêté sous la taille, pouce droit
qui touche le bord de l'image, main levée qui sort du cadre. Conformément à la **règle 9** :

- photo conservée **telle quelle**, **ancrée sur les bords** (bord droit de la photo = bord droit
  du visuel, bas de la photo = bas du visuel) : la coupure se lit comme une sortie de cadre ;
- **aucun membre recomposé**, aucun étirement, aucun pivot, aucun recadrage dans le corps ;
- seule intervention : **nettoyage du contour** sur le canal alpha (médiane 3 + flou 0,6) pour
  supprimer le voile de fond résiduel autour des cheveux, avec la vérification au zoom des
  4 bords, des deux mains et du micro — cheveux, oreille, lunettes, doigts et micro entiers.

## Décisions de composition

- **Titre en trois lignes** (héritage m01) : `Atmosphère` 122 px, `de` 73 px en acier, `prière`
  230 px. Le mot porteur est le plus gros, la préposition s'efface.
- **Pas de typographie fantôme** : sur un titre long, un mot fantôme derrière des lettres
  différentes se lit comme une faute. Le modèle garde de m01 sa **trame de points** et son
  **fondu bas du portrait** dans la bande du nom.
- **Nom dans la bande basse**, à 60 px du bord (marge de sécurité), avec une barre d'or en accent.
- **Coin inférieur droit laissé libre** : le badge de durée YouTube s'y posera ; aucun élément
  d'interface n'est imité.
- **Aucune date** : elle est dispensable et n'a donc pas été inventée (règle 4).

## Contrôles

| Contrôle | Résultat |
|---|---|
| Dimensions | 1280 × 720 exact |
| Dominante bleue | **94,3 %** de la surface (mesuré) |
| Contraste | titre 15,1:1 · nom 18,7:1 (mesuré après voile) |
| Lisibilité en petit | titre et nom lisibles à 160 px de large |
| Silhouette | mains, doigts, micro, oreille, lunettes entiers ; bords vérifiés au zoom |
| Palette | 1 secondaire (chemise) + accent or ; aucun dépassement |
| Interface | aucun badge, aucune barre, aucun logo de plateforme |

## À vérifier

Orthographe du nom affiché — **« Enock MISSIMAHOU »** — recopié tel quel depuis la demande et le
nom de fichier de la photo archivée (`orateurs/ap-enock-missimahou-detourage.png`) · photo
**d'origine déjà coupée**, ancrée aux bords · aucune date affichée (non fournie).
