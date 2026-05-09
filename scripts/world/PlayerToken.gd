extends ColorRect

const TILE_SIZE := 64
const TILE_GAP := 4

func _ready() -> void:
	custom_minimum_size = Vector2(TILE_SIZE, TILE_SIZE)
	color = Color(0.15, 0.85, 0.35, 1.0)
	mouse_filter = Control.MOUSE_FILTER_IGNORE

func set_grid_position(grid_position: Vector2i) -> void:
	GameState.player_position = grid_position
	position = grid_to_screen(grid_position)

func grid_to_screen(grid_position: Vector2i) -> Vector2:
	var step := TILE_SIZE + TILE_GAP
	return Vector2(grid_position.x * step, grid_position.y * step)
