import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "data" / "map_mvp.json"
MAIN = ROOT / "scripts" / "main" / "Main.gd"
GAMESTATE = ROOT / "scripts" / "core" / "GameState.gd"
WORLD_MAP = ROOT / "scripts" / "world" / "WorldMap.gd"
README = ROOT / "README.md"


class SpecialPlacesStaticTests(unittest.TestCase):
    def setUp(self):
        self.map_data = json.loads(MAP.read_text(encoding="utf-8"))
        self.tiles = self.map_data["tiles"]

    def test_special_tiles_define_simple_interaction_effects(self):
        effects_by_type = {
            tile["type"]: tile.get("effect")
            for tile in self.tiles
            if tile["type"] in ["village", "sanctuary", "treasure"]
        }

        self.assertEqual(effects_by_type["village"], "merchant")
        self.assertEqual(effects_by_type["sanctuary"], "full_heal")
        self.assertEqual(effects_by_type["treasure"], "reward")

        for tile in self.tiles:
            if tile["type"] == "village":
                self.assertIn("shop_pool", tile)
                self.assertIn("shop_cost", tile)
            if tile["type"] in ["sanctuary", "treasure"]:
                self.assertTrue(tile.get("one_shot"))
            if tile["type"] == "treasure":
                self.assertIn("reward_pool", tile)

    def test_gamestate_tracks_used_special_places_and_healing(self):
        content = GAMESTATE.read_text(encoding="utf-8")
        for snippet in [
            "const MAX_PLAYER_LIFE := 20",
            "var used_special_tiles: Array = []",
            "func get_special_tile_key(grid_position: Vector2i) -> String:",
            "func mark_special_tile_used(grid_position: Vector2i) -> void:",
            "func is_special_tile_used(grid_position: Vector2i) -> bool:",
            "func heal_player(amount: int) -> void:",
            "player_life = min(MAX_PLAYER_LIFE, player_life + amount)",
            "used_special_tiles = []",
        ]:
            self.assertIn(snippet, content)

    def test_world_map_applies_special_place_interactions(self):
        content = WORLD_MAP.read_text(encoding="utf-8")
        for snippet in [
            "signal reward_requested",
            "func handle_special_tile(tile: Dictionary, grid_position: Vector2i) -> void:",
            '"heal":',
            "GameState.heal_player(int(tile.get(\"heal_amount\", 0)))",
            '"full_heal":',
            "GameState.heal_player(GameState.MAX_PLAYER_LIFE)",
            '"reward":',
            "GameState.pending_reward_pool = str(tile.get(\"reward_pool\", \"weak_reward\"))",
            "GameState.mark_special_tile_used(grid_position)",
            "reward_requested.emit()",
            "GameState.is_special_tile_used(grid_position)",
        ]:
            self.assertIn(snippet, content)

    def test_main_routes_map_treasure_to_reward_scene(self):
        content = MAIN.read_text(encoding="utf-8")
        for snippet in [
            'current_scene.reward_requested.connect(show_reward)',
            'if current_scene.has_signal("reward_requested"):',
        ]:
            self.assertIn(snippet, content)

    def test_readme_marks_t013_done(self):
        content = README.read_text(encoding="utf-8")
        self.assertIn("### T013 — Lieux spéciaux interactifs", content)
        self.assertIn("Village", content)
        self.assertIn("Sanctuaire", content)
        self.assertIn("Trésor", content)


if __name__ == "__main__":
    unittest.main()
