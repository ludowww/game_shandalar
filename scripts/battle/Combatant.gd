extends RefCounted

const Deck = preload("res://scripts/battle/Deck.gd")

var name := ""
var life := 20
var max_life := 20
var deck := Deck.new()
var hand: Array = []
var battlefield: Array = []
var graveyard: Array = []

func setup(combatant_name: String, starting_life: int, card_ids: Array) -> void:
	name = combatant_name
	life = starting_life
	max_life = starting_life
	deck.setup(card_ids)
	hand = deck.draw_many(3)
	battlefield = []
	graveyard = []

func draw_card() -> void:
	var card = deck.draw()
	if card != null:
		hand.append(card)

func play_card(card_index: int, card_database: Dictionary, target):
	if card_index < 0 or card_index >= hand.size():
		return null

	var card_id: String = hand.pop_at(card_index)
	var card: Dictionary = card_database.get(card_id, {}).duplicate()
	if card.is_empty():
		return null
	card["id"] = card_id

	if str(card.get("type", "")) == "creature":
		summon_creature(card)
	else:
		apply_card_effect(card, target)
		move_to_graveyard(card_id)
	return card

func summon_creature(card: Dictionary) -> void:
	var card_id := str(card.get("id", ""))
	var creature := {
		"id": card_id,
		"name": str(card.get("name", card_id)),
		"attack": int(card.get("attack", 0)),
		"health": int(card.get("health", 1)),
		"max_health": int(card.get("health", 1))
	}
	battlefield.append(creature)

func attack_with_creatures(target) -> int:
	var total_damage := 0
	for creature in battlefield:
		total_damage += int(creature.get("attack", 0))
	if total_damage > 0:
		target.life = max(0, target.life - total_damage)
	return total_damage

func move_to_graveyard(card_id: String) -> void:
	if card_id != "":
		graveyard.append(card_id)
		deck.discard(card_id)

func apply_card_effect(card: Dictionary, target) -> void:
	match str(card.get("effect", "")):
		"damage":
			target.life = max(0, target.life - int(card.get("value", 0)))
		"heal":
			life = min(max_life, life + int(card.get("value", 0)))

func is_dead() -> bool:
	return life <= 0
