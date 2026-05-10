import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "data" / "map_mvp.json"
MAIN = ROOT / "scripts" / "main" / "Main.gd"
GAMESTATE = ROOT / "scripts" / "core" / "GameState.gd"
WORLD_MAP = ROOT / "scripts" / "world" / "WorldMap.gd"
MERCHANT_SCRIPT = ROOT / "scripts" / "merchant" / "MerchantController.gd"
MERCHANT_SCENE = ROOT / "scenes" / "merchant" / "MerchantScene.tscn"
README = ROOT / "README.md"
ROADMAP = ROOT / "docs" / "roadmap.md"


class MerchantStaticTests(unittest.TestCase):
    def test_villages_define_simple_merchant_data(self):
        data = json.loads(MAP.read_text(encoding="utf-8"))
        villages = [tile for tile in data["tiles"] if tile["type"] == "village"]
        self.assertGreaterEqual(len(villages), 2)

        for village in villages:
            self.assertEqual(village.get("effect"), "merchant")
            self.assertIn("shop_pool", village)
            self.assertIn("shop_cost", village)
            self.assertGreater(village["shop_cost"], 0)
            self.assertFalse(village.get("one_shot"), "merchant villages stay visitable until a purchase")

    def test_gamestate_tracks_gold_and_pending_shop(self):
        content = GAMESTATE.read_text(encoding="utf-8")
        for snippet in [
            "const STARTING_GOLD := 3",
            "var player_gold := STARTING_GOLD",
            "var pending_shop_pool := \"\"",
            "var pending_shop_cost := 0",
            "var pending_shop_tile_key := \"\"",
            "player_gold = STARTING_GOLD",
            "pending_shop_pool = \"\"",
            "func can_afford(cost: int) -> bool:",
            "return player_gold >= cost",
            "func spend_gold(cost: int) -> bool:",
            "player_gold -= cost",
            "func mark_special_tile_key_used(tile_key: String) -> void:",
        ]:
            self.assertIn(snippet, content)

    def test_world_map_routes_merchant_tiles_to_shop(self):
        content = WORLD_MAP.read_text(encoding="utf-8")
        for snippet in [
            "signal shop_requested",
            '"merchant":',
            "GameState.pending_shop_pool = str(tile.get(\"shop_pool\", \"weak_reward\"))",
            "GameState.pending_shop_cost = int(tile.get(\"shop_cost\", 1))",
            "GameState.pending_shop_tile_key = GameState.get_special_tile_key(grid_position)",
            "shop_requested.emit()",
        ]:
            self.assertIn(snippet, content)

    def test_main_routes_world_map_shop_to_merchant_scene(self):
        content = MAIN.read_text(encoding="utf-8")
        for snippet in [
            'const MERCHANT_SCENE := preload("res://scenes/merchant/MerchantScene.tscn")',
            'if current_scene.has_signal("shop_requested"):',
            'current_scene.shop_requested.connect(show_merchant)',
            'func show_merchant() -> void:',
            '_replace_scene(MERCHANT_SCENE)',
            'current_scene.merchant_finished.connect(show_world_map)',
        ]:
            self.assertIn(snippet, content)

    def test_merchant_scene_and_controller_support_one_simple_purchase(self):
        scene = MERCHANT_SCENE.read_text(encoding="utf-8")
        script = MERCHANT_SCRIPT.read_text(encoding="utf-8")

        for snippet in ["MerchantScene", "MerchantController.gd", "MerchantChoices", "StatusLabel", "Marchand"]:
            self.assertIn(snippet, scene)

        for snippet in [
            "signal merchant_finished",
            "const DataLoaderScript = preload(\"res://scripts/core/DataLoader.gd\")",
            "func show_shop() -> void:",
            "func buy_card(card_id: String) -> void:",
            "GameState.can_afford(GameState.pending_shop_cost)",
            "GameState.spend_gold(GameState.pending_shop_cost)",
            "GameState.add_card_to_deck(card_id)",
            "GameState.mark_special_tile_key_used(GameState.pending_shop_tile_key)",
            "merchant_finished.emit()",
            "Retour carte",
        ]:
            self.assertIn(snippet, script)

    def test_readme_and_roadmap_mark_t014_done(self):
        readme = README.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")
        self.assertIn("### T014 — Marchand simple", readme)
        self.assertIn("or de départ", readme)
        self.assertIn("achat simple", readme)
        self.assertIn("14. T014 — Marchand simple", roadmap)


if __name__ == "__main__":
    unittest.main()
