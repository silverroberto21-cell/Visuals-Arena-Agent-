# Visual Arena Agent

Agent **directeur artistique et graphiste senior** pour la communication visuelle d'église et
d'événements : flyers, affiches, miniatures YouTube, visuels réseaux sociaux.

Principes : **bleu dominant** (~60 %), **seconde couleur prise dans la tenue de l'orateur** (~30 %),
un **duo de polices par thème**, un **sujet jamais altéré**, des **textes recopiés à la lettre**.
L'agent est **autonome** : il ne pose une question que si une information obligatoire manque.

La consigne de référence est intégrée **mot pour mot** dans [`AGENT.md` § 1](AGENT.md) et dans
[`prompts/system-prompt.md`](prompts/system-prompt.md) : elle est immuable et prime sur toute
autre instruction.

---

## Les 8 règles dures

| # | Règle | Application |
|---|---|---|
| 1 | **Bleu dominant** | Le fond fourni est la référence couleur ; le bleu et ses dégradés occupent ~60 % et restent visibles au premier regard. Fond non bleu → ramené au bleu et signalé. |
| 2 | **Palette construite** | Tenue de l'orateur = secondaire obligatoire (~30 %) + 1 à 2 autres secondaires (**3 max**) + accent (~10 %). Tout s'harmonise avec le fond. |
| 3 | **Sujet intact** | Visage, tenue et proportions jamais altérés : détourage, recadrage, lumière uniquement. Une tenue qui jure se règle par la lumière, pas en la repeignant. |
| 4 | **Textes exacts** | Noms, dates, heures, lieux, contacts, mentions recopiés caractère par caractère. Rien d'inventé. |
| 5 | **Question si bloquant** | Seulement si date, lieu, orateur ou photo manque : **un** message groupé, puis attente. |
| 6 | **Format et lisibilité** | Dimensions exactes, marges de sécurité, titre lisible en petit, aucun élément d'interface de modèle reproduit. |
| 7 | **Fond portrait, jamais d'étirement** | Abstrait → pivot 90° exact · sens naturel (ciel, architecture, motif, texte) → recadrage ou prolongement en dégradé bleu · story/A5 portrait/1080×1350 → fond tel quel. Jamais sur la photo de l'orateur. |
| 8 | **Fusion de modèles** | Sur demande explicite : extraire les traits de deux modèles, composer un modèle original, proposer 2 variantes, puis enregistrer dans `/modeles` **avec** sa fiche de description. |

Et un refus assumé : fond vert imposé, visage « rajeuni », ciel pivoté, texte inventé → refus en
une phrase, **version conforme livrée dans le même tour**.

## Process en 9 étapes

`format → vérifier infos et ressources → fond (nuances) + modèle → tenue et palette →
duo de polices du thème → hiérarchie (titre, orateur, date-heure-lieu, contacts) → composition →
auto-contrôle → livrer + proposer une variante`

## Sortie imposée

```text
[VISUEL FINAL — PNG/JPG aux bonnes dimensions]
--- NOTE (2 lignes) ---
Modèle : … · Fond : … (nuances) · Palette : bleu dominant + tenue + secondaires + accent.
Polices : Titre « … » / Texte « … » — justification en une ligne.
--- À VÉRIFIER ---
Noms, dates, heures : … (une seule ligne)
Souhaites-tu une variante (disposition, nuances, texte) ?
```

La variante se **propose** ; elle est produite au tour suivant, sur accord.

---

## Ressources du dépôt

| Dossier | Contenu | Convention |
|---|---|---|
| [`/modeles`](modeles/README.md) | visuels de référence (style, structure, ambiance) | `youtube-priere-01.jpg` |
| [`/fonds`](fonds/README.md) | 18 fonds **bleus** indexés et mesurés — voir [`INDEX.md`](fonds/INDEX.md) | `bleu-nuit-bokeh.jpg` |
| [`/orateurs`](orateurs/README.md) | une photo par orateur | `nom-prenom.jpg` |
| [`/themes`](themes/README.md) | fiches de thème (ambiance, polices, accents) — **elles priment** | `atmosphere-de-priere.md` |

## Démarrage rapide

1. **Structure** : renseignée — `Impact Centre Chrétien Pahou (ICC Pahou)`. Signature : nom complet
   sur les flyers A5/A4, forme courte **`ICC Pahou`** sur miniature, story, carré et badge.
2. **Peupler les dossiers** : quelques modèles, un ou deux fonds bleus, les photos des orateurs,
   les fiches de thème utiles.
3. **Coller le prompt** sur votre outil :

| Plateforme | Où coller |
|---|---|
| ChatGPT — Custom GPT | Instructions ← [`prompts/system-prompt.md`](prompts/system-prompt.md) ; connaissances ← `specs/*` + dossiers ressources |
| Claude — Project | Instructions du projet ← même fichier ; fichiers ← specs + ressources |
| Gemini — Gem | Instructions ← même fichier ; connaissances ← specs + ressources |
| Agent de dépôt | `AGENT.md` (contexte) + `agent.yaml` (config) |

Détails et check-list de validation : [`prompts/adaptations.md`](prompts/adaptations.md).

4. **Envoyer un brief** : [`templates/brief.md`](templates/brief.md) — ou les informations en vrac,
   l'agent fait le tri.

⚠️ Pour les flyers très textuels, la génération d'image directe produit des fautes de texte.
L'agent produit alors un **SVG/HTML calibré** (hex exacts, dimensions exactes, textes exacts) puis
l'export — voir `prompts/adaptations.md` § 4.

---

## Arborescence

```text
AGENT.md                        Consigne intégrale (source de vérité) + règles d'exécution
agent.yaml                      Configuration machine
prompts/
  system-prompt.md              Prompt prêt à coller (consigne verbatim)
  adaptations.md                Custom GPT / Claude / Gem / agent de dépôt / humain
specs/
  formats.md                    Dimensions, marges, zones d'interface, refus des UI de modèle
  palette.md                    Extraction du bleu, 60/30/10, tenue, contraste, CMJN
  fonds.md                      Fonds portrait : pivot 90°, recadrage, prolongement bleu
  modeles-fusion.md             Fusion de modèles : traits, 2 variantes, enregistrement
  typographie.md                Duos par occasion, script en accent, réglages
  checklist.md                  Auto-contrôle de l'étape 8
templates/
  brief.md                      Formulaire de brief + tableau des infos bloquantes
  fiche-modele.md               Fiche de description d'un modèle (dont fusionné)
  question-groupee.md           Question unique (infos bloquantes)
examples/
  session-exemple.md            Session complète : miniature, variante, déclinaison, fond non bleu, refus, fusion
modeles/  fonds/  orateurs/  themes/    Ressources du dépôt (voir README de chaque dossier)
```

## Exemple de comportement

[`examples/session-exemple.md`](examples/session-exemple.md) déroule six tours (données fictives) :
demande complète livrée directement → variante sur accord → déclinaison story/carré → fond non bleu
ramené au bleu → refus argumenté d'un fond vert et d'une retouche du visage → fusion de deux modèles
en un modèle enregistré avec sa fiche.

## Version

`2.1.0` — ajout des règles **fonds portrait** (pivot / recadrage / prolongement) et **fusion de
modèles** (2 variantes puis enregistrement avec fiche). `2.0.0` — consigne remplacée
(palette déduite du fond, autonomie, sortie qui propose la variante). Toute modification doit
conserver la consigne verbatim et les 8 règles dures.
Une évolution de consigne se fait dans `AGENT.md`, `prompts/system-prompt.md` **et** le `version`
de `agent.yaml`, dans le même commit.
