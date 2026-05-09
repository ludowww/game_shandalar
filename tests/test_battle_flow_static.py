import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "scripts" / "main" / "Main.gd"
WORLD_MAP = ROOT / "scripts" / "world" / "WorldMap.gd"
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"
GAMESTATE = ROOT / "scripts" / "core" / "GameState.gd"
BATTLE_SCENE = ROOT / "scenes" / "battle" / "BattleScene.tscn"


class BattleFlowStaticTests(unittest.TestCase):
    def test_gamestate_tracks_last_battle_result(self):
        content = GAMESTATE.read_text(encoding="utf-8")
        for snippet in [
            'var last_battle_won := false',
            'var pending_reward_pool := ""',
            'last_battle_won = false',
            'pending_reward_pool = ""',
        ]:
            self.assertIn(snippet, content)

    def test_main_can_route_between_world_and_battle(self):
        content = MAIN.read_text(encoding="utf-8")
        for snippet in [
            'const WORLD_MAP_SCENE := preload("res://scenes/world/WorldMap.tscn")',
            'const BATTLE_SCENE := preload("res://scenes/battle/BattleScene.tscn")',
            'func show_world_map() -> void:',
            'func show_battle() -> void:',
            'func _replace_scene(scene: PackedScene) -> void:',
            'add_child(current_scene)',
        ]:
            self.assertIn(snippet, content)

    def test_world_map_launches_battle_for_enemy_and_boss(self):
        content = WORLD_MAP.read_text(encoding="utf-8")
        for snippet in [
            'signal battle_requested',
            'battle_requested.emit()',
            'GameState.pending_reward_pool = str(tile.get("reward_pool", ""))',
            'var enemy_data := get_enemy_data(GameState.current_enemy_id)',
            'func get_enemy_data(enemy_id: String) -> Dictionary:',
            'GameState.last_battle_won',
            'GameState.mark_encounter_defeated(GameState.current_enemy_id)',
        ]:
            self.assertIn(snippet, content)

    def test_battle_controller_returns_to_world_after_end(self):
        content = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            'signal battle_finished',
            'battle_finished.emit()',
            'GameState.last_battle_won = true',
            'GameState.mark_encounter_defeated(GameState.current_enemy_id)',
            'GameState.finish_run(false)',
            'ReturnButton',
            'func _on_return_button_pressed() -> void:',
        ]:
            self.assertIn(snippet, content)

    def test_battle_scene_has_return_button(self):
        content = BATTLE_SCENE.read_text(encoding="utf-8")
        self.assertIn('ReturnButton', content)
        self.assertIn('text = "Retour carte"', content)


if __name__ == "__main__":
    unittest.main()
