extends Control

signal battle_requested
signal reward_requested

const DataLoaderScript = preload("res://scripts/core/DataLoader.gd")
const TILE_SIZE := 44
const TILE_GAP := 4
const TILE_COLORS := {
	"empty": Color(0.10, 0.13, 0.16, 1.0),
	"start": Color(0.20, 0.50, 0.90, 1.0),
	"enemy_weak": Color(0.74, 0.40, 0.22, 1.0),
	"enemy_medium": Color(0.78, 0.18, 0.16, 1.0),
	"village": Color(0.22, 0.58, 0.36, 1.0),
	"sanctuary": Color(0.35, 0.72, 0.85, 1.0),
	"treasure": Color(0.95, 0.72, 0.20, 1.0),
	"boss": Color(0.55, 0.18, 0.75, 1.0)
}
const TILE_SYMBOLS := {
	"empty": "·",
	"start": "S",
	"enemy_weak": "g",
	"enemy_medium": "M",
	"village": "V",
	"sanctuary": "+",
	"treasure": "T",
	"boss": "B"
}

var map_width := 0
var map_height := 0
var current_map_data: Dictionary = {}
var enemies_by_id: Dictionary = {}

@onready var grid: GridContainer = %MapGrid
@onready var status_label: Label = %StatusLabel
@onready var player_token: ColorRect = %PlayerToken
@onready var legend_box: VBoxContainer = %LegendBox

var data_loader := DataLoaderScript.new()

func _ready() -> void:
	var map_data = data_loader.load_map()
	if map_data == null:
		status_label.text = "Erreur : impossible de charger data/map_mvp.json"
		return

	enemies_by_id = build_enemy_database(data_loader.load_enemies())
	current_map_data = map_data
	build_grid(map_data)
	build_legend(map_data)
	var start_position: Array = map_data.get("start_position", [1, 4])
	if GameState.player_position == Vector2i.ZERO:
		GameState.player_position = Vector2i(int(start_position[0]), int(start_position[1]))
	player_token.set_grid_position(GameState.player_position)
	refresh_after_battle_if_needed()
	if status_label.text == "Chargement de la carte...":
		status_label.text = "Carte aventure chargée — explore librement, choisis ta route, puis défie le boss."

func _unhandled_input(event: InputEvent) -> void:
	if event.is_echo():
		return

	if Input.is_action_just_pressed("move_up"):
		try_move_player(Vector2i.UP)
	elif Input.is_action_just_pressed("move_down"):
		try_move_player(Vector2i.DOWN)
	elif Input.is_action_just_pressed("move_left"):
		try_move_player(Vector2i.LEFT)
	elif Input.is_action_just_pressed("move_right"):
		try_move_player(Vector2i.RIGHT)

func build_grid(map_data: Dictionary) -> void:
	map_width = int(map_data.get("width", 0))
	map_height = int(map_data.get("height", 0))
	grid.columns = map_width

	for child in grid.get_children():
		child.queue_free()

	for y in range(map_height):
		for x in range(map_width):
			var tile_type := get_tile_type(map_data, x, y)
			var tile_data := get_tile_at_coordinates(map_data, x, y)
			var tile := build_tile_control(tile_type, tile_data, x, y)
			grid.add_child(tile)

func build_tile_control(tile_type: String, tile_data: Dictionary, x: int, y: int) -> PanelContainer:
	var tile := PanelContainer.new()
	tile.custom_minimum_size = Vector2(TILE_SIZE, TILE_SIZE)
	tile.tooltip_text = "%s — %s (%d, %d)" % [tile_data.get("label", tile_type), tile_data.get("description", ""), x, y]

	var style := StyleBoxFlat.new()
	style.bg_color = get_tile_color(tile_type)
	style.corner_radius_top_left = 6
	style.corner_radius_top_right = 6
	style.corner_radius_bottom_left = 6
	style.corner_radius_bottom_right = 6
	style.border_width_left = 1
	style.border_width_top = 1
	style.border_width_right = 1
	style.border_width_bottom = 1
	style.border_color = Color(0.85, 0.90, 0.95, 0.20)
	tile.add_theme_stylebox_override("panel", style)

	var symbol := Label.new()
	symbol.text = TILE_SYMBOLS.get(tile_type, "·")
	symbol.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	symbol.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	symbol.add_theme_font_size_override("font_size", 20)
	symbol.add_theme_color_override("font_color", Color(1, 1, 1, 0.95))
	tile.add_child(symbol)
	return tile

func build_legend(map_data: Dictionary) -> void:
	for child in legend_box.get_children():
		child.queue_free()

	var title := Label.new()
	title.text = "Légende"
	title.add_theme_font_size_override("font_size", 18)
	legend_box.add_child(title)

	for entry in map_data.get("legend", []):
		var line := Label.new()
		line.text = "%s  %s — %s" % [entry.get("symbol", "?"), entry.get("label", entry.get("type", "")), entry.get("description", "")]
		line.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		legend_box.add_child(line)

func try_move_player(delta: Vector2i) -> void:
	var next_position := GameState.player_position + delta
	if not is_inside_map(next_position):
		return

	player_token.set_grid_position(next_position)
	handle_tile_entered(next_position)

func handle_tile_entered(grid_position: Vector2i) -> void:
	var tile := get_tile_at_position(grid_position)
	var tile_type := str(tile.get("type", "empty"))
	var interaction_type := get_interaction_type(tile_type)
	GameState.current_tile_type = interaction_type
	GameState.reward_pending = false

	match interaction_type:
		"enemy":
			GameState.current_enemy_id = str(tile.get("enemy_id", ""))
			if GameState.is_encounter_defeated(GameState.current_enemy_id):
				status_label.text = "Rencontre déjà vaincue : %s" % GameState.current_enemy_id
			else:
				var enemy_data := get_enemy_data(GameState.current_enemy_id)
				GameState.pending_reward_pool = str(tile.get("reward_pool", ""))
				if GameState.pending_reward_pool == "":
					GameState.pending_reward_pool = str(enemy_data.get("reward_pool", ""))
				status_label.text = "%s : %s" % [tile.get("label", "Rencontre"), GameState.current_enemy_id]
				battle_requested.emit()
		"boss":
			GameState.current_enemy_id = str(tile.get("enemy_id", ""))
			if GameState.is_encounter_defeated(GameState.current_enemy_id):
				status_label.text = "Boss déjà vaincu : %s" % GameState.current_enemy_id
			else:
				GameState.pending_reward_pool = ""
				status_label.text = "Boss final : %s" % GameState.current_enemy_id
				battle_requested.emit()
		"reward", "village", "sanctuary":
			handle_special_tile(tile, grid_position)
		_:
			GameState.current_enemy_id = ""
			status_label.text = "Position joueur : (%d, %d)" % [grid_position.x, grid_position.y]

func handle_special_tile(tile: Dictionary, grid_position: Vector2i) -> void:
	GameState.current_enemy_id = ""
	var label := str(tile.get("label", "Lieu spécial"))
	if bool(tile.get("one_shot", false)) and GameState.is_special_tile_used(grid_position):
		status_label.text = "%s — déjà utilisé." % label
		return

	match str(tile.get("effect", "")):
		"heal":
			GameState.heal_player(int(tile.get("heal_amount", 0)))
			GameState.mark_special_tile_used(grid_position)
			status_label.text = "%s — repos : PV %d/%d." % [label, GameState.player_life, GameState.MAX_PLAYER_LIFE]
		"full_heal":
			GameState.heal_player(GameState.MAX_PLAYER_LIFE)
			GameState.mark_special_tile_used(grid_position)
			status_label.text = "%s — sanctuaire : PV restaurés." % label
		"reward":
			GameState.reward_pending = true
			GameState.pending_reward_pool = str(tile.get("reward_pool", "weak_reward"))
			GameState.mark_special_tile_used(grid_position)
			status_label.text = "%s — trésor trouvé." % label
			reward_requested.emit()
		_:
			status_label.text = "%s — rien à faire pour l'instant." % label

func refresh_after_battle_if_needed() -> void:
	if GameState.last_battle_won and GameState.current_enemy_id != "":
		GameState.mark_encounter_defeated(GameState.current_enemy_id)
		status_label.text = "Victoire : %s vaincu." % GameState.current_enemy_id
		GameState.last_battle_won = false
	elif GameState.run_finished and not GameState.run_won:
		status_label.text = "Défaite — run terminée."

func build_enemy_database(enemies_data: Array) -> Dictionary:
	var result := {}
	for enemy_data in enemies_data:
		result[str(enemy_data.get("id", ""))] = enemy_data
	return result

func get_enemy_data(enemy_id: String) -> Dictionary:
	return enemies_by_id.get(enemy_id, {})

func get_tile_at_position(grid_position: Vector2i) -> Dictionary:
	return get_tile_at_coordinates(current_map_data, grid_position.x, grid_position.y)

func get_tile_at_coordinates(map_data: Dictionary, x: int, y: int) -> Dictionary:
	for tile in map_data.get("tiles", []):
		if int(tile.get("x", -1)) == x and int(tile.get("y", -1)) == y:
			return tile
	return {"type": "empty", "label": "Plaine", "description": "Route libre"}

func is_inside_map(grid_position: Vector2i) -> bool:
	return grid_position.x >= 0 and grid_position.y >= 0 and grid_position.x < map_width and grid_position.y < map_height

func get_tile_type(map_data: Dictionary, x: int, y: int) -> String:
	var tile := get_tile_at_coordinates(map_data, x, y)
	if tile.get("enemy_id", "") != "" and GameState.is_encounter_defeated(str(tile.get("enemy_id", ""))):
		return "empty"
	return str(tile.get("type", "empty"))

func get_interaction_type(tile_type: String) -> String:
	match tile_type:
		"enemy_weak", "enemy_medium":
			return "enemy"
		"treasure":
			return "reward"
		_:
			return tile_type

func get_tile_color(tile_type: String) -> Color:
	return TILE_COLORS.get(tile_type, TILE_COLORS["empty"])
