# Palette — le bleu comme référence, la tenue comme secondaire

La palette n'est pas une liste de hex figée : elle se **déduit du fond fourni**. Ce document décrit
la méthode et les garde-fous.

## 1. Règle absolue

Le bleu et ses dégradés occupent **~60 %** de la surface et restent visibles **au premier regard**.
Test de contrôle : à 20 % de zoom, l'image doit encore se lire « bleue », pas « multicolore ».

## 2. Extraction des nuances du fond (étape 3 du process)

1. Prélever **3 à 5 nuances** dans le fond fourni : ombre profonde, bleu médian, lumière/haute
   valeur, éventuelle teinte d'accent déjà présente.
2. Noter les hex (ou leur approximation) — ils servent de base à tous les aplats, dégradés et
   voiles du visuel.
3. Vérifier la température : bleu froid (tendance cyan) ou bleu chaud (tendance indigo/violet).
   Les secondaires devront rester du même côté de la roue.
4. Si le fond est un dégradé : respecter son axe (haut sombre → bas clair, ou rayonnement central)
   pour que la lumière du visuel reste cohérente.

## 3. Construction de la palette (étape 4 du process)

| Part | Rôle | Source | Vérification |
|---|---|---|---|
| ~60 % | Dominante bleue | nuances du fond | recouvrement mesuré, pas estimé |
| ~30 % | **Secondaire 1 : couleur de la tenue** | échantillonnage du vêtement de l'orateur | identifiable, jamais plaquée sur un visage |
| 0–20 % | Secondaire 2 (+ éventuelle 3) | choix libre, harmonie avec le fond | maximum **3** secondaires, tenue incluse |
| ~10 % | Accent | date, lettre décorative, lumière, filets | jamais un aplat de fond, jamais un texte long |

### Échantillonner la tenue sans la trahir

- Prélever la teinte du vêtement **dans une zone éclairée** (éviter les plis sombres et les
  hautes lumières brûlées).
- En dériver 2 à 3 valeurs (claire / moyenne / sombre) pour les blocs graphiques, filets,
  libellés.
- La couleur de la tenue **n'est pas** une autorisation à repeindre la tenue : le vêtement de la
  photo reste tel qu'il est.
- Si la tenue est un neutre (noir, blanc, gris, beige), on prend sa **valeur** et on la teinte
  légèrement vers la famille du fond : la règle « tenue = secondaire » reste honorée, sans
  introduire de famille étrangère.

### Harmonie avec le fond

- Privilégier les combinaisons **analogues** (bleu + indigo + cyan) ou **complémentaires
  maîtrisées** (bleu + ocre/or/ambre en accent).
- Interdits : vert franc, magenta saturé, rouge vif en grande surface — ils cassent la dominante.
- La profondeur se construit par la **valeur** (clair/sombre) et la saturation, pas en empilant
  des teintes.

## 4. Si le fond n'est pas franchement bleu

1. Recalage de teinte (virage vers le bleu) si le fond est une texture neutre.
2. Superposition d'un dégradé bleu (20 à 60 % d'opacité) ou d'un voile de la dominante.
3. **Prolongement du fond** dans son axe par un dégradé bleu, quand le gabarit est plus large que
   le fond (`specs/fonds.md`, cas 2b) : on prolonge avec les nuances du fond, jamais avec un bleu
   standard.
4. Remplacement par un fond bleu construit dans le même esprit.
5. **Signalement obligatoire dans la note**, ligne 1 : « fond ramené au bleu » / « fond prolongé ».

Après tout traitement de fond (pivot, recadrage, prolongement, voile) : **recompter la part de
bleu**. Un prolongement ou un recadrage peut faire glisser la dominante sous les 60 % sans qu'on
le voie à l'œil.

## 5. La tenue « jure » avec le bleu — procédure

On ne repeint pas. Dans l'ordre :

1. Reculer la **saturation des seuls éléments graphiques** dérivés de la tenue (filets, blocs,
   libellés) — la photo, elle, ne bouge pas.
2. Séparer le sujet du fond par la **lumière** : liseré clair, halo sombre, dégradé bleu derrière
   la silhouette, légère vignette bleue.
3. Réduire la **surface** occupée par la tenue dans la composition (cadrage plus serré sur le
   buste, bloc bleu qui reprend le bas du visuel).
4. En dernier recours, désaturer **légèrement** la photo entière (≤ 15 %) : cela reste un
   ajustement global de lumière/couleur, jamais une recoloration localisée du vêtement, et cela se
   signale.

## 6. Contraste : mesurer, pas estimer

| Élément | Ratio minimum |
|---|---|
| Texte courant, date-lieu, contacts | 4,5:1 |
| Titre ≥ 24 px gras / ≥ 32 px | 3:1 |
| Filet, lettre décorative porteuse d'information | 3:1 |
| Texte sur photo ou dégradé | 4,5:1 après voile, mesuré sur la zone la plus claire |

Procédure : identifier le hex réel derrière le texte → calculer (formule WCAG) → si échec :
changer la valeur **dans la famille bleue** (blanc cassé, bleu nuit) ou poser un voile bleu
40–75 %, ou déplacer le texte sur une zone plus dense. Jamais de contour blanc « pour dépanner ».

## 7. Impression

- Convertir en CMJN pour les flyers, garder le RVB pour le web.
- Les bleus profonds et les accents très saturés ne se reproduisent pas exactement : donner
  l'approximation CMJN retenue (en « À vérifier » si l'écart est visible).
- Taux d'encre total ≤ 300 % pour les grands aplats bleu nuit.

## 8. Exemple de traçabilité (note interne, non livrée)

```text
Fond F2 (dégradé bleu nuit → bleu acier) : #071A33 · #0E2C52 · #1B4A7A
Tenue (veste bordeaux) : #6E2233 → valeurs #8A3145 / #4E1524
Autres secondaires : #C9A227 (laiton, harmonie chaude) · #DCE6F2 (blanc bleuté, texte)
Accent : #F2C14E (date + lettre décorative)
Contraste titre #F7FAFF sur #0E2C52 = 12,1:1 · contacts #DCE6F2 sur #071A33 = 13,4:1
```
