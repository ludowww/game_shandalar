import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAMESTATE = ROOT / "scripts" / "core" / "GameState.gd"
PROJECT = ROOT / "project.godot"


class GameStateStaticTests(unittest.TestCase):
    def test_gamestate_script_defines_run_state_and_reset(self):
        content = GAMESTATE.read_text(encoding="utf-8")

        expected_snippets = [
            "extends Node",
            "var player_position := Vector2i(1, 1)",
            "var player_life := 20",
            "var player_deck: Array = []",
            "var defeated_encounters: Array = []",
            "var current_enemy_id := \"\"",
            "var run_finished := false",
            "var run_won := false",
            "func reset_run() -> void:",
        ]

        for snippet in expected_snippets:
            self.assertIn(snippet, content)

    def test_gamestate_is_registered_as_autoload(self):
        content = PROJECT.read_text(encoding="utf-8")

        self.assertIn("[autoload]", content)
        self.assertIn('GameState="*res://scripts/core/GameState.gd"', content)


if __name__ == "__main__":
    unittest.main()
