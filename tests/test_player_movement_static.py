import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYER_SCRIPT = ROOT / "scripts" / "world" / "PlayerToken.gd"
WORLD_MAP_SCRIPT = ROOT / "scripts" / "world" / "WorldMap.gd"
PROJECT = ROOT / "project.godot"


class PlayerMovementStaticTests(unittest.TestCase):
    def test_project_defines_movement_input_actions(self):
        content = PROJECT.read_text(encoding="utf-8")

        for action in [
            "move_up",
            "move_down",
            "move_left",
            "move_right",
        ]:
            self.assertIn(action, content)

    def test_player_token_script_exposes_grid_position_api(self):
        content = PLAYER_SCRIPT.read_text(encoding="utf-8")

        expected_snippets = [
            "extends ColorRect",
            "const TILE_SIZE := 44",
            "const TILE_GAP := 4",
            "func set_grid_position(grid_position: Vector2i) -> void:",
            "GameState.player_position = grid_position",
            "position = grid_to_screen(grid_position)",
            "func grid_to_screen(grid_position: Vector2i) -> Vector2:",
        ]

        for snippet in expected_snippets:
            self.assertIn(snippet, content)

    def test_world_map_handles_keyboard_movement_and_bounds(self):
        content = WORLD_MAP_SCRIPT.read_text(encoding="utf-8")

        expected_snippets = [
            "@onready var player_token: ColorRect = %PlayerToken",
            "func _unhandled_input(event: InputEvent) -> void:",
            "Input.is_action_just_pressed(\"move_up\")",
            "Input.is_action_just_pressed(\"move_down\")",
            "Input.is_action_just_pressed(\"move_left\")",
            "Input.is_action_just_pressed(\"move_right\")",
            "func try_move_player(delta: Vector2i) -> void:",
            "func is_inside_map(grid_position: Vector2i) -> bool:",
            "player_token.set_grid_position(next_position)",
        ]

        for snippet in expected_snippets:
            self.assertIn(snippet, content)


if __name__ == "__main__":
    unittest.main()
