# Auto-contrôle (étape 7)

À passer **avant** chaque livraison. Un seul échec = correction, puis on repasse la check-list.
On ne livre jamais avec une case non cochée, et on ne raconte pas la check-list dans la sortie.

## Bloc A — Couleurs

- [ ] Chaque couleur visible figure dans la charte (aplats, dégradés, ombres, contours, puces,
      icônes, cadres, badges, étiquettes).
- [ ] Les nuances utilisées sont dérivées d'un hex charte (opacité/luminosité), pas inventées.
- [ ] Le blanc et le noir ne sont présents que si la charte les autorise.
- [ ] Aucune teinte étrangère apportée par une photo, un fond ou un logo secondaire.
- [ ] Contraste mesuré : 4,5:1 (texte, contacts) · 3:1 (titre ≥ 24 px gras) · après scrim sur photo.
- [ ] Répartition 60 dominante / 30 secondaire / 10 accent respectée (l'accent reste un accent).

## Bloc B — Textes

- [ ] Comparaison **caractère par caractère** avec la source : titre, nom(s), qualité, date,
      heure, lieu, adresse, contacts.
- [ ] Accents et casse identiques à la source (`ÉVÉNEMENT`, `Cœur`, `Aïcha`).
- [ ] Chiffres exacts : date, année, heure, numéro de téléphone, prix.
- [ ] Aucun ajout : pas de slogan, pas de hashtag, pas de « entrée libre » non fourni.
- [ ] Aucune correction silencieuse : une incohérence source est en « À vérifier », pas réécrite.
- [ ] Cohérence interne : le jour de la semaine correspond à la date, l'heure est plausible.
- [ ] Orthographe française relue (une relecture dédiée, pas en même temps que la composition).

## Bloc C — Photo

- [ ] C'est bien la photo désignée pour cet orateur (bonne personne, bonne prise).
- [ ] Visage intact : pas de lissage, pas de retouche, pas de changement d'expression.
- [ ] Tenue intacte : pas de recoloration, pas de redessin, pas de logo effacé.
- [ ] Cheveux, épaules, mains non rognés par un détourage.
- [ ] Aucun filtre, aucune désaturation globale de la photo.
- [ ] Le visage n'est ni dans une zone de coupe, ni sous l'interface, ni sous un texte.
- [ ] Résolution suffisante pour le format final (≥ 1280 px sur le grand côté pour du web,
      300 dpi pour l'impression) — sinon le signaler en « À vérifier ».

## Bloc D — Polices

- [ ] Deux familles maximum, 3 graisses maximum.
- [ ] Même duo que les autres formats du thème.
- [ ] Accents français corrects, pas de glyphe manquant (carré ou substitution silencieuse).
- [ ] Aucun script pour les informations pratiques.
- [ ] Hiérarchie de tailles cohérente : titre > orateur > date-lieu > contacts.
- [ ] Retours de ligne maîtrisés : pas d'orphelin, pas de titre en 4 lignes.

## Bloc E — Lisibilité et fabrication

- [ ] Format aux dimensions exactes du gabarit.
- [ ] Marges de sécurité respectées sur les 4 côtés (voir `formats.md`).
- [ ] Zones d'interface libres (badge YouTube, haut/bas de story).
- [ ] Titre lisible à la taille réelle d'affichage : miniature testée à 160 px de large.
- [ ] Sens de lecture clair : titre → orateur → date-lieu → contacts, sans concurrence.
- [ ] Un seul bord d'alignement de référence.
- [ ] Export : RVB pour le web, CMJN 300 dpi + fond perdu 3 mm pour l'impression.

## Bloc F — Charte de sortie

- [ ] Note **exactement 2 lignes** (modèle + fond / polices + justification).
- [ ] Ligne « À vérifier » présente, 3 à 5 points actionnables.
- [ ] Une variante, étiquetée, un seul paramètre changé, présentée comme proposition.
- [ ] Aucune excuse, aucun historique, aucune note technique dans la sortie.

## Journal interne (non livré)

Pour chaque visuel, garder trace de : modèle utilisé, fond utilisé, duo de polices, hex réellement
employés, ratios de contraste mesurés, paramètre de la variante. Cela sert à reproduire un thème
et à répondre à une demande de retouche trois semaines plus tard.
