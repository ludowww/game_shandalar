extends Control

signal battle_finished

const DataLoaderScript = preload("res://scripts/core/DataLoader.gd")
const Deck = preload("res://scripts/battle/Deck.gd")
const Combatant = preload("res://scripts/battle/Combatant.gd")
const SimpleAI = preload("res://scripts/battle/SimpleAI.gd")
const ATTACK_LOG_TEXT := "créatures attaquent"

var card_database: Dictionary = {}
var enemies_by_id: Dictionary = {}
var decks: Dictionary = {}
var player := Combatant.new()
var enemy := Combatant.new()
var ai := SimpleAI.new()
var battle_finished_state := false
var data_loader := DataLoaderScript.new()

@onready var player_life_label: Label = %PlayerLifeLabel
@onready var enemy_life_label: Label = %EnemyLifeLabel
@onready var enemy_name_label: Label = %EnemyNameLabel
@onready var player_battlefield_container: HBoxContainer = %PlayerBattlefieldContainer
@onready var enemy_battlefield_container: HBoxContainer = %EnemyBattlefieldContainer
@onready var magic_zones_label: Label = %MagicZonesLabel
@onready var mana_label: Label = %ManaLabel
@onready var hand_container: HBoxContainer = %HandContainer
@onready var log_label: Label = %LogLabel
@onready var return_button: Button = %ReturnButton

func _ready() -> void:
	return_button.pressed.connect(_on_return_button_pressed)
	return_button.visible = false
	start_battle(GameState.current_enemy_id)

func start_battle(enemy_id: String) -> void:
	battle_finished_state = false
	GameState.last_battle_won = false
	card_database = build_card_database(data_loader.load_cards())
	decks = data_loader.load_decks()
	enemies_by_id = build_enemy_database(data_loader.load_enemies())

	var enemy_data: Dictionary = enemies_by_id.get(enemy_id, {})
	if enemy_data.is_empty():
		log_label.text = "Erreur : ennemi inconnu %s" % enemy_id
		return_button.visible = true
		return

	var player_deck_ids: Array = GameState.player_deck
	if player_deck_ids.is_empty():
		player_deck_ids = decks.get("player_start", [])
		GameState.player_deck = player_deck_ids.duplicate()

	player.setup("Joueur", GameState.player_life, player_deck_ids)
	enemy.setup(str(enemy_data.get("name", enemy_id)), int(enemy_data.get("life", 10)), decks.get(str(enemy_data.get("deck_id", "")), []))
	player.start_turn_resources()
	enemy.start_turn_resources()
	log_label.text = "Combat contre %s" % enemy.name
	refresh_ui()

func build_card_database(cards_data: Array) -> Dictionary:
	var result := {}
	for card in cards_data:
		result[str(card.get("id", ""))] = card
	return result

func build_enemy_database(enemies_data: Array) -> Dictionary:
	var result := {}
	for enemy_data in enemies_data:
		result[str(enemy_data.get("id", ""))] = enemy_data
	return result

func play_player_card(card_index: int) -> void:
	if battle_finished_state:
		return

	player.start_turn_resources()
	var card = player.play_card(card_index, card_database, enemy)
	if card == null:
		log_label.text = "Mana insuffisant ou terrain déjà joué."
		refresh_ui()
		return

	log_label.text = "Tu joues %s." % str(card.get("name", "Carte"))
	draw_player_card()
	resolve_creature_attack(player, enemy, "Tes")
	player.ready_creatures_for_next_turn()
	if check_battle_end():
		refresh_ui()
		return

	enemy_turn()
	refresh_ui()

func draw_player_card() -> void:
	player.draw_card()

func enemy_turn() -> void:
	enemy.start_turn_resources()
	enemy.draw_card()
	var card_index := ai.choose_card_index(enemy, card_database)
	if card_index == -1:
		log_label.text += "\n%s ne peut pas jouer." % enemy.name
	else:
		var card = enemy.play_card(card_index, card_database, player)
		if card != null:
			log_label.text += "\n%s joue %s." % [enemy.name, str(card.get("name", "Carte"))]
	resolve_creature_attack(enemy, player, enemy.name)
	enemy.ready_creatures_for_next_turn()
	check_battle_end()

func resolve_creature_attack(attacker, defender, attacker_label: String) -> void:
	var damage: int = attacker.attack_with_creatures(defender)
	if damage > 0:
		log_label.text += "\n%s %s pour %d." % [attacker_label, ATTACK_LOG_TEXT, damage]

func check_battle_end() -> bool:
	if enemy.is_dead():
		battle_finished_state = true
		GameState.last_battle_won = true
		GameState.player_life = player.life
		GameState.mark_encounter_defeated(GameState.current_enemy_id)
		if is_current_enemy_boss():
			GameState.pending_reward_pool = ""
			GameState.finish_run(true)
			log_label.text += "\nVictoire finale."
		else:
			log_label.text += "\nVictoire."
		return_button.visible = true
		return true
	if player.is_dead():
		battle_finished_state = true
		GameState.last_battle_won = false
		GameState.player_life = 0
		GameState.finish_run(false)
		log_label.text += "\nDéfaite."
		return_button.visible = true
		return true
	return false

func refresh_ui() -> void:
	player_life_label.text = "Joueur : %d PV" % player.life
	enemy_life_label.text = "%s : %d PV" % [enemy.name, enemy.life]
	enemy_name_label.text = enemy.name
	refresh_battlefield_ui()
	refresh_zone_summary_ui()
	refresh_mana_ui()

	for child in hand_container.get_children():
		child.queue_free()

	for i in range(player.hand.size()):
		var card_id: String = player.hand[i]
		var card: Dictionary = card_database.get(card_id, {})
		var button := Button.new()
		var cost := int(card.get("cost", 0))
		var card_text := "%s\nCoût: %d\n%s" % [str(card.get("name", card_id)), cost, str(card.get("text", ""))]
		configure_card_button(button, card_text, card_text, Vector2(180, 132))
		button.disabled = battle_finished_state or not player.can_play_card(card)
		button.pressed.connect(play_player_card.bind(i))
		hand_container.add_child(button)

func configure_card_button(button: Button, text: String, tooltip: String, minimum_size: Vector2) -> void:
	button.custom_minimum_size = minimum_size
	button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	button.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	button.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	button.tooltip_text = tooltip
	button.text = text

func refresh_battlefield_ui() -> void:
	populate_battlefield(player_battlefield_container, player.battlefield)
	populate_battlefield(enemy_battlefield_container, enemy.battlefield)

func refresh_zone_summary_ui() -> void:
	var player_zones: Dictionary = player.get_zone_summary()
	var enemy_zones: Dictionary = enemy.get_zone_summary()
	magic_zones_label.text = "Zones Magic — Joueur: Bibliothèque %d | Main %d | Champ de bataille %d | Cimetière %d | Terrains %d\nEnnemi: Bibliothèque %d | Main %d | Champ de bataille %d | Cimetière %d | Terrains %d" % [
		int(player_zones.get("library", 0)),
		int(player_zones.get("hand", 0)),
		int(player_zones.get("battlefield", 0)),
		int(player_zones.get("graveyard", 0)),
		int(player_zones.get("lands", 0)),
		int(enemy_zones.get("library", 0)),
		int(enemy_zones.get("hand", 0)),
		int(enemy_zones.get("battlefield", 0)),
		int(enemy_zones.get("graveyard", 0)),
		int(enemy_zones.get("lands", 0))
	]

func refresh_mana_ui() -> void:
	mana_label.text = "Mana joueur: %d | Terrains joueur: %d\nMana ennemi: %d | Terrains ennemi: %d" % [
		player.current_mana,
		player.lands.size(),
		enemy.current_mana,
		enemy.lands.size()
	]

func populate_battlefield(container: HBoxContainer, creatures: Array) -> void:
	for child in container.get_children():
		child.queue_free()
	for creature in creatures:
		var label := Label.new()
		label.custom_minimum_size = Vector2(120, 64)
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		var status := ""
		if bool(creature.get("summoning_sick", false)):
			status = "\nMal d'invocation"
		label.text = ("%s\n%d/%d" % [str(creature.get("name", "Créature")), int(creature.get("attack", 0)), int(creature.get("health", 0))]) + status
		container.add_child(label)

func is_current_enemy_boss() -> bool:
	var enemy_data: Dictionary = enemies_by_id.get(GameState.current_enemy_id, {})
	return bool(enemy_data.get("is_boss", false))

func _on_return_button_pressed() -> void:
	battle_finished.emit()
