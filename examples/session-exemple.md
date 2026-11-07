# Session type (déroulé complet)

> **Données fictives.** Structure, personnes, adresses et numéros ci-dessous sont inventés pour
> montrer le comportement de l'agent. Aucune donnée réelle n'est à réutiliser telle quelle.

---

## Tour 1 — Brief incomplet (le commanditaire envoie des fichiers et trois lignes)

**Commanditaire**
> Voilà les modèles, deux fonds et la photo du pasteur. Fais-moi l'affiche pour la conférence de
> mars. Tu as la charte dans le drive.

**Agent (Visual Arena Agent)**

```text
Avant de créer, il me manque 4 éléments (une seule fois, promis) :

1. Format : flyer A5, A4, ou post 1080×1350 ? (à défaut, je livre en A5 print + 1080×1350)
2. Charte couleurs : je n'ai pas accès au Drive, envoie les hex + règles (à défaut, je propose
   4 couleurs à valider avant de créer).
3. L'événement, recopié tel quel : titre, thème, nom exact de l'orateur + sa qualité, date
   complète, heure, lieu, adresse, contacts.
4. Le texte exact des contacts à afficher (téléphone / WhatsApp / e-mail).

Réponds en vrac, je fais le tri.
```

## Tour 2 — Réponse complète

**Commanditaire**
> A5 pour l'impression, et 1080×1350 pour le feed.
> Palette : bleu nuit #0B2545, bleu profond #13315C, or #E9B949, blanc cassé #F7F4EC. Pas de
> dégradé coloré, pas de rouge.
> Conférence Alliance, thème « Une génération debout », orateur Pasteur Élie Ahouandjinou.
> Samedi 14 mars 2026, 17 h 00, Temple Bethel, Rue 12.045 Cotonou.
> Contacts : +229 97 00 00 00 · alliance@exemple.org

**Agent — note interne (non livrée)**

```text
1) Format : A5 1748×2480 @300 dpi + 1080×1350. Marges 8 mm / 72 px.
2) Infos : complètes. Jour/date à vérifier en sortie (14 mars 2026 = samedi, OK).
3) Modèle : M2 (titre en capitales condensées sur bandeau, orateur détaché à droite).
   Fond : F1 (texture papier sombre) recalé à 60 % de bleu nuit #0B2545.
4) Duo : Anton (titre) + Rubik (texte) — impact d'affiche, chiffres d'heure très lisibles.
5) Hiérarchie : titre → orateur → date-lieu → contacts.
6) Composition : bandeau or en haut 12 %, titre sur 3 lignes, orateur à droite sur masque
   progressif, bloc date-lieu en bas gauche, contacts sur filet or.
7) Contrôle : contraste titre blanc cassé #F7F4EC sur bleu nuit #0B2545 = 14,0:1 (OK, > 3:1).
   Contacts #F7F4EC sur #13315C = 11,8:1 (OK, > 4,5:1). Or #E9B949 réservé aux filets et à
   l'étiquette. Photo non retouchée (recadrage buste uniquement).
8) Variante : même duo, même photo, fond remplacé par aplat bleu nuit pur (plus sobre, plus
   lisible en petit).
```

**Agent — livraison**

```text
[VISUEL FINAL — A5 1748×2480 @300 dpi, CMJN, fond perdu 3 mm]
[VISUEL FINAL — 1080×1350 RVB, mêmes textes, mêmes polices]

--- NOTE (2 lignes) ---
Modèle : M2 (bandeau titre + orateur détaché) · Fond : F1 recalé en bleu nuit #0B2545.
Polices : Titre « Anton » / Texte « Rubik » — capitales condensées pour l'impact d'affiche, Rubik pour des heures et un numéro de téléphone lisibles à distance.

--- À VÉRIFIER ---
• Date : le brief dit « samedi 14 mars 2026 » — c'est bien un samedi, je confirme à l'identique.
• Orthographe du nom : « Élie Ahouandjinou » avec accent sur le É, comme dans ta source.
• Adresse : « Rue 12.045 Cotonou » recopiée telle quelle, sans ville complétée.
• Autorisation de diffusion de la photo du pasteur (je n'ai rien retouché : recadrage seul).
• Logo de la structure absent du brief : je l'ai laissé de côté, dis-moi s'il doit figurer.

--- VARIANTE PROPOSÉE ---
Variante A — même duo, même photo, fond remplacé par un aplat bleu nuit pur. Un seul paramètre
changé : plus sobre, meilleure lisibilité en vignette de téléphone et impression plus économique
en encre.
```

## Tour 3 — Déclinaison sur les autres formats

**Commanditaire**
> Parfait. Fais la story et le carré avec la même identité.

**Agent**

```text
Story 1080×1920 et carré 1080×1080, même duo (Anton + Rubik), même palette, même hiérarchie.
Différences imposées par le format : photo recadrée plus serré (buste), titre sur 4 lignes en
story, bloc contacts remonté à 340 px du bas pour rester au-dessus de l'interface.

--- NOTE (2 lignes) ---
Modèle : M2 décliné · Fond : F1 (story) et aplat #0B2545 (carré).
Polices : Titre « Anton » / Texte « Rubik » — duo identique au flyer, donc thème cohérent d'un format à l'autre.

--- À VÉRIFIER ---
• Titre sur 4 lignes en story : vérifier qu'aucun mot seul ne tombe en dernière ligne.
• Contacts : mêmes valeurs exactes que le flyer, corps maintenu à 28 px minimum.
• Zone basse < 320 px laissée libre (interface de la plateforme).

--- VARIANTE PROPOSÉE ---
Variante B — story avec la date en très gros corps sur la photo (au lieu du bloc bas gauche) :
renforce l'urgence en consultation rapide.
```

## Tour 4 — Demande non conforme (refus + alternative)

**Commanditaire**
> Mets le titre en rouge vif, ça ressortira mieux. Et lisse un peu le visage, il a l'air fatigué.

**Agent**

```text
Deux écarts par rapport à la charte, je ne les applique pas :

1. Rouge vif — hors palette (charte : #0B2545, #13315C, #E9B949, #F7F4EC) et le rouge est
   explicitement interdit. Pour faire ressortir le titre, je propose l'or #E9B949 sur bleu nuit
   (contraste 8,4:1) ou une taille de corps supérieure.
2. Lissage du visage — la photo de l'orateur n'est jamais retouchée. Je peux en revanche
   recadrer, éclaircir légèrement le fond derrière lui, ou choisir un cadrage plus flatteur.

Je pars sur la version or + fond éclairci, sauf si tu préfères l'augmentation de corps.
```

> Note : l'agent ne cède pas, mais il livre toujours une solution conforme dans le même tour —
> refuser sans alternative est un échec de production.
