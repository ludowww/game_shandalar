extends Node

const CARDS_PATH := "res://data/cards.json"
const DECKS_PATH := "res://data/decks.json"
const ENEMIES_PATH := "res://data/enemies.json"
const MAP_PATH := "res://data/map_mvp.json"
const REWARDS_PATH := "res://data/rewards.json"

func load_json_file(path: String):
	if not FileAccess.file_exists(path):
		push_error("DataLoader: JSON file not found: %s" % path)
		return null

	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("DataLoader: cannot open JSON file: %s" % path)
		return null

	var content := file.get_as_text()
	var data = JSON.parse_string(content)
	if data == null:
		push_error("DataLoader: invalid JSON file: %s" % path)
		return null

	return data

func load_cards():
	return load_json_file(CARDS_PATH)

func load_decks():
	return load_json_file(DECKS_PATH)

func load_enemies():
	return load_json_file(ENEMIES_PATH)

func load_map():
	return load_json_file(MAP_PATH)

func load_rewards():
	return load_json_file(REWARDS_PATH)
