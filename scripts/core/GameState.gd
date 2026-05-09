extends Node

var player_position := Vector2i(1, 1)
var player_life := 20
var player_deck: Array = []
var defeated_encounters: Array = []
var current_enemy_id := ""
var run_finished := false
var run_won := false
var cards_added := 0

func reset_run() -> void:
	player_position = Vector2i(1, 1)
	player_life = 20
	player_deck = []
	defeated_encounters = []
	current_enemy_id = ""
	run_finished = false
	run_won = false
	cards_added = 0

func mark_encounter_defeated(encounter_id: String) -> void:
	if encounter_id != "" and not defeated_encounters.has(encounter_id):
		defeated_encounters.append(encounter_id)

func is_encounter_defeated(encounter_id: String) -> bool:
	return defeated_encounters.has(encounter_id)

func finish_run(won: bool) -> void:
	run_finished = true
	run_won = won
