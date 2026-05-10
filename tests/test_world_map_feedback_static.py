import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORLD_MAP_SCRIPT = ROOT / "scripts" / "world" / "WorldMap.gd"
WORLD_MAP_SCENE = ROOT / "scenes" / "world" / "WorldMap.tscn"
README = ROOT / "README.md"
ROADMAP = ROOT / "docs" / "roadmap.md"


class WorldMapFeedbackStaticTests(unittest.TestCase):
    def test_world_map_scene_exposes_hud_and_detail_nodes(self):
        content = WORLD_MAP_SCENE.read_text(encoding="utf-8")
        for snippet in [
            'name="HudLabel"',
            'name="TileDetailLabel"',
            'PV',
            'Or',
            'Vaincus',
            'Cartes',
        ]:
            self.assertIn(snippet, content)

    def test_world_map_script_refreshes_hud_with_run_state(self):
        content = WORLD_MAP_SCRIPT.read_text(encoding="utf-8")
        for snippet in [
            '@onready var hud_label: Label = %HudLabel',
            '@onready var tile_detail_label: Label = %TileDetailLabel',
            'func refresh_hud() -> void:',
            'GameState.player_life',
            'GameState.MAX_PLAYER_LIFE',
            'GameState.player_gold',
            'GameState.defeated_encounters.size()',
            'GameState.cards_added',
            'refresh_hud()',
        ]:
            self.assertIn(snippet, content)

    def test_world_map_marks_used_and_defeated_tiles_visually(self):
        content = WORLD_MAP_SCRIPT.read_text(encoding="utf-8")
        for snippet in [
            'const USED_TILE_COLOR :=',
            'const DEFEATED_TILE_COLOR :=',
            'func is_tile_consumed(tile: Dictionary, grid_position: Vector2i) -> bool:',
            'GameState.is_special_tile_used(grid_position)',
            'GameState.is_encounter_defeated(str(tile.get("enemy_id", "")))',
            'tile.modulate = Color(0.70, 0.70, 0.70, 1.0)',
            'symbol.text = "✓"',
        ]:
            self.assertIn(snippet, content)

    def test_world_map_updates_detail_feedback_for_tile_types(self):
        content = WORLD_MAP_SCRIPT.read_text(encoding="utf-8")
        for snippet in [
            'func describe_tile(tile: Dictionary, grid_position: Vector2i) -> String:',
            'Danger : faible',
            'Danger : moyen',
            'Boss final — très risqué',
            'Marchand : %d or',
            'Sanctuaire : soin complet',
            'Trésor : récompense de carte',
            'Déjà utilisé',
            'Déjà vaincu',
            'tile_detail_label.text = describe_tile(tile, grid_position)',
        ]:
            self.assertIn(snippet, content)

    def test_readme_and_roadmap_mark_t015_done(self):
        readme = README.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")
        self.assertIn("### T015 — Feedback UI carte aventure", readme)
        self.assertIn("HUD carte", readme)
        self.assertIn("lieux déjà utilisés", readme)
        self.assertIn("15. T015 — Feedback UI carte aventure", roadmap)


if __name__ == "__main__":
    unittest.main()
