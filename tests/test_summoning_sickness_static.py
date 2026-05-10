import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMBATANT = ROOT / "scripts" / "battle" / "Combatant.gd"
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"
README = ROOT / "README.md"
ROADMAP = ROOT / "docs" / "roadmap.md"


class SummoningSicknessStaticTests(unittest.TestCase):
    def test_summoned_creatures_enter_summoning_sick_and_do_not_attack_immediately(self):
        content = COMBATANT.read_text(encoding="utf-8")
        for snippet in [
            '"summoning_sick": true',
            "func ready_creatures_for_next_turn() -> void:",
            'if bool(creature.get("summoning_sick", false)):',
            'creature["summoning_sick"] = false',
            "func attack_with_creatures(target) -> int:",
            'if bool(creature.get("summoning_sick", false)):',
            "continue",
        ]:
            self.assertIn(snippet, content)

    def test_battle_controller_lifts_summoning_sickness_after_controller_turn(self):
        content = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            "resolve_creature_attack(player, enemy, \"Tes\")",
            "player.ready_creatures_for_next_turn()",
            "resolve_creature_attack(enemy, player, enemy.name)",
            "enemy.ready_creatures_for_next_turn()",
        ]:
            self.assertIn(snippet, content)

    def test_battlefield_ui_marks_summoning_sick_creatures(self):
        content = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            "Mal d'invocation",
            'bool(creature.get("summoning_sick", false))',
        ]:
            self.assertIn(snippet, content)

    def test_readme_and_roadmap_mark_t016b_done(self):
        readme = README.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")
        self.assertIn("### T016b — Mal d’invocation", readme)
        self.assertIn("mal d’invocation", readme.lower())
        self.assertIn("T016b — Mal d’invocation", roadmap)


if __name__ == "__main__":
    unittest.main()
