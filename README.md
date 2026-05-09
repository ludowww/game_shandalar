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

## Prochains tickets

- T003 — `DataLoader` JSON
- T004 — carte MVP 8x8
- T005 — déplacement joueur
- T006 — détection rencontres
- T007 — données cartes/decks/ennemis
- T008 — moteur combat abstrait
- T009 — retour carte / victoire / défaite
- T010 — récompenses
- T011 — écran fin de run
- T012 — équilibrage V0
