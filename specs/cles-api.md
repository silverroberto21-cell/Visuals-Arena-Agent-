# Clés d'API et secrets — où ils vivent, où ils ne vivent JAMAIS

> Règle 12 (AGENT.md § 3.12). Une clé est un **laissez-passer** : elle ne se versionne pas, ne se cite
> pas, ne se colle pas dans une conversation. Ce document dit où la mettre pour qu'elle reste utile
> sans devenir un incident.

## 1. Règle en une phrase

La clé vit dans l'**environnement d'exécution** (gestionnaire de secrets), jamais dans le **contenu**
du projet. Le dépôt, lui, ne contient qu'un **modèle vide** : `.env.example`.

## 2. Où enregistrer les clés — par contexte

| Contexte | Emplacement correct | Détail |
|---|---|---|
| **Poste de travail / bac à sable** | fichier **`.env`** à la racine, **ignoré par Git** | chargé par l'environnement shell (`export`/`set -a; source .env`) ou par le script appelant ; jamais lu par le dépôt lui-même |
| **GitHub Actions / CI** | *Settings → Secrets and variables → Actions* | secrets de dépôt ou d'environnement, exposés en variables d'environnement au job ; jamais en clair dans le YAML |
| **Plateforme d'agent (Arena, hébergeur, orchestrateur)** | gestionnaire de secrets de la plateforme | saisie dans l'interface, injectée à l'exécution ; jamais recopiée dans un prompt |
| **Serveur / VPS** | gestionnaire de secrets système (`systemd` `EnvironmentFile=` avec permissions `600`, coffre type Vault, Doppler, 1Password CLI) | un fichier `.env` lisible par tous est un incident qui attend son heure |
| **Partage avec un exécutant humain** | canal chiffré, clé à durée limitée, révoquée après la mission | jamais par mail, jamais par capture d'écran, jamais dans un ticket |

Chemins **interdits** : `agent.yaml`, `prompts/`, `specs/`, `themes/`, `templates/`, `scripts/`,
`livrables/`, les notes de livraison, les messages de commit, les commentaires de code, la
conversation avec l'agent.

## 3. Le fichier `.env`

Modèle versionné : **`.env.example`** (noms de variables seuls, valeurs vides).
Fichier réel : **`.env`** — présent en local, **absent du dépôt**.

```bash
# .env (local, jamais commité)
QWEN_API_KEY=
FLUX_API_KEY=
IMAGE_API_KEY=
UPSCALER_API_KEY=
```

`.gitignore` doit contenir, au minimum :

```gitignore
.env
.env.*
!.env.example
__pycache__/
*.pyc
```

Une clé qui a **déjà** été commitée est une clé **compromise** : on la révoque et on en crée une
autre **avant** de nettoyer l'historique. Nettoyer l'historique sans révoquer ne protège rien.

## 4. Vérification avant chaque commit

```bash
git diff --cached | grep -nEi '(api[_-]?key|secret|token|bearer|sk-[a-z0-9]{16,})' && echo "STOP : secret probable"
```

Si la commande remonte quelque chose, on **retire la ligne**, on ne « renomme » pas la variable.

## 5. Ce que l'agent doit répondre quand une clé manque

Une seule ligne, factuelle, puis la bascule (`outils-ia.md` § 4) :

> « Modèle payant indisponible ici (aucune clé dans cet environnement) → repli sur <solution locale>,
> résultat conforme pour ce visuel. »

On ne demande **jamais** à l'utilisateur de coller sa clé dans la conversation. On lui indique **où**
la mettre (tableau § 2) et on continue avec le repli.

## 6. Coût et crédits

- Une clé n'est pas un budget : les **crédits** sont vérifiés avant un usage intensif.
- Un usage intensif (série, upscale multiple, génération en boucle) est **chiffré avant**.
- Un dépassement se signale en une ligne, sans dramatiser et sans masquer le repli.
- Aucune clé de facturation n'est stockée dans le dépôt, même « juste pour tester ».
