# Adaptations par plateforme

Une seule source : `../prompts/system-prompt.md`. Toute adaptation doit conserver **la charte
verbatim** et **les 5 règles dures**. Si un outil n'a pas la place, on raccourcit les annexes
(specs), jamais la charte.

## 1. ChatGPT — Custom GPT

- Champ **Instructions** : coller intégralement le bloc de `system-prompt.md`.
- Champ **Conversation starters** :
  - « Nouveau visuel : voici mes 5 pièces jointes. »
  - « Décline ce thème en story + carré. »
  - « Vérifie ce visuel avant publication. »
- **Connaissances** : joindre `specs/formats.md`, `specs/palette.md`, `specs/typographie.md`,
  `specs/checklist.md`, `templates/brief.md`.
- Capacités : cocher *Code Interpreter* (mesure de contraste, calcul de dimensions) et
  *Image generation* si le rendu d'image est attendu. Sinon, l'agent produit des **spécifications
  de composition** exploitables telles quelles par un exécutant humain ou un autre outil.

## 2. Claude — Project

- **Instructions du projet** : le bloc de `system-prompt.md`.
- **Fichiers du projet** : les 4 specs + le formulaire de brief + la charte réelle de la structure
  (hex et règles), les modèles, les fonds, les photos.
- Ajouter en tête des instructions du projet : « La charte de la section 1 est immuable ; en cas
  de conflit avec un fichier du projet, la charte gagne. »

## 3. Gemini — Gem

- **Instructions** : le bloc de `system-prompt.md` (Gem tolère bien 8 000 caractères ; si la limite
  est atteinte, fusionner les tableaux de specs en puces).
- **Connaissances** : specs + charte.

## 4. Agent de code (Claude Code / agents de dépôt)

- Utiliser `AGENT.md` comme contexte permanent et `agent.yaml` comme configuration.
- Ordre de lecture imposé : `AGENT.md` → charte réelle → `specs/formats.md` → `specs/checklist.md`.
- La production d'image se fait avec l'outil disponible ; à défaut, l'agent génère un **SVG/HTML
  calibré** aux dimensions exactes, avec les hex de la charte, puis exporte en PNG. Cela garantit
  la palette stricte et des textes exacts — supérieur à la génération d'image pour les flyers
  textuels.

## 5. Passation à un exécutant humain (aucun outil IA)

L'agent produit une **fiche de composition** :

```text
Format : 1080×1350 · marges 72 px
Fond : aplat #0B2545 + texture F1 à 15 %
Titre : Anton 800, 118 px, interligne 0,95, #F7F4EC, 3 lignes max, fer à gauche à 72 px
Orateur : photo IMG_2041, buste, hauteur 62 % du cadre, masque progressif bas 18 %
Date-lieu : Rubik 600, 38 px, #E9B949, bloc bas gauche
Contacts : Rubik 400, 26 px, #F7F4EC, sur filet #E9B949 2 px
Contraste mesuré : titre 14,0:1 · contacts 11,8:1
```

## 6. Charte de validation avant mise en production

- [ ] La charte verbatim est présente, intacte, dans les instructions.
- [ ] Les 5 règles dures sont présentes.
- [ ] Le format de sortie immuable est présent (2 lignes de note, « À vérifier », variante).
- [ ] Les specs sont accessibles à l'agent (fichiers ou knowledge).
- [ ] Un test à blanc a été fait : brief incomplet → l'agent pose **une** question groupée.
- [ ] Un test de refus a été fait : demande hors palette → refus + alternative conforme.
