extends RefCounted

const Deck = preload("res://scripts/battle/Deck.gd")

var name := ""
var life := 20
var max_life := 20
var deck := Deck.new()
var hand: Array = []

func setup(combatant_name: String, starting_life: int, card_ids: Array) -> void:
	name = combatant_name
	life = starting_life
	max_life = starting_life
	deck.setup(card_ids)
	hand = deck.draw_many(3)

func draw_card() -> void:
	var card = deck.draw()
	if card != null:
		hand.append(card)

func play_card(card_index: int, card_database: Dictionary, target):
	if card_index < 0 or card_index >= hand.size():
		return null

	var card_id: String = hand.pop_at(card_index)
	var card: Dictionary = card_database.get(card_id, {})
	if card.is_empty():
		return null

	apply_card_effect(card, target)
	return card

func apply_card_effect(card: Dictionary, target) -> void:
	match str(card.get("effect", "")):
		"damage":
			target.life = max(0, target.life - int(card.get("value", 0)))
		"heal":
			life = min(max_life, life + int(card.get("value", 0)))

func is_dead() -> bool:
	return life <= 0
