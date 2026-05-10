extends Node

const MAX_PLAYER_LIFE := 20
const STARTING_GOLD := 3

var player_position := Vector2i(1, 1)
var player_life := MAX_PLAYER_LIFE
var player_gold := STARTING_GOLD
var player_deck: Array = []
var defeated_encounters: Array = []
var used_special_tiles: Array = []
var current_enemy_id := ""
var current_tile_type := ""
var reward_pending := false
var pending_reward_pool := ""
var pending_shop_pool := ""
var pending_shop_cost := 0
var pending_shop_tile_key := ""
var last_battle_won := false
var run_finished := false
var run_won := false
var cards_added := 0

func reset_run() -> void:
	player_position = Vector2i.ZERO
	player_life = MAX_PLAYER_LIFE
	player_gold = STARTING_GOLD
	player_deck = []
	defeated_encounters = []
	used_special_tiles = []
	current_enemy_id = ""
	current_tile_type = ""
	reward_pending = false
	pending_reward_pool = ""
	pending_shop_pool = ""
	pending_shop_cost = 0
	pending_shop_tile_key = ""
	last_battle_won = false
	run_finished = false
	run_won = false
	cards_added = 0

func mark_encounter_defeated(encounter_id: String) -> void:
	if encounter_id != "" and not defeated_encounters.has(encounter_id):
		defeated_encounters.append(encounter_id)

func is_encounter_defeated(encounter_id: String) -> bool:
	return defeated_encounters.has(encounter_id)

func get_special_tile_key(grid_position: Vector2i) -> String:
	return "%d,%d" % [grid_position.x, grid_position.y]

func mark_special_tile_used(grid_position: Vector2i) -> void:
	mark_special_tile_key_used(get_special_tile_key(grid_position))

func mark_special_tile_key_used(tile_key: String) -> void:
	if tile_key != "" and not used_special_tiles.has(tile_key):
		used_special_tiles.append(tile_key)

func is_special_tile_used(grid_position: Vector2i) -> bool:
	return used_special_tiles.has(get_special_tile_key(grid_position))

func heal_player(amount: int) -> void:
	if amount <= 0:
		return
	player_life = min(MAX_PLAYER_LIFE, player_life + amount)

func can_afford(cost: int) -> bool:
	return player_gold >= cost

func spend_gold(cost: int) -> bool:
	if cost < 0 or not can_afford(cost):
		return false
	player_gold -= cost
	return true

func add_card_to_deck(card_id: String) -> void:
	if card_id == "":
		return
	player_deck.append(card_id)
	cards_added += 1
	reward_pending = false
	pending_reward_pool = ""
	last_battle_won = false

func finish_run(won: bool) -> void:
	run_finished = true
	run_won = won
