import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / "scenes" / "battle" / "BattleScene.tscn"
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"


class BattleLogScrollStaticTests(unittest.TestCase):
    def test_battle_log_is_in_dedicated_scrollable_panel(self):
        scene = SCENE.read_text(encoding="utf-8")
        for snippet in [
            '[node name="LogPanel" type="PanelContainer" parent="RootMargin/VBox"]',
            '[node name="LogVBox" type="VBoxContainer" parent="RootMargin/VBox/LogPanel"]',
            '[node name="LogTitle" type="Label" parent="RootMargin/VBox/LogPanel/LogVBox"]',
            'text = "Journal du combat"',
            '[node name="LogScroll" type="ScrollContainer" parent="RootMargin/VBox/LogPanel/LogVBox"]',
            'vertical_scroll_mode = 1',
            'custom_minimum_size = Vector2(0, 120)',
            '[node name="LogLabel" type="Label" parent="RootMargin/VBox/LogPanel/LogVBox/LogScroll"]',
            'size_flags_vertical = 3',
            'autowrap_mode = 3',
        ]:
            self.assertIn(snippet, scene)

    def test_battle_controller_keeps_log_scroll_at_bottom(self):
        content = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            '@onready var log_scroll: ScrollContainer = %LogScroll',
            'func scroll_log_to_bottom() -> void:',
            'var scrollbar := log_scroll.get_v_scroll_bar()',
            'scrollbar.value = scrollbar.max_value',
            'log_scroll.call_deferred("ensure_control_visible", log_label)',
            'scroll_log_to_bottom.call_deferred()',
        ]:
            self.assertIn(snippet, content)


if __name__ == "__main__":
    unittest.main()
