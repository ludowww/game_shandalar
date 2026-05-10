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

### T012 — Carte aventure Shandalar-like

- Carte agrandie en 15x9 (`theme: shandalar_adventure_v1`)
- Lieux visibles : départ, ennemis faibles, ennemis moyens, boss, villages, sanctuaires, trésors
- Légende intégrée et symboles sur les cases pour une lecture immédiate
- Données JSON enrichies (`label`, `description`, `danger`, `legend`)
- Ennemis supplémentaires reliés aux decks existants pour éviter les doublons d'ID sur la carte
- Boucle existante conservée : carte → combat → récompense → retour carte → boss → fin

### T013 — Lieux spéciaux interactifs

- Village : repos simple, rend quelques PV une seule fois
- Sanctuaire : restauration complète une seule fois
- Trésor : ouvre directement une récompense de carte via la scène existante
- `GameState` suit les lieux spéciaux déjà utilisés pour éviter le farming
- Pas encore de vraie économie, pas de quêtes, pas de déplacement ennemi

### T014 — Marchand simple

- Les villages deviennent des marchands simples
- Le joueur démarre avec un petit or de départ (`3`)
- Un marchand propose 3 cartes issues d'un pool existant
- achat simple : payer l'or, ajouter la carte au deck, retour carte
- Le marchand est marqué utilisé après achat pour éviter le farming
- Pas de vraie économie avancée : pas de vente, pas de prix dynamiques, pas d'inventaire complexe

### T015 — Feedback UI carte aventure

- Ajout d'un HUD carte : PV, or, ennemis vaincus, cartes gagnées
- Ajout d'un panneau détail qui explique le lieu courant
- Messages clarifiés pour ennemis faibles/moyens, boss, marchand, sanctuaire et trésor
- Les lieux déjà utilisés et ennemis vaincus sont grisés avec une coche
- La carte indique mieux ce qui reste utile, dangereux ou déjà consommé

### T016 — Créatures persistantes

- Les cartes créature deviennent des permanents sur le champ de bataille
- Une créature conserve nom, attaque et endurance/vie
- Les sorts restent des effets immédiats puis vont au cimetière/défausse
- Les créatures du joueur attaquent automatiquement l'ennemi à chaque tour
- Les créatures ennemies attaquent automatiquement le joueur à chaque tour
- Le combat affiche les créatures en jeu côté joueur et côté ennemi
- Les zones restent compatibles avec l'évolution Magic : deck/bibliothèque, main, champ de bataille, cimetière/défausse

### T016b — Mal d’invocation

- Une créature invoquée arrive avec le mal d’invocation
- Elle est ignorée par l’attaque automatique du tour où elle arrive en jeu
- Le mal d’invocation est levé après le tour de son contrôleur, pour attaquer au prochain tour
- L’UI du champ de bataille affiche un feedback simple `Mal d'invocation`
- Pas de célérité, mana, blocage, pile, priorité ou phases Magic complètes

### T017 — Zones Magic explicites

- Les zones du duel sont formalisées : Bibliothèque, Main, Champ de bataille, Cimetière
- Le script de combat expose un résumé des zones pour préparer les règles Magic futures
- Les créatures restent dirigées vers le Champ de bataille
- Les sorts restent des effets immédiats puis vont au Cimetière
- L’UI du duel affiche les compteurs de zones joueur/ennemi
- Des hooks nommés préparent Terrains et Mana sans les implémenter encore
- Pas de mana, terrains, phases complètes, blocage manuel, pile ou priorité

## Prochains tickets

- T018 — équilibrage V1
