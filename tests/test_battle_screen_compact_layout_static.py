import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / "scenes" / "battle" / "BattleScene.tscn"


class BattleScreenCompactLayoutStaticTests(unittest.TestCase):
    def test_battle_screen_uses_main_area_plus_side_log_panel(self):
        scene = SCENE.read_text(encoding="utf-8")
        for snippet in [
            '[node name="RootSplit" type="HBoxContainer" parent="RootMargin"]',
            '[node name="MainVBox" type="VBoxContainer" parent="RootMargin/RootSplit"]',
            '[node name="LogPanel" type="PanelContainer" parent="RootMargin/RootSplit"]',
            'custom_minimum_size = Vector2(280, 0)',
            '[node name="LogScroll" type="ScrollContainer" parent="RootMargin/RootSplit/LogPanel/LogVBox"]',
            '[node name="LogLabel" type="Label" parent="RootMargin/RootSplit/LogPanel/LogVBox/LogScroll"]',
        ]:
            self.assertIn(snippet, scene)
        self.assertLess(scene.index('name="MainVBox"'), scene.index('name="LogPanel"'))

    def test_critical_combat_info_stays_in_main_column_outside_log(self):
        scene = SCENE.read_text(encoding="utf-8")
        for snippet in [
            '[node name="LifeRow" type="HBoxContainer" parent="RootMargin/RootSplit/MainVBox"]',
            '[node name="MagicZonesLabel" type="Label" parent="RootMargin/RootSplit/MainVBox"]',
            '[node name="ManaLabel" type="Label" parent="RootMargin/RootSplit/MainVBox"]',
            '[node name="PhaseLabel" type="Label" parent="RootMargin/RootSplit/MainVBox"]',
            '[node name="ActionRow" type="HBoxContainer" parent="RootMargin/RootSplit/MainVBox"]',
            '[node name="HandScroll" type="ScrollContainer" parent="RootMargin/RootSplit/MainVBox"]',
        ]:
            self.assertIn(snippet, scene)
        self.assertLess(scene.index('name="LifeRow"'), scene.index('name="HandScroll"'))


if __name__ == "__main__":
    unittest.main()
