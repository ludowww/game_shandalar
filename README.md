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

## Prochains tickets

- T006 — détection rencontres
- T007 — données cartes/decks/ennemis
- T008 — moteur combat abstrait
- T009 — retour carte / victoire / défaite
- T010 — récompenses
- T011 — écran fin de run
- T012 — équilibrage V0
