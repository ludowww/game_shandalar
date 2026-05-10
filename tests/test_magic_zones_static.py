import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMBATANT = ROOT / "scripts" / "battle" / "Combatant.gd"
DECK = ROOT / "scripts" / "battle" / "Deck.gd"
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"
SCENE = ROOT / "scenes" / "battle" / "BattleScene.tscn"
README = ROOT / "README.md"
ROADMAP = ROOT / "docs" / "roadmap.md"


class MagicZonesStaticTests(unittest.TestCase):
    def test_combatant_declares_explicit_magic_zones_and_future_hooks(self):
        content = COMBATANT.read_text(encoding="utf-8")
        for snippet in [
            'const ZONE_LIBRARY := "Bibliothèque"',
            'const ZONE_HAND := "Main"',
            'const ZONE_BATTLEFIELD := "Champ de bataille"',
            'const ZONE_GRAVEYARD := "Cimetière"',
            'const FUTURE_ZONE_LANDS := "Terrains (futur)"',
            'const FUTURE_RESOURCE_MANA := "Mana (futur)"',
            'var library = deck',
            'var hand: Array = []',
            'var battlefield: Array = []',
            'var graveyard: Array = []',
        ]:
            self.assertIn(snippet, content)

    def test_zone_transitions_are_documented_for_creatures_and_spells(self):
        content = COMBATANT.read_text(encoding="utf-8")
        for snippet in [
            'func get_zone_summary() -> Dictionary:',
            '"library": library_size()',
            '"hand": hand.size()',
            '"battlefield": battlefield.size()',
            '"graveyard": graveyard.size()',
            'func library_size() -> int:',
            'summon_creature(card)',
            'battlefield.append(creature)',
            'apply_card_effect(card, target)',
            'move_to_graveyard(card_id)',
            'graveyard.append(card_id)',
        ]:
            self.assertIn(snippet, content)

    def test_deck_script_clarifies_library_and_cemetery_terms(self):
        content = DECK.read_text(encoding="utf-8")
        for snippet in [
            'const ZONE_LIBRARY := "Bibliothèque"',
            'const ZONE_GRAVEYARD := "Cimetière"',
            'func library_size() -> int:',
            'return cards.size()',
            'func graveyard_buffer_size() -> int:',
            'return discard_pile.size()',
        ]:
            self.assertIn(snippet, content)

    def test_battle_ui_displays_zone_summary(self):
        scene = SCENE.read_text(encoding="utf-8")
        controller = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            'MagicZonesLabel',
            'Zones Magic',
            'Bibliothèque',
            'Main',
            'Champ de bataille',
            'Cimetière',
        ]:
            self.assertIn(snippet, scene)
        for snippet in [
            '@onready var magic_zones_label: Label = %MagicZonesLabel',
            'func refresh_zone_summary_ui() -> void:',
            'player.get_zone_summary()',
            'enemy.get_zone_summary()',
            'Bibliothèque',
            'Cimetière',
            'refresh_zone_summary_ui()',
        ]:
            self.assertIn(snippet, controller)

    def test_readme_and_roadmap_mark_t017_done(self):
        readme = README.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")
        self.assertIn("### T017 — Zones Magic explicites", readme)
        self.assertIn("Bibliothèque", readme)
        self.assertIn("Main", readme)
        self.assertIn("Champ de bataille", readme)
        self.assertIn("Cimetière", readme)
        self.assertIn("T017 — Zones Magic explicites", roadmap)


if __name__ == "__main__":
    unittest.main()
