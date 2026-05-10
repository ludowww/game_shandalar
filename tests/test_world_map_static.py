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
    def test_map_json_defines_readable_adventure_layout(self):
        data = json.loads(MAP_JSON.read_text(encoding="utf-8"))

        self.assertGreaterEqual(data["width"], 12)
        self.assertGreaterEqual(data["height"], 9)
        self.assertEqual(data["start_position"], [1, 4])
        self.assertEqual(data["theme"], "shandalar_adventure_v1")

        tiles = data["tiles"]
        tile_types = [tile["type"] for tile in tiles]
        for required_type in ["start", "enemy_weak", "enemy_medium", "boss", "village", "sanctuary", "treasure"]:
            self.assertIn(required_type, tile_types)

        self.assertGreaterEqual(tile_types.count("enemy_weak"), 4)
        self.assertGreaterEqual(tile_types.count("enemy_medium"), 3)
        self.assertEqual(tile_types.count("boss"), 1)

        for tile in tiles:
            self.assertIn("label", tile)
            self.assertIn("description", tile)
            self.assertGreaterEqual(tile["x"], 0)
            self.assertGreaterEqual(tile["y"], 0)
            self.assertLess(tile["x"], data["width"])
            self.assertLess(tile["y"], data["height"])

        boss_tiles = [tile for tile in tiles if tile["type"] == "boss"]
        self.assertEqual(boss_tiles[0]["enemy_id"], "boss_seal_guardian")
        self.assertEqual(boss_tiles[0]["danger"], "boss")

    def test_adventure_map_has_legend_and_route_choices(self):
        data = json.loads(MAP_JSON.read_text(encoding="utf-8"))

        legend_types = {entry["type"] for entry in data["legend"]}
        for required_type in ["start", "enemy_weak", "enemy_medium", "boss", "village", "sanctuary", "treasure"]:
            self.assertIn(required_type, legend_types)

        walkable_tiles = {(tile["x"], tile["y"]) for tile in data["tiles"]}
        start = tuple(data["start_position"])
        self.assertIn((start[0] + 1, start[1] - 1), walkable_tiles)
        self.assertIn((start[0] + 1, start[1] + 1), walkable_tiles)
        self.assertIn((data["width"] - 2, data["height"] // 2), walkable_tiles)

    def test_world_map_script_loads_map_and_builds_grid(self):
        content = WORLD_MAP_SCRIPT.read_text(encoding="utf-8")

        expected_snippets = [
            "extends Control",
            "const TILE_SIZE := 44",
            "const TILE_COLORS :=",
            "const TILE_SYMBOLS :=",
            "@onready var legend_box",
            "func _ready() -> void:",
            "data_loader.load_map()",
            "func build_grid(map_data: Dictionary) -> void:",
            "func build_legend(map_data: Dictionary) -> void:",
            "func get_tile_type",
            "func get_interaction_type",
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
        self.assertIn('name="LegendBox"', world_scene)
        self.assertIn('custom_minimum_size = Vector2(712, 444)', world_scene)
        self.assertIn('path="res://scripts/main/Main.gd"', main_scene)
        self.assertIn('preload("res://scenes/world/WorldMap.tscn")', main_script)
        self.assertIn('show_world_map', main_script)


if __name__ == "__main__":
    unittest.main()
