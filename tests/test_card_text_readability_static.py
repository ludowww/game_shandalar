import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"
REWARD = ROOT / "scripts" / "reward" / "RewardController.gd"
MERCHANT = ROOT / "scripts" / "merchant" / "MerchantController.gd"
BATTLE_SCENE = ROOT / "scenes" / "battle" / "BattleScene.tscn"
REWARD_SCENE = ROOT / "scenes" / "reward" / "RewardScene.tscn"
MERCHANT_SCENE = ROOT / "scenes" / "merchant" / "MerchantScene.tscn"


class CardTextReadabilityStaticTests(unittest.TestCase):
    def test_card_buttons_wrap_text_and_keep_full_tooltips(self):
        for path in [BATTLE, REWARD, MERCHANT]:
            content = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn("func configure_card_button", content)
                self.assertIn("button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART", content)
                self.assertIn("button.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS", content)
                self.assertIn("button.tooltip_text =", content)
                self.assertIn("button.custom_minimum_size", content)

    def test_card_rows_are_scrollable_to_preserve_screen_space(self):
        scene_expectations = [
            (BATTLE_SCENE, "HandScroll", "HandContainer"),
            (REWARD_SCENE, "RewardChoicesScroll", "RewardChoices"),
            (MERCHANT_SCENE, "MerchantChoicesScroll", "MerchantChoices"),
        ]
        for scene_path, scroll_name, container_name in scene_expectations:
            scene = scene_path.read_text(encoding="utf-8")
            with self.subTest(scene=scene_path.name):
                self.assertIn(f'[node name="{scroll_name}" type="ScrollContainer"', scene)
                self.assertIn("horizontal_scroll_mode = 1", scene)
                self.assertIn("vertical_scroll_mode = 0", scene)
                self.assertIn(f'[node name="{container_name}" type="HBoxContainer" parent=', scene)
                self.assertIn("size_flags_horizontal = 3", scene)


if __name__ == "__main__":
    unittest.main()
