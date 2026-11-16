#!/usr/bin/env python3
"""Vérifie que la consigne du commanditaire est reproduite mot pour mot.

Référence : le bloc ```text de la section 1 de `AGENT.md`.
Copie     : le bloc ```text de `prompts/system-prompt.md`, entre la ligne d'ouverture
            « === CONSIGNE … === » et la ligne « === FIN DE LA CONSIGNE === ».

La comparaison est exacte, ligne à ligne, espaces comprises. Les annexes qui suivent
« FIN DE LA CONSIGNE » ne font pas partie de la consigne : elles sont libres d'évoluer.

Code de sortie : 0 = identique · 1 = divergence (premier écart affiché).

Usage : python3 scripts/check_mirror.py [--quiet]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENT = ROOT / "AGENT.md"
PROMPT = ROOT / "prompts" / "system-prompt.md"

OPEN_MARK = "=== CONSIGNE"
CLOSE_MARK = "=== FIN DE LA CONSIGNE ==="


def first_text_block(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").split("\n")
    try:
        start = next(i for i, l in enumerate(lines) if l.strip().startswith("```text"))
    except StopIteration:
        raise SystemExit(f"{path.name} : aucun bloc ```text trouvé")
    for end in range(start + 1, len(lines)):
        if lines[end].strip() == "```":
            return lines[start + 1:end]
    raise SystemExit(f"{path.name} : bloc ```text non fermé")


def strip_blanks(lines: list[str]) -> list[str]:
    a, b = 0, len(lines)
    while a < b and not lines[a].strip():
        a += 1
    while b > a and not lines[b - 1].strip():
        b -= 1
    return lines[a:b]


def consigne_agent() -> list[str]:
    return strip_blanks(first_text_block(AGENT))


def consigne_prompt() -> list[str]:
    block = first_text_block(PROMPT)
    try:
        start = next(i for i, l in enumerate(block) if l.strip().startswith(OPEN_MARK))
    except StopIteration:
        raise SystemExit(f"{PROMPT.name} : ligne d'ouverture « {OPEN_MARK} » absente")
    try:
        end = next(i for i, l in enumerate(block) if l.strip() == CLOSE_MARK)
    except StopIteration:
        raise SystemExit(f"{PROMPT.name} : ligne « {CLOSE_MARK} » absente")
    return strip_blanks(block[start + 1:end])


def main() -> int:
    quiet = "--quiet" in sys.argv[1:]
    a, b = consigne_agent(), consigne_prompt()

    if a == b:
        if not quiet:
            print(f"OK — consigne identique ({len(a)} lignes, {sum(len(l) for l in a)} caractères) : "
                  "AGENT.md § 1 = prompts/system-prompt.md")
        return 0

    print(f"DIVERGENCE — AGENT.md § 1 : {len(a)} lignes · consigne de "
          f"prompts/system-prompt.md : {len(b)} lignes")
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else "<fin de la consigne AGENT.md>"
        y = b[i] if i < len(b) else "<fin de la consigne system-prompt.md>"
        if x != y:
            print(f"Premier écart, ligne {i + 1} de la consigne :")
            print(f"  AGENT.md          : {x!r}")
            print(f"  system-prompt.md  : {y!r}")
            break
    return 1


if __name__ == "__main__":
    sys.exit(main())
