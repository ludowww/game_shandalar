extends RefCounted

const Deck = preload("res://scripts/battle/Deck.gd")

const ZONE_LIBRARY := "Bibliothèque"
const ZONE_HAND := "Main"
const ZONE_BATTLEFIELD := "Champ de bataille"
const ZONE_GRAVEYARD := "Cimetière"
const ZONE_LANDS := "Terrains"
const RESOURCE_MANA := "Mana générique"
const FUTURE_ZONE_LANDS := "Terrains (futur)"
const FUTURE_RESOURCE_MANA := "Mana (futur)"

var name := ""
var life := 20
var max_life := 20
var deck := Deck.new()
var library = deck
var hand: Array = []
var battlefield: Array = []
var graveyard: Array = []
var lands: Array = []
var current_mana := 0
var land_played_this_turn := false

func setup(combatant_name: String, starting_life: int, card_ids: Array) -> void:
	name = combatant_name
	life = starting_life
	max_life = starting_life
	library = deck
	library.setup(card_ids)
	hand = library.draw_many(3)
	battlefield = []
	graveyard = []
	lands = []
	current_mana = 0
	land_played_this_turn = false

func start_turn_resources() -> void:
	current_mana = total_mana_from_lands()
	land_played_this_turn = false

func total_mana_from_lands() -> int:
	var total := 0
	for land in lands:
		total += int(land.get("mana_value", 1))
	return total

func draw_card() -> void:
	var card = library.draw()
	if card != null:
		hand.append(card)

func play_card(card_index: int, card_database: Dictionary, target):
	if card_index < 0 or card_index >= hand.size():
		return null

	var card_id: String = hand.pop_at(card_index)
	var card: Dictionary = card_database.get(card_id, {}).duplicate()
	if card.is_empty():
		hand.insert(card_index, card_id)
		return null
	card["id"] = card_id

	if not can_play_card(card):
		hand.insert(card_index, card_id)
		return null

	if str(card.get("type", "")) == "land":
		play_land(card)
	elif str(card.get("type", "")) == "creature":
		pay_mana_for(card)
		summon_creature(card)
	else:
		pay_mana_for(card)
		apply_card_effect(card, target)
		move_to_graveyard(card_id)
	return card

func can_play_card(card: Dictionary) -> bool:
	if str(card.get("type", "")) == "land":
		return not land_played_this_turn
	return current_mana >= int(card.get("cost", 0))

func play_land(card: Dictionary) -> void:
	var land := {
		"id": str(card.get("id", "")),
		"name": str(card.get("name", "Terrain")),
		"mana_value": int(card.get("mana_value", 1))
	}
	lands.append(land)
	land_played_this_turn = true
	current_mana = total_mana_from_lands()

func pay_mana_for(card: Dictionary) -> void:
	current_mana -= int(card.get("cost", 0))
	current_mana = max(0, current_mana)

func summon_creature(card: Dictionary) -> void:
	var card_id := str(card.get("id", ""))
	var creature := {
		"id": card_id,
		"name": str(card.get("name", card_id)),
		"attack": int(card.get("attack", 0)),
		"health": int(card.get("health", 1)),
		"max_health": int(card.get("health", 1)),
		"summoning_sick": true
	}
	battlefield.append(creature)

func attack_with_creatures(target) -> int:
	var total_damage := 0
	for creature in battlefield:
		if bool(creature.get("summoning_sick", false)):
			continue
		total_damage += int(creature.get("attack", 0))
	if total_damage > 0:
		target.life = max(0, target.life - total_damage)
	return total_damage

func ready_creatures_for_next_turn() -> void:
	for creature in battlefield:
		if bool(creature.get("summoning_sick", false)):
			creature["summoning_sick"] = false

func move_to_graveyard(card_id: String) -> void:
	if card_id != "":
		graveyard.append(card_id)
		deck.discard(card_id)

func get_zone_summary() -> Dictionary:
	return {
		"library": library_size(),
		"hand": hand.size(),
		"battlefield": battlefield.size(),
		"graveyard": graveyard.size(),
		"lands": lands.size(),
		"mana": current_mana,
		"future_lands": FUTURE_ZONE_LANDS,
		"future_mana": FUTURE_RESOURCE_MANA
	}

func library_size() -> int:
	return library.library_size()

func apply_card_effect(card: Dictionary, target) -> void:
	match str(card.get("effect", "")):
		"damage":
			target.life = max(0, target.life - int(card.get("value", 0)))
		"heal":
			life = min(max_life, life + int(card.get("value", 0)))

func is_dead() -> bool:
	return life <= 0
