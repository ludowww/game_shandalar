import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_JSON = ROOT / "data" / "map_mvp.json"
WORLD_MAP_SCRIPT = ROOT / "scripts" / "world" / "WorldMap.gd"
WORLD_MAP_SCENE = ROOT / "scenes" / "world" / "WorldMap.tscn"
MAIN_SCENE = ROOT / "scenes" / "main" / "Main.tscn"
MAIN_SCRIPT = ROOT / "scripts" / "main" / "Main.gd"


class WorldMapStaticTests(unittest.TestCase):
    def test_map_json_defines_8_by_8_mvp_layout(self):
        data = json.loads(MAP_JSON.read_text(encoding="utf-8"))

        self.assertEqual(data["width"], 8)
        self.assertEqual(data["height"], 8)
        self.assertEqual(data["start_position"], [1, 1])

        tiles = data["tiles"]
        tile_types = [tile["type"] for tile in tiles]
        self.assertIn("start", tile_types)
        self.assertGreaterEqual(tile_types.count("enemy"), 3)
        self.assertIn("reward", tile_types)
        self.assertIn("boss", tile_types)

        boss_tiles = [tile for tile in tiles if tile["type"] == "boss"]
        self.assertEqual(boss_tiles[0]["enemy_id"], "boss_seal_guardian")

    def test_world_map_script_loads_map_and_builds_grid(self):
        content = WORLD_MAP_SCRIPT.read_text(encoding="utf-8")

        expected_snippets = [
            "extends Control",
            "const TILE_SIZE := 64",
            "const TILE_COLORS :=",
            "func _ready() -> void:",
            "data_loader.load_map()",
            "func build_grid(map_data: Dictionary) -> void:",
            "func get_tile_type",
            "func get_tile_color",
            "GridContainer",
        ]

        for snippet in expected_snippets:
            self.assertIn(snippet, content)

    def test_world_map_scene_exists_and_main_instantiates_it(self):
        world_scene = WORLD_MAP_SCENE.read_text(encoding="utf-8")
        main_scene = MAIN_SCENE.read_text(encoding="utf-8")
        main_script = MAIN_SCRIPT.read_text(encoding="utf-8")

        self.assertIn('path="res://scripts/world/WorldMap.gd"', world_scene)
        self.assertIn('path="res://scripts/main/Main.gd"', main_scene)
        self.assertIn('preload("res://scenes/world/WorldMap.tscn")', main_script)
        self.assertIn('show_world_map', main_script)


if __name__ == "__main__":
    unittest.main()
