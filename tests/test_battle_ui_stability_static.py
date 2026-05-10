import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"
SCENE = ROOT / "scenes" / "battle" / "BattleScene.tscn"


class BattleUiStabilityStaticTests(unittest.TestCase):
    def test_player_actions_append_to_log_instead_of_replacing_history(self):
        content = BATTLE.read_text(encoding="utf-8")
        self.assertIn("func append_log(message: String, replace := false) -> void:", content)
        self.assertIn("log_label.text += \"\\n\" + message", content)
        self.assertIn('append_log("Phase principale : tu joues %s."', content)
        self.assertIn('append_log("Tu termines ta phase principale.")', content)
        self.assertNotIn('log_label.text = "Phase principale : tu joues %s."', content)
        self.assertNotIn('log_label.text = "Tu termines ta phase principale."', content)

    def test_combat_zones_have_fixed_scrollable_vertical_space(self):
        scene = SCENE.read_text(encoding="utf-8")
        for snippet in [
            '[node name="EnemyBattlefieldScroll" type="ScrollContainer" parent="RootMargin/RootSplit/MainVBox"]',
            '[node name="EnemyBattlefieldContainer" type="HBoxContainer" parent="RootMargin/RootSplit/MainVBox/EnemyBattlefieldScroll"]',
            '[node name="PlayerBattlefieldScroll" type="ScrollContainer" parent="RootMargin/RootSplit/MainVBox"]',
            '[node name="PlayerBattlefieldContainer" type="HBoxContainer" parent="RootMargin/RootSplit/MainVBox/PlayerBattlefieldScroll"]',
            'custom_minimum_size = Vector2(0, 72)',
            'horizontal_scroll_mode = 1',
            'vertical_scroll_mode = 0',
            '[node name="LogPanel" type="PanelContainer" parent="RootMargin/RootSplit"]',
            'custom_minimum_size = Vector2(280, 0)',
            '[node name="HandScroll" type="ScrollContainer" parent="RootMargin/RootSplit/MainVBox"]',
            'custom_minimum_size = Vector2(0, 132)',
        ]:
            self.assertIn(snippet, scene)


if __name__ == "__main__":
    unittest.main()
