extends Control

signal merchant_finished

const DataLoaderScript = preload("res://scripts/core/DataLoader.gd")

var data_loader := DataLoaderScript.new()
var card_database: Dictionary = {}
var rewards_by_pool: Dictionary = {}

@onready var status_label: Label = %StatusLabel
@onready var merchant_choices: HBoxContainer = %MerchantChoices

func _ready() -> void:
	show_shop()

func show_shop() -> void:
	card_database = build_card_database(data_loader.load_cards())
	rewards_by_pool = data_loader.load_rewards()

	for child in merchant_choices.get_children():
		child.queue_free()

	var pool_id := GameState.pending_shop_pool
	var pool: Array = rewards_by_pool.get(pool_id, [])
	status_label.text = "Marchand — %d or disponible, %d or par carte." % [GameState.player_gold, GameState.pending_shop_cost]

	if pool.is_empty():
		add_back_button("Aucun stock — Retour carte")
		return

	for i in range(min(3, pool.size())):
		var card_id := str(pool[i])
		var card: Dictionary = card_database.get(card_id, {})
		var button := Button.new()
		button.custom_minimum_size = Vector2(180, 108)
		button.text = "%s\n%s\nAcheter (%d or)" % [str(card.get("name", card_id)), str(card.get("text", "")), GameState.pending_shop_cost]
		button.disabled = not GameState.can_afford(GameState.pending_shop_cost)
		button.pressed.connect(buy_card.bind(card_id))
		merchant_choices.add_child(button)

	add_back_button("Retour carte")

func add_back_button(label: String) -> void:
	var back_button := Button.new()
	back_button.text = label
	back_button.custom_minimum_size = Vector2(160, 64)
	back_button.pressed.connect(func(): merchant_finished.emit())
	merchant_choices.add_child(back_button)

func build_card_database(cards_data: Array) -> Dictionary:
	var result := {}
	for card in cards_data:
		result[str(card.get("id", ""))] = card
	return result

func buy_card(card_id: String) -> void:
	if not GameState.can_afford(GameState.pending_shop_cost):
		status_label.text = "Pas assez d'or — Retour carte."
		return
	if not GameState.spend_gold(GameState.pending_shop_cost):
		status_label.text = "Achat impossible — Retour carte."
		return
	GameState.add_card_to_deck(card_id)
	GameState.mark_special_tile_key_used(GameState.pending_shop_tile_key)
	GameState.pending_shop_pool = ""
	GameState.pending_shop_cost = 0
	GameState.pending_shop_tile_key = ""
	status_label.text = "Achat : %s" % card_id
	merchant_finished.emit()
