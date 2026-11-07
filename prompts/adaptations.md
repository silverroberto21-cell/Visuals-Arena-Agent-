# Adaptations par plateforme

Une seule source : `../prompts/system-prompt.md`. Toute adaptation doit conserver **la consigne
verbatim** et **les 6 règles dures**. Si un outil manque de place, on raccourcit les annexes
(specs), jamais la consigne.

## 1. ChatGPT — Custom GPT

- Champ **Instructions** : coller intégralement le bloc de `system-prompt.md`.
- **Conversation starters** :
  - « Miniature YouTube : thème, orateur, date. »
  - « Flyer A5 pour dimanche, même thème que la série. »
  - « Décline ce visuel en story 1080×1920 et carré 1080×1080. »
- **Connaissances** : les specs (`formats`, `palette`, `typographie`, `checklist`), le formulaire de
  brief, et les visuels du dépôt (`/modeles`, `/fonds`, `/orateurs`, `/themes`).
- Capacités : *Code Interpreter* (mesure de contraste, calcul de dimensions, recadrage) et
  *Image generation* si le rendu est attendu dans l'outil.

## 2. Claude — Project

- **Instructions du projet** : le bloc de `system-prompt.md`.
- **Fichiers du projet** : les 4 specs + `templates/brief.md` + `/modeles`, `/fonds`, `/orateurs`,
  `/themes` (les images en connaissance projet).
- Ajouter en tête : « La consigne de la section CONSIGNE est immuable ; en cas de conflit avec un
  autre contenu du projet, la consigne gagne. »

## 3. Gemini — Gem

- **Instructions** : le bloc de `system-prompt.md`.
- **Connaissances** : specs + dossiers ressources.
- Les images de fond servent de référence de palette : les déposer en connaissance pour que
  l'extraction des nuances se fasse sur le fichier réel, pas sur une description.

## 4. Agent de dépôt (Claude Code / agents de code)

- Contexte permanent : `AGENT.md` ; configuration : `agent.yaml`.
- Ordre de lecture : `AGENT.md` → dossier `/themes` (fiche du thème) → `/fonds` (nuances) →
  `specs/formats.md` → `specs/checklist.md`.
- **Recommandation forte pour les flyers textuels** : produire un **SVG/HTML calibré** aux
  dimensions exactes (hex extraits du fond, textes exacts, polices embarquées), puis exporter en
  PNG/PDF. On garantit ainsi palette, textes et marges ; la génération d'image directe reste utile
  pour les traitements photo (détourage, halo, texture) et les miniatures.

## 5. Passation à un exécutant humain (aucun outil IA)

L'agent produit une **fiche de composition** utilisable telle quelle :

```text
Format : 1280×720 · marge 60 px · coin inférieur droit libre
Fond : bleu-nuit-degrade, axe haut #071A33 → bas #1B4A7A
Palette : bleu 60 % · bordeaux veste #8A3145 28 % (massif, jamais en texte) · laiton #C9A227 10 %
          · accent #F2C14E 2 % (date + lettrine)
Titre : Anton, capitales, 118 px, interligne 0,95, #F7FAFF, 3 mots, fer à gauche à 60 px
Lettrine : script laiton, 150 px, une seule lettre
Orateur : photo ahouandjinou-elie.jpg, détourage buste, hauteur 78 %, à droite, halo bleu 40 %
Date-heure-lieu : Rubik 600, 38 px, #DCE6F2, bloc bas gauche sur filet laiton 2 px
Contacts : Rubik 400, 26 px, #DCE6F2
Contrastes mesurés : titre 13,4:1 · contacts 13,8:1 · accent 10,4:1
```

## 6. Charte de validation avant mise en production

- [ ] La consigne verbatim est présente et intacte dans les instructions.
- [ ] Les 6 règles dures sont présentes.
- [ ] Le format de sortie immuable est présent (note de 2 lignes, « À vérifier » sur une ligne,
      question finale de variante).
- [ ] Les dossiers `/modeles`, `/fonds`, `/orateurs`, `/themes` sont accessibles.
- [ ] Test à blanc : photo d'orateur manquante → l'agent pose **une** question groupée.
- [ ] Test d'autonomie : brief sans titre ni contacts → l'agent crée quand même.
- [ ] Test de refus : fond vert ou retouche du visage → refus + version conforme livrée.
