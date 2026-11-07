# Charte couleurs — règles d'application

La charte est fournie par la structure sous la forme `[HEX + règles]`. Tant qu'elle n'est pas
fournie, **aucune création**. Ce document fixe comment on l'applique : il ne remplace jamais les
hex du commanditaire.

## 1. Structure de palette à exiger

Un jeu exploitable décrit, pour chaque couleur :

| Rôle | Ce qu'on attend | Exemple de format |
|---|---|---|
| Dominante (fond) | 1 couleur principale, 60 % de la surface | `#0B2545` |
| Secondaire | soutien, aplats, blocs | `#13315C` |
| Accent | titres, filets, CTA — 5 à 10 % max | `#E9B949` |
| Neutre texte clair | texte sur dominante | `#FFFFFF` (si autorisé) |
| Neutre texte sombre | texte sur fond clair | `#111111` (si autorisé) |
| Interdits | ex. « pas de rouge vif », « pas de dégradé » | texte |

Si la charte ne donne que 2 hex, la production se limite à ces 2 hex + leurs nuances internes, et
le manque part en question groupée avant de créer.

## 2. Ce qui compte comme « couleur hors charte »

Sont interdits tant qu'ils ne sont pas explicitement dans la charte :

- un aplat, un dégradé, une texture colorée, un motif ;
- une ombre portée colorée, un halo, un glow ;
- un contour, une puce, une icône, un badge, un cadre, une étiquette de prix ;
- un fond de photo qui amène une teinte étrangère (vert d'une pelouse, bleu d'un ciel) ;
- le blanc ou le noir purs si la charte ne les mentionne pas (ou précise « pas de blanc pur ») ;
- une couleur « presque » pareille choisie à l'œil.

## 3. Nuances autorisées (dérivées, jamais inventées)

Une seule méthode : la couleur charte + opacité, sur un fond charte.

- Teinte claire : hex charte à 10 / 20 / 30 / 40 % d'opacité sur la dominante.
- Teinte sombre : hex charte superposé à un aplat noir *si le noir est autorisé*, sinon
  2 couches de la dominante.
- On ne fait pas varier la teinte (pas de rotation de roue chromatique) : uniquement
  luminosité et opacité.
- Documenter les nuances utilisées dans la note technique interne (pas dans la sortie).

## 4. Contraste : mesurer, pas estimer

| Élément | Ratio mini |
|---|---|
| Texte courant, date, lieu, contacts | 4,5:1 |
| Titre ≥ 24 px gras / ≥ 32 px | 3:1 |
| Filet ou icône porteuse d'information | 3:1 |
| Texte sur photo | 4,5:1 après scrim (mesure sur la zone la plus claire) |

Procédure :
1. Identifier le hex réel du fond **derrière le texte** (photo comprise).
2. Calculer le ratio avec la formule WCAG (luminance relative).
3. Si échec : changer la couleur *dans la charte* → sinon ajouter un scrim charte 40–75 % →
   sinon déplacer le texte sur une zone plus calme.
4. Un titre peut être en accent sur dominante même si le ratio est bas **seulement** s'il
   atteint 3:1 et mesure ≥ 48 px ; sinon il passe en neutre clair.

## 5. Traitement des photos sans les altérer

- Le sujet (peau, cheveux, vêtement) n'est **jamais** recoloré, filtré, lissé.
- Le fond d'une photo peut être neutralisé : voile d'une couleur charte, dégradé en pied,
  vignettage charte, masque progressif. Cela ne touche pas le sujet.
- Photos de groupes fournies en couleurs vives : on ne désature pas la photo entière (le sujet
  serait altéré) ; on compense par la composition (bloc charte plein, scrim localisé).
- Détourage : uniquement si la charte autorise le détourage, et sans manger cheveux, épaules,
  mains. En cas de doute : pas de détourage.

## 6. Fonds fournis

Un fond n'entre dans la composition que s'il respecte la palette. Sinon :

1. Recalage de teinte du fond **si** le fond est une texture neutre (bois, béton, papier).
2. Voile de la dominante à 50–70 % pour le ramener dans la charte.
3. Remplacement par un aplat / dégradé 100 % charte construit dans le même esprit (à signaler en
   « À vérifier »).

## 7. Impression

- Convertir en CMJN pour l'impression, garder le RVB pour le web.
- Signaler tout hex impossible à reproduire en CMJN (accents très saturés, verts fluo, certains
  bleus profonds) et donner l'approximation CMJN retenue en « À vérifier ».
- Noir de texte sur fond clair : privilégier un noir riche si la charte le permet ; sinon le hex
  sombre de la charte.
- Taux d'encre total ≤ 300 % pour les grands aplats sombres.
