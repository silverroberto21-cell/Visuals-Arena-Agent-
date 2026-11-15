# Thème : ALERTE CODE R.O.U.G.E — les 5 clés pour vivre une chrétienne victorieuse

- **Intitulé (source, rectifié le 2026-11-07)** : « ALERTE CODE R.O.U.G.E : les 5 clés pour vivre
  une chrétienne victorieuse » — recopié à la lettre, points du mot-code compris. La forme
  précédente (« Les 5 clés pour vivre une vie chrétienne victorieuse : ROUGE ») est **remplacée**.
- **Occasion** : message d'enseignement / culte du dimanche (acrostiche R.O.U.G.E)
- **Ambiance** (2 mots) : urgence, clarté
- **Couleur imposée** : **ROUGE** — traité comme l'**accent** du visuel (~10 %) : le mot-code, les
  cinq lettres-clés et les filets. Jamais en fond : le bleu du fond reste la dominante (~85 %).
- **Duo de polices** : **Anton** (accroche, mot-code, verbes-clés — capitales condensées très
  grasses, lisibles à 320 px) + **Jost** (phrase du thème, gloses et références — géométrique, très
  lisible en petit)
  → *le mot-code doit se lire lettre par lettre d'un coup d'œil : un titre de caractère pour
  l'accroche et le code, une géométrique neutre pour tout le texte qui les accompagne.*
- **Script / lettrine** : aucune — l'accent du thème est **la couleur** et **la lettre**.
- **Accents** : rouge vif `#DE2638` (mot-code, lettres-clés), rouge clair `#FF6A60` (haut du
  dégradé), filets rouges, barre d'alerte à gauche de l'accroche ; acier `#B0D6F6` pour les gloses
  et la signature.
- **Traitement du fond** : FOND 6 (`f06-bleu-acier-texture.jpg`) — texture toile bleu acier,
  lumière rasante du coin haut droit, assombrie de 10 %, scrim vertical + halo cyan conservé ;
  souffle rouge très diffus dans l'angle bas gauche pour accorder l'accent.
- **Secondaires types** : acier clair `#B0D6F6` + cyan du fond `#0AB0D9` + blanc froid.
  Le rouge reste **unique** : aucun rouge de modèle, aucune couleur inventée.
- **À éviter** : peindre le fond en rouge (le bleu doit rester majoritaire), empiler les effets,
  séparer la lettre de son verbe, oublier une référence biblique, **écrire « ROUGE » sans ses
  points** — le mot-code est `R.O.U.G.E`.
- **Formats déjà servis** :
  - **visuel 1280 × 720** des cinq clés (`2026-11-07-visuel-alerte-code-rouge-1280x720.jpg`) ;
  - **miniature YouTube 1280 × 720** du thème seul, sans les points
    (`2026-11-07-miniature-alerte-code-rouge-theme-1280x720.jpg`) : accroche, mot-code, phrase du
    thème ; une clé filaire et cinq pastilles rouges disent le sujet sans un mot de plus ;
  - **miniatures avec l'orateur AP Enock** (détouré, à droite) : FOND 6 (`…-avec-ap-1280x720.jpg`)
    et FOND 26 ramené au bleu (`…-avec-ap-v2-fond26-1280x720.jpg`). Photo `_DSC3458` : plan large
    derrière un pupitre → **pupitre, Bible et écran coupés hors cadre**, silhouette entière.
  Les quatre sorties sont rendues par **un seul script** — `scripts/render_alerte_code_rouge.py` —
  pour que le bloc typographique ne diverge jamais d'un format à l'autre.

## Historique

| Date | Changement |
|---|---|
| 2026-11-07 | thème créé sous le titre « Les 5 clés pour vivre une vie chrétienne victorieuse : ROUGE » (acrostiche `R O U G E` sans points) — fichiers conservés, non réédités |
| 2026-11-07 | **rectification** : intitulé « ALERTE CODE R.O.U.G.E : les 5 clés pour vivre une chrétienne victorieuse ». Les quatre sorties sont rééditées sous de **nouveaux noms** ; les fichiers du titre précédent restent en place, jamais écrasés |
| 2026-11-07 | **photo et nom** : la photo `_DSC3458` remplace `_DSC3532` sur les deux miniatures avec l'orateur ; le nom s'écrit **« AP Enock »** (patronyme retiré sur demande). Détourage `orateurs/ap-enock-3458-detourage.png`, le pupitre ne sort pas |

## Réglages de référence (1280 × 720)

| Élément | Réglage |
|---|---|
| fond | FOND 6, `cover` 1280×720, flou 1,2 px, accentuation 70 %, luminosité ×0,86 |
| marque | `ICC PAHOU` Jost SemiBold 18 px, tracking 7, acier ; filet rouge 32 px + filet acier |
| accroche | « ALERTE CODE » Anton 64–68 px blanc, tracking 4, précédée d'une **barre d'alerte rouge** de 7 px |
| mot-code | « R.O.U.G.E » Anton 240 px (miniature) / 150 px (visuel), dégradé rouge clair → rouge foncé, ombre 28/160, interlettrage resserré de 2 px |
| filet d'accent | 4 px rouge sous le mot-code, longueur = largeur du mot plafonnée à 196 px |
| phrase | « les 5 clés pour vivre / une chrétienne victorieuse » Jost SemiBold 31–33 px blanc, tracking 1, césure à la frontière de sens |
| prédicateur | filet acier + « PRÉDICATEUR » Jost SemiBold 13 px tracking 6 + nom Jost SemiBold 25 px |
| clés (visuel) | lettre Anton 54 px rouge dégradée · verbe Anton 33 px blanc · glose Jost Regular 22 px acier · référence Jost SemiBold 21 px blanc, alignée à droite |
| rangées | 5 rangées de 112 px, filet acier 60 % au-dessus de chacune, filet de clôture 110 % |
| séparateur | filet vertical acier 34 % à x = 492 |
| légende | « ACROSTICHE · CINQ CLÉS » Jost Medium 14 px, tracking 3 (visuel seulement) |
| motif (miniature du thème) | clé filaire acier 466 × 192, épaisseur 13, rotation −15°, liseré rouge sur l'anneau + halo rouge ; cinq pastilles rouges alignées dessous |

## Déclinaisons avec l'orateur

La clé filaire cède sa place à **AP Enock** détouré, à droite (597 × 662, ancré au bord bas : le
détourage s'arrête au-dessus de la barre du pupitre). Colonne de texte inchangée, prédicateur ajouté en pied de
colonne. Deux fonds :

- **FOND 6** (v1) — la miniature du thème, avec AP ;
- **FOND 26** (v2) — diagonale bleu → rouge du fond fourni, reconstruite dans la palette (magenta
  recalé, diagonale rallumée par canaux).
