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

	var card = player.play_card(card_index, card_database, enemy)
	if card == null:
		log_label.text = "Carte invalide."
		refresh_ui()
		return

	log_label.text = "Tu joues %s." % str(card.get("name", "Carte"))
	draw_player_card()
	resolve_creature_attack(player, enemy, "Tes")
	if check_battle_end():
		refresh_ui()
		return

	enemy_turn()
	refresh_ui()

func draw_player_card() -> void:
	player.draw_card()

func enemy_turn() -> void:
	enemy.draw_card()
	var card_index := ai.choose_card_index(enemy)
	if card_index == -1:
		log_label.text += "\n%s ne peut pas jouer." % enemy.name
		return

	var card = enemy.play_card(card_index, card_database, player)
	if card != null:
		log_label.text += "\n%s joue %s." % [enemy.name, str(card.get("name", "Carte"))]
	resolve_creature_attack(enemy, player, enemy.name)
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

	for child in hand_container.get_children():
		child.queue_free()

	for i in range(player.hand.size()):
		var card_id: String = player.hand[i]
		var card: Dictionary = card_database.get(card_id, {})
		var button := Button.new()
		button.text = "%s\n%s" % [str(card.get("name", card_id)), str(card.get("text", ""))]
		button.disabled = battle_finished_state
		button.pressed.connect(play_player_card.bind(i))
		hand_container.add_child(button)

func refresh_battlefield_ui() -> void:
	populate_battlefield(player_battlefield_container, player.battlefield)
	populate_battlefield(enemy_battlefield_container, enemy.battlefield)

func populate_battlefield(container: HBoxContainer, creatures: Array) -> void:
	for child in container.get_children():
		child.queue_free()
	for creature in creatures:
		var label := Label.new()
		label.custom_minimum_size = Vector2(120, 48)
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		label.text = "%s\n%d/%d" % [str(creature.get("name", "Créature")), int(creature.get("attack", 0)), int(creature.get("health", 0))]
		container.add_child(label)

func is_current_enemy_boss() -> bool:
	var enemy_data: Dictionary = enemies_by_id.get(GameState.current_enemy_id, {})
	return bool(enemy_data.get("is_boss", false))

func _on_return_button_pressed() -> void:
	battle_finished.emit()
