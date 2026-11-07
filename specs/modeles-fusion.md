# Fusion de modèles

Associer **deux modèles** en un **troisième, original**, proposer **2 variantes**, puis
l'enregistrer dans `/modeles` avec sa fiche. Sur demande explicite uniquement.

## 1. Quand déclencher

| Situation | Réponse |
|---|---|
| « Fusionne M2 et M5 », « crée un modèle original à partir de ces deux-là » | **oui**, on lance la voie fusion |
| « Fais-moi un visuel dans l'esprit de M2 » | non : c'est un visuel, process normal |
| « Ces deux modèles, tu peux en faire un troisième ? » | oui (demande explicite, même formulée en question) |
| L'agent trouve lui-même que deux modèles se marieraient bien | **non** : il n'y a pas de demande. Il peut le suggérer en fin de livraison, jamais l'exécuter. |

## 2. Étape 1 — Extraire les traits

Remplir ce tableau **avant** de composer. Un trait par ligne, deux sources par colonne.

| Trait | Modèle A | Modèle B | Retenu |
|---|---|---|---|
| Structure / grille | ex. bandeau titre haut, portrait pleine hauteur à droite | ex. composition diagonale, portrait en bas | A |
| Traitement du titre | ex. capitales condensées, lettrine scripte | ex. serif italique, filet sous le titre | A + lettrine de B |
| Place du portrait | ex. 45 % largeur, pied coupé | ex. détouré sur halo | B |
| Effets | ex. grain + vignettage | ex. lueur radiale, profondeur de champ | A grain + B lueur |
| Lumière | ex. contre-jour | ex. lumière frontale douce | B |
| Texture | ex. papier | ex. verre fumé | — |
| Rythme / densité | ex. très dense | ex. très aéré | A |

Le tableau est la trace du travail : il sert à rédiger la fiche (§ 5).

## 3. Étape 2 — Composer de l'original

- Une **structure nouvelle** naît de la combinaison des traits retenus — pas de la juxtaposition
  de deux morceaux d'image.
- Interdit : moitié haute de A + moitié basse de B. C'est un collage, pas un modèle.
- Interdit : reprendre une composition **identifiable** d'un modèle protégé (une signature
  graphique reconnaissable reste protégée, même recomposée).
- Autorisé et attendu : reprendre des **traits génériques** (bandeau titre, diagonale, halo,
  vignettage, grain) qui n'appartiennent à personne.
- Le modèle fusionné doit être **rejouable** : on doit pouvoir y glisser un autre titre, un autre
  orateur, une autre date, sans casser la composition.

## 4. Étape 3 — Proposer 2 variantes

- **V1** et **V2**, construites sur les mêmes traits retenus, avec **une différence majeure** :
  - V1 privilégie la **structure** (disposition, rythme, place du portrait) ;
  - V2 privilégie les **effets** (lumière, profondeur, texture) sur une structure plus sobre.
- Ce qui **ne change pas** entre V1 et V2 : la dominante bleue, le duo de polices du thème, la
  hiérarchie, les garde-fous (sujet intact, textes exacts, marges, pas d'interface de plateforme).
- Présentation : deux images côte à côte, une phrase de différence chacune, et on **attend le
  choix**. On n'enregistre pas « la meilleure » d'office.

Format de proposition :

```text
V1 — structure : …
V2 — effets : …
Laquelle j'enregistre comme modèle ? (ou : je peux croiser les deux, dis-moi ce que tu gardes)
```

## 5. Étape 4 — Enregistrer

Après choix (ou croisement demandé) :

```text
/modeles/modele-fusion-<slug>.jpg     ← le visuel modèle, sans texte d'un événement précis
/modeles/modele-fusion-<slug>.md      ← la fiche de description
```

- `<slug>` : 2 à 3 mots, minuscules, sans accent — ex. `modele-fusion-priere-profonde.jpg`.
- Le JPG doit être **propre** : pas de date, pas de nom d'événement, pas de contact. Un modèle se
  réutilise ; un modèle daté est un visuel mort.
- La fiche suit `templates/fiche-modele.md` et contient au minimum : sources, traits retenus,
  nouveauté, duo de polices, palette, effets, formats compatibles, ce qu'il faut éviter.
- Le modèle fusionné rejoint la liste des références : il peut être cité comme « modèle le plus
  proche » à l'étape 3 du process normal.

## 6. Critères de qualité avant enregistrement

- [ ] Le modèle est original : aucune composition identifiable reprise d'une source.
- [ ] Il ne contient aucun élément d'interface de plateforme.
- [ ] Il fonctionne avec un autre titre, un autre orateur, une autre date.
- [ ] Le bleu domine (~60 %) et la palette est cohérente avec les nuances des fonds.
- [ ] Le duo de polices est cohérent avec le thème (ou explicitement « duo du modèle »).
- [ ] Les marges du gabarit sont respectées (le modèle sert ensuite de base).
- [ ] La fiche est rédigée et enregistrée avec le JPG.

## 7. Refus et cas limites

| Demande | Réponse |
|---|---|
| « Fusionne ces deux modèles » sans fichiers identifiables | question groupée unique : quels fichiers ? |
| Fusionner un modèle avec une **capture d'écran** de plateforme | on extrait l'ambiance, jamais le chrome ; on le dit |
| « Fais exactement le même modèle que cette affiche connue » | refus : on reprend des traits génériques, pas une identité visuelle |
| Fusionner 3 modèles ou plus | possible uniquement sur demande explicite ; on documente les 3 sources dans la fiche |
| Le commanditaire ne choisit aucune variante | on ne sauvegarde pas ; on propose un croisement V1+V2 |
