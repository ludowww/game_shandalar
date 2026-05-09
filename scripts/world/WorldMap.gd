extends Control

const TILE_SIZE := 64
const TILE_GAP := 4
const TILE_COLORS := {
	"empty": Color(0.12, 0.15, 0.18, 1.0),
	"start": Color(0.20, 0.50, 0.90, 1.0),
	"enemy": Color(0.75, 0.22, 0.18, 1.0),
	"reward": Color(0.95, 0.72, 0.20, 1.0),
	"boss": Color(0.55, 0.18, 0.75, 1.0)
}

var map_width := 0
var map_height := 0
var current_map_data: Dictionary = {}

@onready var grid: GridContainer = %MapGrid
@onready var status_label: Label = %StatusLabel
@onready var player_token: ColorRect = %PlayerToken

func _ready() -> void:
	var map_data = DataLoader.load_map()
	if map_data == null:
		status_label.text = "Erreur : impossible de charger data/map_mvp.json"
		return

	current_map_data = map_data
	build_grid(map_data)
	var start_position: Array = map_data.get("start_position", [1, 1])
	player_token.set_grid_position(Vector2i(int(start_position[0]), int(start_position[1])))
	handle_tile_entered(GameState.player_position)
	status_label.text = "Carte MVP 8x8 chargée — déplace-toi avec les flèches ou ZQSD."

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
			var tile := ColorRect.new()
			tile.custom_minimum_size = Vector2(TILE_SIZE, TILE_SIZE)
			tile.color = get_tile_color(tile_type)
			tile.tooltip_text = "%s (%d, %d)" % [tile_type, x, y]
			grid.add_child(tile)

func try_move_player(delta: Vector2i) -> void:
	var next_position := GameState.player_position + delta
	if not is_inside_map(next_position):
		return

	player_token.set_grid_position(next_position)
	handle_tile_entered(next_position)

func handle_tile_entered(grid_position: Vector2i) -> void:
	var tile := get_tile_at_position(grid_position)
	var tile_type := str(tile.get("type", "empty"))
	GameState.current_tile_type = tile_type
	GameState.reward_pending = false

	match tile_type:
		"enemy":
			GameState.current_enemy_id = str(tile.get("enemy_id", ""))
			if GameState.is_encounter_defeated(GameState.current_enemy_id):
				status_label.text = "Rencontre déjà vaincue : %s" % GameState.current_enemy_id
			else:
				status_label.text = "Rencontre : %s" % GameState.current_enemy_id
		"boss":
			GameState.current_enemy_id = str(tile.get("enemy_id", ""))
			status_label.text = "Boss : %s" % GameState.current_enemy_id
		"reward":
			GameState.current_enemy_id = ""
			GameState.reward_pending = true
			status_label.text = "Récompense trouvée."
		_:
			GameState.current_enemy_id = ""
			status_label.text = "Position joueur : (%d, %d)" % [grid_position.x, grid_position.y]

func get_tile_at_position(grid_position: Vector2i) -> Dictionary:
	for tile in current_map_data.get("tiles", []):
		if int(tile.get("x", -1)) == grid_position.x and int(tile.get("y", -1)) == grid_position.y:
			return tile
	return {"type": "empty"}

func is_inside_map(grid_position: Vector2i) -> bool:
	return grid_position.x >= 0 and grid_position.y >= 0 and grid_position.x < map_width and grid_position.y < map_height

func get_tile_type(map_data: Dictionary, x: int, y: int) -> String:
	for tile in map_data.get("tiles", []):
		if int(tile.get("x", -1)) == x and int(tile.get("y", -1)) == y:
			return str(tile.get("type", "empty"))
	return "empty"

func get_tile_color(tile_type: String) -> Color:
	return TILE_COLORS.get(tile_type, TILE_COLORS["empty"])
