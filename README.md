# game_shandalar

Prototype V0 Godot inspiré de Shandalar.

## Objectif V0

Valider la boucle jouable minimale :

```txt
carte → déplacement → rencontre → combat abstrait → récompense → amélioration du deck → boss → fin de run
```

## Stack

- Godot 4
- GDScript
- Données JSON
- Prototype desktop 2D

## Scope actuel

### T001 — Initialisation projet

- Projet Godot créé
- Scène principale `scenes/main/Main.tscn`
- Placeholder visuel
- Arborescence initiale

### T002 — GameState global

- Script global `scripts/core/GameState.gd`
- Autoload `GameState` configuré dans `project.godot`
- État de run centralisé
- Fonction `reset_run()`

### T003 — DataLoader JSON

- Script global `scripts/core/DataLoader.gd`
- Autoload `DataLoader` configuré dans `project.godot`
- Chargement centralisé des fichiers JSON V0
- Helpers `load_cards()`, `load_decks()`, `load_enemies()`, `load_map()`, `load_rewards()`

### T004 — Carte MVP 8x8

- Données de carte `data/map_mvp.json`
- Scène `scenes/world/WorldMap.tscn`
- Script `scripts/world/WorldMap.gd`
- Affichage d'une grille 8x8 avec cases start/enemy/reward/boss
- `Main.tscn` instancie la carte V0

### T005 — Déplacement joueur

- Script `scripts/world/PlayerToken.gd`
- Token joueur affiché sur la grille
- Déplacement case par case avec flèches ou ZQSD
- Position synchronisée dans `GameState.player_position`
- Blocage aux limites de la carte

### T006 — Détection rencontres

- Détection des cases `enemy`, `boss`, `reward`, `empty`
- `GameState.current_enemy_id` défini sur les ennemis/boss
- `GameState.current_tile_type` suit le type de case courant
- `GameState.reward_pending` activé sur les cases récompense
- Feedback texte dans la carte pour préparer le branchement combat/récompense

### T007 — Données cartes/decks/ennemis

- Fichier `data/cards.json`
- Fichier `data/decks.json`
- Fichier `data/enemies.json`
- Cartes V0 : dégâts, soin, créatures abstraites
- Ennemis de la carte reliés à des decks existants

### T008 — Moteur combat abstrait

- Scène `scenes/battle/BattleScene.tscn`
- Scripts `Deck`, `Combatant`, `SimpleAI`, `BattleController`
- Main initiale de 3 cartes
- Effets V0 : dégâts et soin
- IA ennemie joue automatiquement la première carte disponible
- Victoire/défaite basique détectée

### T009 — Retour carte / victoire / défaite

- `Main.gd` route entre carte et combat
- Entrer sur ennemi/boss lance `BattleScene`
- Victoire marque l'ennemi comme vaincu
- Défaite termine la run
- Bouton retour carte après fin de combat

### T010 — Récompenses

- Fichier `data/rewards.json`
- Scène `scenes/reward/RewardScene.tscn`
- Script `scripts/reward/RewardController.gd`
- Après une victoire contre un ennemi normal, 3 cartes sont proposées
- Cliquer une carte l'ajoute au deck de run avant retour carte

### T011 — Écran fin de run

- Scène `scenes/ui/RunResult.tscn`
- Script `scripts/ui/RunResult.gd`
- Victoire boss ou défaite joueur affiche un écran de résultat
- Stats affichées : ennemis vaincus, cartes gagnées, PV restants
- Bouton `Recommencer` qui relance une run propre

## Prochains tickets

- T012 — équilibrage V0
