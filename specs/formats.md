# Formats et marges de sécurité

Les dimensions sont des **contraintes**, pas des suggestions. On ne livre jamais un
« 1080×1080 approximatif ».

## 1. Gabarits

| Usage | Format | Dimensions px | Marges de sécurité | Longueur de titre | Fond perdu |
|---|---|---|---|---|---|
| Miniature YouTube | 16:9 | **1280×720** | 60 px sur les 4 côtés | **3 à 6 mots** | — |
| Flyer A5 | 148×210 mm | 1748×2480 @300 dpi | 8 mm (≈ 95 px) | 4 à 7 mots | 3 mm |
| Flyer A4 | 210×297 mm | 2480×3508 @300 dpi | 10 mm (≈ 118 px) | 4 à 8 mots | 3 mm |
| Post / flyer numérique | 4:5 | **1080×1350** | 72 px | 4 à 8 mots | — |
| Story / Reel | 9:16 | **1080×1920** | 120 px côtés · 250 px haut · 320 px bas | 4 à 8 mots | — |
| Carré réseaux | 1:1 | **1080×1080** | 72 px | 4 à 7 mots | — |

Règle de fond perdu (impression) : tout élément qui touche le bord doit être prolongé de 3 mm
au-delà. Aucun texte ni visage dans cette bande.

## 2. Zones à ne jamais occuper

### Miniature 1280×720
- **Coin inférieur droit** : badge de durée YouTube → garder ~200×70 px libres.
- **Bord bas** : barre de progression → 24 px.
- Vérification obligatoire : réduire à **160 px de large** ; si le titre n'est plus lisible,
  le visuel est refusé.

### Story 1080×1920
- **Haut 250 px** : nom du compte, barre de statut.
- **Bas 320 px** : bouton « Envoyer un message », légende, CTA de la plateforme.
- **Côtés 120 px** : flèche de navigation.
- Le bloc contacts vit **au-dessus** de 320 px, jamais dessous.

### Feed 1080×1350 et 1080×1080
- Bas de l'image partiellement masqué par la légende sur certains affichages : les contacts
  restent à au moins 72 px du bord bas.

### Affiches A5/A4
- Zone de fixation / agrafage en haut : ne pas mettre le titre à moins de 10 mm du bord haut.
- Lisibilité à 2 mètres minimum pour A4 en extérieur : corps de texte ≥ 24 pt pour les infos clés.

## 3. Grille de composition

- Grille de 12 colonnes sur la largeur utile (largeur − marges), gouttière = 1 colonne.
- Le titre occupe au minimum 6 colonnes ; il peut déborder de la grille **une fois**, jamais deux.
- Alignement : un seul bord de référence pour les blocs texte (gauche ou centre), pas les deux.
- Le bloc date-lieu est **un** bloc : date et heure sur une ligne, lieu en dessous, ou trois
  lignes dans le même bloc. Jamais dispersé dans deux coins.
- Zone de respiration : au moins 1 hauteur de ligne entre deux niveaux différents.

## 4. Pièges fréquents

| Piège | Conséquence | Parade |
|---|---|---|
| Texte collé au bord | Coupé à l'impression / masqué | Marge de sécurité de la table § 1 |
| Titre à 7 mots en miniature | Illisible en vignette | Retirer des mots, jamais rétrécir sous 54 px de corps |
| Contacts sous l'interface de story | Invisibles | Remonter à 320 px du bas |
| Photo plein cadre sans scrim | Contraste < 3:1 | Scrim charte 40–75 % derrière le texte |
| A5 exporté en 72 dpi | Flou à l'impression | 300 dpi, 1748×2480 px |
| Couleurs RVB pour l'impression | Dérive à l'impression | Convertir en CMJN pour les flyers, signaler l'écart |
| Visage sur la grille de pli A4 | Visage déformé | Garder les visages hors axe de pli |

## 5. Déclinaison d'un même thème

Un thème = un duo de polices + une palette + une hiérarchie. En passant d'un format à l'autre :

| Élément | Règle de déclinaison |
|---|---|
| Titre | Même casse, même duo, corps adapté ; en story on peut monter à 3 lignes |
| Photo | Même cadrage, recadrage plus serré autorisé (buste) en story et carré |
| Date-lieu | Bloc identique, repositionné selon les zones d'interface |
| Contacts | Même contenu exact, corps jamais inférieur à 24 px |
| Fond | Même famille de fond ; le fond peut changer si le recadrage l'impose (le signaler) |
