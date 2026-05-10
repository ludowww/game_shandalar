extends Control

signal reward_finished

const DataLoaderScript = preload("res://scripts/core/DataLoader.gd")

var data_loader := DataLoaderScript.new()
var card_database: Dictionary = {}
var rewards_by_pool: Dictionary = {}

@onready var status_label: Label = %StatusLabel
@onready var reward_choices: HBoxContainer = %RewardChoices

func _ready() -> void:
	show_rewards()

func show_rewards() -> void:
	card_database = build_card_database(data_loader.load_cards())
	rewards_by_pool = data_loader.load_rewards()

	for child in reward_choices.get_children():
		child.queue_free()

	var pool_id := GameState.pending_reward_pool
	var pool: Array = rewards_by_pool.get(pool_id, [])
	if pool.is_empty():
		status_label.text = "Aucune récompense disponible — retour carte."
		var back_button := Button.new()
		back_button.text = "Retour carte"
		back_button.pressed.connect(func(): reward_finished.emit())
		reward_choices.add_child(back_button)
		return

	status_label.text = "Choisis une récompense (%s)." % pool_id
	for i in range(min(3, pool.size())):
		var card_id := str(pool[i])
		var card: Dictionary = card_database.get(card_id, {})
		var button := Button.new()
		var card_text := "%s\n%s" % [str(card.get("name", card_id)), str(card.get("text", ""))]
		configure_card_button(button, card_text, card_text, Vector2(180, 120))
		button.pressed.connect(choose_reward.bind(card_id))
		reward_choices.add_child(button)

func configure_card_button(button: Button, text: String, tooltip: String, minimum_size: Vector2) -> void:
	button.custom_minimum_size = minimum_size
	button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	button.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	button.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	button.tooltip_text = tooltip
	button.text = text

func build_card_database(cards_data: Array) -> Dictionary:
	var result := {}
	for card in cards_data:
		result[str(card.get("id", ""))] = card
	return result

func choose_reward(card_id: String) -> void:
	GameState.add_card_to_deck(card_id)
	status_label.text = "Carte ajoutée : %s" % card_id
	reward_finished.emit()
