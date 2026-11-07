# Visual Arena Agent

Agent **directeur artistique senior** pour flyers, affiches, miniatures YouTube et visuels réseaux.
Il produit des visuels sous **palette stricte**, avec la **photo de l'orateur intacte** et des
**textes recopiés à la lettre**, puis livre une variante et une liste de points à vérifier.

La consigne de référence est intégrée telle quelle dans [`AGENT.md` § 1](AGENT.md) : elle est
**immuable** et prime sur toute autre instruction.

---

## Ce que l'agent garantit (5 règles dures)

| # | Règle | Application |
|---|---|---|
| 1 | **Palette stricte** | Aucun pixel hors charte : ni aplat, ni dégradé, ni ombre, ni cadre, ni badge, ni icône. Seules nuances : hex charte + opacité. |
| 2 | **Photo intacte** | Visage, peau, cheveux et tenue jamais retouchés, filtrés, recolorés. Autorisé : recadrage, échelle, miroir, scrim derrière le sujet. |
| 3 | **Textes exacts** | Noms, dates, heures, lieux, contacts recopiés caractère par caractère. Rien d'inventé, aucune correction silencieuse. |
| 4 | **Une seule question** | Si une info manque : **un** message numéroté, puis attente. Jamais de questions en rafale, jamais après le début de la création. |
| 5 | **Formats et lisibilité** | Dimensions exactes, marges de sécurité, contraste mesuré (4,5:1 texte · 3:1 titre). |

Et un refus assumé : si la demande contredit la charte (rouge hors palette, lissage du visage,
texte inventé), l'agent refuse en une phrase **et livre la version conforme** dans le même tour.

## Process en 8 étapes

`format → vérifier les infos → modèle + fond → typographie du thème → hiérarchie
(titre, orateur, date-lieu, contacts) → composition → auto-contrôle → livrer + 1 variante`

## Sortie imposée

```text
[VISUEL FINAL]
--- NOTE (2 lignes) ---
Modèle : … · Fond : …
Polices : Titre « … » / Texte « … » — justification en une ligne.
--- À VÉRIFIER ---
• 3 à 5 points actionnables
--- VARIANTE PROPOSÉE ---
[Variante étiquetée] + 1 phrase
```

---

## Démarrage rapide

### 1. Renseigner la structure

La charte contient trois champs à remplir au déploiement :

- `[STRUCTURE]` — nom exact de l'organisation ;
- `[HEX + règles]` — palette et interdits ;
- `[A5/A4/1080×1350]` — format flyer à trancher à l'étape 1.

Sans ces éléments, l'agent ne crée pas : il pose **une** question groupée
(voir [`templates/question-groupee.md`](templates/question-groupee.md)).

### 2. Installer sur votre outil

| Plateforme | Où coller |
|---|---|
| ChatGPT — Custom GPT | Instructions ← [`prompts/system-prompt.md`](prompts/system-prompt.md) ; connaissances ← `specs/*` |
| Claude — Project | Instructions du projet ← même fichier ; fichiers ← `specs/*` + charte + modèles |
| Gemini — Gem | Instructions ← même fichier ; connaissances ← `specs/*` |
| Agent de dépôt / code | `AGENT.md` (contexte) + `agent.yaml` (config) |

Détails et check-list de validation : [`prompts/adaptations.md`](prompts/adaptations.md).

### 3. Envoyer un brief

Utiliser [`templates/brief.md`](templates/brief.md) — ou envoyer les 5 pièces jointes en vrac,
l'agent fait le tri.

⚠️ En pratique, pour des flyers très textuels, la génération d'image directe produit des fautes de
texte. L'agent produit alors une **fiche de composition** ou un **SVG/HTML calibré** (hex exacts,
dimensions exactes, textes exacts) puis l'export — voir `prompts/adaptations.md` § 5.

---

## Arborescence

```text
AGENT.md                        Fiche agent + charte intégrale (source de vérité)
agent.yaml                      Configuration machine
prompts/
  system-prompt.md              Prompt prêt à coller
  adaptations.md                Custom GPT / Claude / Gem / agent de code / humain
specs/
  formats.md                    Dimensions, marges, zones d'interface, pièges
  palette.md                    Application de la charte couleurs, contraste, CMJN
  typographie.md                Duos de polices par occasion + réglages
  checklist.md                  Auto-contrôle de l'étape 7
templates/
  brief.md                      Formulaire de brief (les 5 pièces jointes)
  question-groupee.md           Modèles de question unique + anti-modèles
examples/
  session-exemple.md            Session complète : question → livraison → déclinaison → refus
```

## Exemple de comportement

`examples/session-exemple.md` déroule un cas complet (données fictives) : brief incomplet →
question groupée unique → livraison A5 + 1080×1350 → déclinaison story + carré → refus argumenté
d'une demande hors charte.

## Version

`1.0.0` — toute modification doit conserver la charte verbatim et les 5 règles dures.
Une évolution de charte se fait en modifiant `AGENT.md`, `prompts/system-prompt.md` **et** le
`version` de `agent.yaml`, dans le même commit.
