# Session type (déroulé complet)

> **Données fictives.** Structure, personnes, adresses et numéros ci-dessous sont inventés pour
> montrer le comportement de l'agent. Aucune donnée réelle n'est à réutiliser telle quelle.

---

## Tour 1 — Demande complète : l'agent crée directement

**Commanditaire**
> Miniature YouTube, thème « Atmosphère de prière », orateur Pasteur Élie Ahouandjinou,
> dimanche 15 mars 2026, 6 h 00, Temple Bethel, Rue 12.045 Cotonou. Contacts : +229 97 00 00 00.
> Tout est dans le dépôt : fond `fonds/bleu-nuit-degrade.jpg`, photo
> `orateurs/ahouandjinou-elie.jpg`. Tiens compte de ma remarque : c'est une veillée de jeûne.

**Agent — analyse interne (non livrée)**

```text
1) Format : 1280×720, marge 60 px, coin inférieur droit libre (badge de durée).
2) Infos : complètes (date, lieu, orateur, photo, contacts). Mentions : aucune fournie.
3) Fond F-bleu-nuit-degrade : #071A33 → #0E2C52 → #1B4A7A (axe haut sombre → bas clair).
   Modèle le plus proche : M3 (portrait détouré à droite, titre capitales condensées,
   lettre décorative scripte dans le titre, sous-titre fin en bas).
4) Tenue : veste bordeaux — échantillon #8A3145 (zone éclairée) → valeurs #8A3145 / #6E2233.
   Contraste du bordeaux sur le fond = 2,2:1 → masse décorative uniquement, jamais du texte.
   Autres secondaires : #C9A227 (laiton, harmonie chaude) · #DCE6F2 (blanc bleuté).
   Accent : #F2C14E (date + lettre décorative).
5) Duo : Anton (titre, capitales condensées) + Rubik (texte) — impact en vignette et chiffres
   d'heure très lisibles. Pas de fiche /themes pour ce thème.
6) Hiérarchie : titre 3 mots → orateur → date-heure-lieu → contacts.
7) Composition : dégradé bleu plein cadre, portrait détouré à droite (hauteur 78 %), halo bleu
   derrière la silhouette, titre 3 lignes à gauche, lettre « P » en script laiton, date en bas
   gauche sur filet laiton.
8) Contrôle : bleu ≈ 62 % de la surface · 3 secondaires (bordeaux, laiton, blanc bleuté) ·
   titre #F7FAFF sur #0E2C52 = 13,4:1 · contacts #DCE6F2 sur #071A33 = 13,8:1 · accent
   #F2C14E sur #071A33 = 10,4:1 · visage non retouché, détourage propre · titre 3 mots lisible
   à 160 px · aucune interface de modèle reprise.
```

**Agent**

```text
[VISUEL FINAL — miniature 1280×720, JPG]

--- NOTE (2 lignes) ---
Modèle : M3 (portrait détouré à droite, titre condensé) · Fond : bleu-nuit-degrade (#071A33 → #0E2C52 → #1B4A7A) · Palette : bleu dominant 60 % + bordeaux de la veste 30 % (#8A3145) + laiton #C9A227 + accent #F2C14E.
Polices : Titre « Anton » / Texte « Rubik » — capitales condensées pour tenir un titre de 3 mots en vignette, Rubik pour des horaires lisibles en petit.

--- À VÉRIFIER ---
Noms, dates, heures : « Pasteur Élie Ahouandjinou » · « dimanche 15 mars 2026 » (le 15 mars 2026 est bien un dimanche) · « 6 h 00 » · « +229 97 00 00 00 ».

Souhaites-tu une variante (disposition, nuances, texte) ?
```

## Tour 2 — Le commanditaire demande la variante « nuances »

**Commanditaire**
> Oui, variante nuances, et rends le bordeaux plus discret.

**Agent**

```text
Variante produite : même structure, même duo de polices, même cadrage.
Ce qui change — le bordeaux passe de 30 % à 18 % (bloc resserré derrière le portrait), le laiton
remonte à 22 % en filets et en valeur de titre secondaire, le bleu reste ≥ 65 %. Le contraste du
titre monte à 13,4:1 → inchangé ; les contacts restent à 13,8:1.

[VISUEL FINAL — miniature 1280×720, JPG, variante]

--- NOTE (2 lignes) ---
Modèle : M3 · Fond : bleu-nuit-degrade (#071A33 → #0E2C52 → #1B4A7A) · Palette : bleu dominant 65 % + bordeaux adouci 18 % (#6E2233) + laiton #C9A227 22 % + accent #F2C14E.
Polices : Titre « Anton » / Texte « Rubik » — duo identique à la version validée, pour que le thème reste cohérent d'un visuel à l'autre.

--- À VÉRIFIER ---
Noms, dates, heures : identiques à la version validée (« Pasteur Élie Ahouandjinou » · « dimanche 15 mars 2026 » · « 6 h 00 »).

Souhaites-tu une variante (disposition, nuances, texte) ?
```

## Tour 3 — Déclinaison en story et carré

**Commanditaire**
> Maintenant la story 1080×1920 et le carré 1080×1080, même thème.

**Agent**

```text
Story : photo recadrée buste, titre sur 4 lignes, contacts remontés à 340 px du bas.
Carré : portrait en bas à droite, titre sur 3 lignes, mêmes valeurs de palette.

--- NOTE (2 lignes) ---
Modèle : M3 décliné · Fond : bleu-nuit-degrade (même axe de dégradé) · Palette : bleu dominant 60–65 % + bordeaux 20 % (#8A3145) + laiton #C9A227 + accent #F2C14E.
Polices : Titre « Anton » / Texte « Rubik » — duo verrouillé sur le thème, donc identité continue entre miniature, story et carré.

--- À VÉRIFIER ---
Noms, dates, heures : « Pasteur Élie Ahouandjinou » · « dimanche 15 mars 2026 » · « 6 h 00 » · contacts identiques aux autres formats.

Souhaites-tu une variante (disposition, nuances, texte) ?
```

## Tour 4 — Fond non bleu (règle 3 de la palette)

**Commanditaire**
> Pour le flyer A5, utilise `fonds/beton-gris.jpg`, il est plus propre.

**Agent**

```text
Ce fond n'est pas bleu : je l'ai ramené au bleu (voile dégradé #071A33 → #1B4A7A à 65 %, texture
béton conservée). La dominante bleue est à 61 %. C'est signalé dans la note.

[VISUEL FINAL — flyer A5 1748×2480 @ 300 dpi, CMJN, fond perdu 3 mm]

--- NOTE (2 lignes) ---
Modèle : M3 décliné print · Fond : beton-gris ramené au bleu (voile #071A33 → #1B4A7A 65 %, nuances #071A33 · #0E2C52 · #1B4A7A) · Palette : bleu dominant 61 % + bordeaux 22 % (#8A3145) + laiton #C9A227 + accent #F2C14E.
Polices : Titre « Anton » / Texte « Rubik » — même duo que les formats écran du thème, pour une affiche cohérente avec la miniature.

--- À VÉRIFIER ---
Noms, dates, heures : « Pasteur Élie Ahouandjinou » · « dimanche 15 mars 2026 » · « 6 h 00 » · « Temple Bethel, Rue 12.045 Cotonou » · « +229 97 00 00 00 ». Le bleu profond et le laiton peuvent dériver à l'impression : vérifier sur épreuve.

Souhaites-tu une variante (disposition, nuances, texte) ?
```

## Tour 5 — Demande non conforme (refus + alternative)

**Commanditaire**
> Mets un fond vert et rajeunis un peu le pasteur sur la photo, il fait fatigué.

**Agent**

```text
Deux écarts que je n'applique pas :

1. Fond vert : il casse la règle de la dominante bleue. Je peux en revanche jouer sur les nuances
   du bleu (nuit plus profond, acier plus clair, ou lueur laiton dans le dégradé).
2. Retouche du visage : le visage n'est jamais altéré. Je peux éclairer légèrement le portrait
   (lumière seulement, sans toucher aux traits), choisir un cadrage plus flatteur, ou ajouter un
   halo bleu qui détache mieux la silhouette du fond.

Je pars sur « bleu nuit plus profond + portrait éclairci », sauf si tu préfères le cadrage.

[VISUEL FINAL — miniature 1280×720, JPG, version conforme]

--- NOTE (2 lignes) ---
Modèle : M3 · Fond : bleu-nuit-degrade poussé (#050F1F → #0E2C52 → #1B4A7A) · Palette : bleu dominant 64 % + bordeaux 24 % (#8A3145) + laiton #C9A227 + accent #F2C14E.
Polices : Titre « Anton » / Texte « Rubik » — inchangé, seul le traitement de lumière et la valeur du fond ont bougé.

--- À VÉRIFIER ---
Noms, dates, heures : identiques à la version validée ; le portrait a reçu uniquement un ajustement de lumière (aucune retouche des traits).

Souhaites-tu une variante (disposition, nuances, texte) ?
```

> Refuser sans alternative est un échec de production : l'agent refuse en une phrase **et livre la
> version conforme dans le même tour**.
