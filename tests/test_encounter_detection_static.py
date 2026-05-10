import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORLD_MAP_SCRIPT = ROOT / "scripts" / "world" / "WorldMap.gd"
GAMESTATE_SCRIPT = ROOT / "scripts" / "core" / "GameState.gd"


class EncounterDetectionStaticTests(unittest.TestCase):
    def test_gamestate_tracks_current_tile_and_reward_pending(self):
        content = GAMESTATE_SCRIPT.read_text(encoding="utf-8")

        expected_snippets = [
            'var current_tile_type := ""',
            "var reward_pending := false",
            'current_tile_type = ""',
            "reward_pending = false",
        ]

        for snippet in expected_snippets:
            self.assertIn(snippet, content)

    def test_world_map_keeps_map_data_for_encounter_lookup(self):
        content = WORLD_MAP_SCRIPT.read_text(encoding="utf-8")

        expected_snippets = [
            "var current_map_data: Dictionary = {}",
            "current_map_data = map_data",
            "func get_tile_at_position(grid_position: Vector2i) -> Dictionary:",
            "func handle_tile_entered(grid_position: Vector2i) -> void:",
            "handle_tile_entered(next_position)",
        ]

        for snippet in expected_snippets:
            self.assertIn(snippet, content)

    def test_world_map_detects_enemy_boss_reward_and_empty_tiles(self):
        content = WORLD_MAP_SCRIPT.read_text(encoding="utf-8")

        expected_snippets = [
            '"enemy":',
            '"boss":',
            '"reward":',
            "GameState.current_enemy_id = str(tile.get(\"enemy_id\", \"\"))",
            "GameState.current_tile_type = interaction_type",
            "GameState.reward_pending = true",
            "GameState.is_encounter_defeated(GameState.current_enemy_id)",
            'status_label.text = "%s : %s"',
            'status_label.text = "Boss final : %s"',
            'status_label.text = "%s — trésor trouvé."',
        ]

        for snippet in expected_snippets:
            self.assertIn(snippet, content)


if __name__ == "__main__":
    unittest.main()
