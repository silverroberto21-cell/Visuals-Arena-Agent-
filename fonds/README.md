# /fonds — images de fond

Les fonds sont la **référence couleur** de tous les visuels : ils sont toujours bleus ou en
dégradés de bleu.

## Convention de nommage

```text
<ambiance>-<variante>.jpg      ex. bleu-nuit-degrade.jpg
                               ex. bleu-acier-texture.jpg
                               ex. bleu-indigo-rayonnant.jpg
```

## Qualité attendue

- Résolution suffisante pour le plus grand format servi (≥ 2480 px sur le grand côté pour du A4
  à 300 dpi ; ≥ 1920 px pour une story).
- **Pas de texte incrusté** ni de logo dans le fond.
- Dégradé lisible : on doit pouvoir prélever 3 à 5 nuances distinctes (ombre, médian, lumière).

## Ce que l'agent fait du fond

1. Extrait 3 à 5 nuances (hex) qui deviennent la base de la palette.
2. Conserve l'axe du dégradé pour que la lumière du visuel reste cohérente.
3. Si le fond n'est pas franchement bleu, le ramène au bleu (teinte, voile, superposition) et le
   signale dans la note, ligne 1.

## Formats de référence

| Usage | Ratio | Taille mini |
|---|---|---|
| Miniature YouTube | 16:9 | 1280×720 |
| Post / flyer numérique | 4:5 | 1080×1350 |
| Story | 9:16 | 1080×1920 |
| Carré | 1:1 | 1080×1080 |
| Flyer A4 print | 1:1.414 | 2480×3508 |
