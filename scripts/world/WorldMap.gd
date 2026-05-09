extends Control

const TILE_SIZE := 64
const TILE_COLORS := {
	"empty": Color(0.12, 0.15, 0.18, 1.0),
	"start": Color(0.20, 0.50, 0.90, 1.0),
	"enemy": Color(0.75, 0.22, 0.18, 1.0),
	"reward": Color(0.95, 0.72, 0.20, 1.0),
	"boss": Color(0.55, 0.18, 0.75, 1.0)
}

@onready var grid: GridContainer = %MapGrid
@onready var status_label: Label = %StatusLabel

func _ready() -> void:
	var map_data = DataLoader.load_map()
	if map_data == null:
		status_label.text = "Erreur : impossible de charger data/map_mvp.json"
		return

	build_grid(map_data)
	status_label.text = "Carte MVP 8x8 chargée — boss visible dès le départ."

func build_grid(map_data: Dictionary) -> void:
	var width := int(map_data.get("width", 0))
	var height := int(map_data.get("height", 0))
	grid.columns = width

	for child in grid.get_children():
		child.queue_free()

	for y in range(height):
		for x in range(width):
			var tile_type := get_tile_type(map_data, x, y)
			var tile := ColorRect.new()
			tile.custom_minimum_size = Vector2(TILE_SIZE, TILE_SIZE)
			tile.color = get_tile_color(tile_type)
			tile.tooltip_text = "%s (%d, %d)" % [tile_type, x, y]
			grid.add_child(tile)

func get_tile_type(map_data: Dictionary, x: int, y: int) -> String:
	for tile in map_data.get("tiles", []):
		if int(tile.get("x", -1)) == x and int(tile.get("y", -1)) == y:
			return str(tile.get("type", "empty"))
	return "empty"

func get_tile_color(tile_type: String) -> Color:
	return TILE_COLORS.get(tile_type, TILE_COLORS["empty"])
