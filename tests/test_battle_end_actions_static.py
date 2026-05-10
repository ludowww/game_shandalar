import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"
SCENE = ROOT / "scenes" / "battle" / "BattleScene.tscn"


class BattleEndActionsStaticTests(unittest.TestCase):
    def test_return_and_pass_buttons_are_grouped_above_hand_for_visibility(self):
        scene = SCENE.read_text(encoding="utf-8")
        self.assertIn('[node name="ActionRow" type="HBoxContainer" parent="RootMargin/RootSplit/MainVBox"]', scene)
        self.assertIn('[node name="PassTurnButton" type="Button" parent="RootMargin/RootSplit/MainVBox/ActionRow"]', scene)
        self.assertIn('[node name="ReturnButton" type="Button" parent="RootMargin/RootSplit/MainVBox/ActionRow"]', scene)
        self.assertLess(scene.index('name="ActionRow"'), scene.index('name="HandTitle"'))

    def test_battle_end_switches_from_pass_to_visible_return_button(self):
        content = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            "func show_battle_end_actions() -> void:",
            "pass_turn_button.visible = false",
            "return_button.visible = true",
            "return_button.disabled = false",
            "show_battle_end_actions()",
            "pass_turn_button.visible = not battle_finished_state",
        ]:
            self.assertIn(snippet, content)


if __name__ == "__main__":
    unittest.main()
