# Boîte à outils IA — le meilleur modèle accessible, et on le dit

> Règle 10 (AGENT.md § 3.10 et § 5quater). Principe unique : pour **chaque tâche**, on prend le
> meilleur modèle accessible, on **bascule automatiquement** vers le suivant s'il ne l'est pas, et
> **on annonce la bascule**. Un basculement silencieux est une faute, pas une économie.

## 1. Chaînes de préférence par tâche

| Tâche | 1. Payant haut de gamme | 2. Open source / local | 3. Repli manuel |
|---|---|---|---|
| **Fonds et effets** | modèle image haut de gamme | **Qwen-Image**, **FLUX.2 klein**, **Z-Image** | dégradé, halo, texture, grain — outillage du dépôt (`scripts/`) |
| **Édition d'image** | modèle d'édition payant | **Qwen-Image-Edit**, **FLUX.2 klein** | outils classiques : masque, couleur, composition |
| **Texte dans l'image** | modèle typographique dédié | **Qwen-Image** | **texte en couche de design** — voie par défaut |
| **Détourage** | suppression de fond par IA | détourage assisté + **contours vérifiés** | détourage manuel (masque, propagation, grabCut) |
| **Amélioration** | **upscaler IA** | upscaler classique (Lanczos + accentuation) | redimensionnement simple, annoncé |

Le classement est un **ordre d'essai**, pas une obligation d'achat : si le premier n'est pas
accessible, on prend le deuxième **et on le dit en une ligne**.

## 2. Texte : la couche de design est la voie par défaut

Tout texte qui porte une information — nom, titre, date, heure, lieu, contact, référence biblique,
mention obligatoire — est **composé typographiquement** (police embarquée, calage mesuré), jamais
généré par un modèle.

Raisons, dans l'ordre :

1. les **accents français** (`É`, `À`, `ç`, `œ`) sont la première chose qu'un modèle génératif rate ;
2. l'**orthographe** d'un nom propre ou d'une référence doit être exacte au caractère ;
3. la **répétabilité** : un texte composé se recompose à l'identique dans deux ans, pas une image
   générée.

Un modèle typographique peut servir d'**inspiration** de traitement (graisse, interlettrage,
déformation) ; le texte final reste une couche de design.

## 3. Le sujet est hors d'atteinte des modèles

Aucun modèle génératif ne touche le visage, la peau, les cheveux, les mains, la tenue ni les
proportions du prédicateur (`photos-sujet.md`). Le détourage peut être **assisté** par un modèle de
suppression de fond, mais les contours sont vérifiés à la main.

## 4. Annoncer — trois obligations

1. **L'outil choisi** : nom du modèle, ou « aucun » avec la raison.
2. **L'accès manquant** : clé absente, crédits épuisés, quota atteint, modèle retiré → une ligne,
   puis on bascule. Jamais de silence, jamais de « c'est fait » qui masque un repli.
3. **Le coût** : tout usage intensif (série de visuels, upscale de plusieurs fichiers, génération en
   boucle) est chiffré **avant** le lancement. Une estimation suffit ; l'absence d'estimation non.

Formulations types, à réutiliser telles quelles :

- « Qwen-Image n'est pas accessible ici (pas de clé) → fond composé manuellement (dégradé + halo),
  résultat équivalent pour ce cas. »
- « Upscale IA indisponible (crédits épuisés) → Lanczos + accentuation, contrôlé à 100 %. »
- « Aucun outil IA : texte en couche de design et détourage manuel, la silhouette est vérifiée. »
- « Usage intensif annoncé : 6 variantes de fond = 6 générations, coût estimé avant lancement. »

## 5. Registre des outils (à tenir à jour)

| Outil | Tâche | Accès | Statut | Dernier usage |
|---|---|---|---|---|
| composition typographique (Pillow + polices du dépôt) | texte, mise en page | local, libre | **disponible** | permanent |
| détourage manuel / assisté (masque, seuils, propagation) | détourage | local, libre | **disponible** | à chaque portrait |
| upscaler classique (Lanczos + accentuation) | agrandissement | local, libre | **disponible** | selon besoin |
| Qwen-Image / Qwen-Image-Edit | fonds, édition | open source, poids lourds | **non installé** | — |
| FLUX.2 klein | fonds, édition | open source | **non installé** | — |
| Z-Image | fonds | open source | **non installé** | — |
| modèles image / édition payants | fonds, édition | clé + crédits | **non configuré** | — |
| upscaler IA | agrandissement | selon service | **non configuré** | — |

« Non installé » et « non configuré » sont des états **légitimes** : ils se disent, ils ne se
cachent pas. La colonne « Dernier usage » sert à savoir ce qui a réellement tourné, sans quoi on finit
par raconter.

## 6. Ce que la note de sortie doit contenir

Ligne 2 de la note : `Outil IA : <nom ou « aucun, raison : … »> · Polices : …`.

Exemples conformes :

- `Outil IA : texte en couche de design (Pillow) + détourage manuel · Polices : …`
- `Outil IA : Qwen-Image-Edit (fond), texte en couche de design · Polices : …`
- `Outil IA : aucun, raison : pas de clé dans cet environnement → dégradé et halo composés · Polices : …`

Une note sans la mention de l'outil est **incomplète** : la réponse ne part pas.
