import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"
SCENE = ROOT / "scenes" / "battle" / "BattleScene.tscn"


class PassTurnStaticTests(unittest.TestCase):
    def test_battle_scene_exposes_pass_turn_button(self):
        scene = SCENE.read_text(encoding="utf-8")
        self.assertIn('[node name="PassTurnButton" type="Button" parent="RootMargin/VBox/ActionRow"]', scene)
        self.assertIn("unique_name_in_owner = true", scene)
        self.assertIn('text = "Terminer le tour"', scene)

    def test_battle_controller_can_end_player_turn_without_playing_card(self):
        content = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            "@onready var pass_turn_button: Button = %PassTurnButton",
            "pass_turn_button.pressed.connect(end_player_turn)",
            "func end_player_turn() -> void:",
            'append_log("Tu termines ta phase principale.")',
            "resolve_player_combat_step()",
            "resolve_creature_attack(player, enemy, \"Tes\")",
            "player.ready_creatures_for_next_turn()",
            "enemy_turn()",
            "refresh_ui()",
            "pass_turn_button.disabled = battle_finished_state",
        ]:
            self.assertIn(snippet, content)


if __name__ == "__main__":
    unittest.main()
