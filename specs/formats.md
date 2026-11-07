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

Fond perdu (impression) : tout élément qui touche le bord est prolongé de 3 mm au-delà. Aucun
texte, aucun visage dans cette bande.

## 2. Zones à ne jamais occuper

### Miniature 1280×720
- **Coin inférieur droit** : badge de durée YouTube → ~200×70 px libres.
- **Bord bas** : barre de progression → 24 px.
- Test obligatoire : réduire à **160 px de large** ; si le titre n'est plus lisible, ou si la
  dominante bleue se perd, le visuel est refusé.

### Story 1080×1920
- **Haut 250 px** : nom du compte, barre de statut.
- **Bas 320 px** : bouton « Envoyer un message », légende, CTA.
- **Côtés 120 px** : flèche de navigation.
- Le bloc contacts vit **au-dessus** de 320 px, jamais dessous.

### Feed 1080×1350 et 1080×1080
- Le bas de l'image peut être partiellement masqué par la légende : contacts à ≥ 72 px du bord.

### Affiches A5 / A4
- Zone de fixation en haut : titre à ≥ 10 mm du bord haut.
- Lisibilité à 2 m pour un A4 en extérieur : infos clés à ≥ 24 pt.

## 3. Aucun élément d'interface du modèle

Un modèle sert de référence de **style** : structure, ambiance, effets, traitement du titre.
On ne recopie **jamais** son interface :

- badge de durée (`12:45`), barre de progression, boutons de plateforme, curseur ;
- faux play, vignettes de vidéo, logos YouTube / Facebook / Instagram / TikTok ;
- numéros d'épisode ou compteurs qui n'appartiennent pas à l'événement.

Si un modèle est une capture d'écran, on reconstruit l'ambiance (dégradé, texture, lumière) sans
le chrome de l'application.

## 3bis. Orientation du fond

Les fonds sont souvent livrés en portrait alors que la miniature est en paysage. Le traitement
suit trois cas (détail : `specs/fonds.md`) :

| Gabarit | Traitement du fond |
|---|---|
| Story 1080×1920 · A5/A4 portrait · 1080×1350 | fond **tel quel** (aucun pivot) |
| Miniature 1280×720 · carré 1080×1080 · A5/A4 paysage | fond abstrait → **pivot 90°** · fond à sens naturel → **recadrage** ou **prolongement en dégradé bleu** |

Jamais d'étirement. Le traitement retenu est mentionné dans la note, ligne 1.

## 4. Grille de composition

- 12 colonnes sur la largeur utile, gouttière = 1 colonne.
- Le titre occupe au moins 6 colonnes ; il peut déborder de la grille **une fois**, jamais deux.
- Un seul bord de référence pour les blocs texte (gauche ou centre), pas les deux.
- Le bloc **date-heure-lieu** est **un** bloc : jamais dispersé dans deux coins.
- Zone de respiration : au moins une hauteur de ligne entre deux niveaux.
- La dominante bleue se lit dans la **structure** (fond, masses, dégradés), pas seulement dans un
  bandeau : si le bleu n'apparaît que sur 20 % posés en aplat, c'est un échec.

## 5. Pièges fréquents

| Piège | Conséquence | Parade |
|---|---|---|
| Texte collé au bord | Coupé à l'impression / masqué | Marges du § 1 |
| Titre à 7 mots en miniature | Illisible en vignette | Retirer des mots, jamais descendre sous 54 px |
| Contacts sous l'interface de story | Invisibles | Remonter à 320 px du bas |
| Photo plein cadre sans voile | Contraste < 3:1 | Voile bleu 40–75 % derrière le texte |
| A5 exporté en 72 dpi | Flou à l'impression | 300 dpi, 1748×2480 px |
| RVB imprimé | Dérive de bleu | CMJN + signalement de l'écart |
| Visage sur l'axe de pli A4 | Visage déformé | Visages hors pli |
| Effets empilés « pour le style » | Visuel sale, modèle trahi | Un effet = une fonction (profondeur, lumière, texture) |

## 6. Déclinaison d'un même thème

Un thème = un duo de polices + une méthode de palette + une hiérarchie. En changeant de format :

| Élément | Règle |
|---|---|
| Dominante bleue | même famille de fond, même axe de dégradé ; le bleu reste ≥ 60 % |
| Tenue (secondaire) | même teinte échantillonnée, mêmes valeurs dérivées |
| Titre | même casse, même duo ; en story on peut monter à 4 lignes |
| Photo | même cadrage, recadrage plus serré (buste) autorisé |
| Date-heure-lieu | bloc identique, repositionné selon les zones d'interface |
| Contacts | contenu exact identique, ≥ 24 px |
| Accent | même couleur, même rôle (date, lettre, lumière) |
