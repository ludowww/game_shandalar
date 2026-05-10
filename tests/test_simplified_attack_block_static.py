import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMBATANT = ROOT / "scripts" / "battle" / "Combatant.gd"
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"
SCENE = ROOT / "scenes" / "battle" / "BattleScene.tscn"
README = ROOT / "README.md"
ROADMAP = ROOT / "docs" / "roadmap.md"


class SimplifiedAttackBlockStaticTests(unittest.TestCase):
    def test_combatant_declares_attackers_blockers_and_combat_resolution(self):
        content = COMBATANT.read_text(encoding="utf-8")
        for snippet in [
            "func get_ready_attackers() -> Array:",
            'if bool(creature.get("summoning_sick", false)):',
            "func assign_simple_blockers(attackers: Array) -> Dictionary:",
            "var blockers_by_attacker := {}",
            "blockers_by_attacker[attacker] = blocker",
            "func resolve_simplified_combat_against(defender) -> Dictionary:",
            "get_ready_attackers()",
            "defender.assign_simple_blockers(attackers)",
            "unblocked_damage",
            "blocked_count",
            "dead_attackers",
            "dead_blockers",
            "remove_dead_creatures()",
        ]:
            self.assertIn(snippet, content)

    def test_blocked_creatures_exchange_damage_and_unblocked_hit_player(self):
        content = COMBATANT.read_text(encoding="utf-8")
        for snippet in [
            'attacker["health"] = int(attacker.get("health", 0)) - int(blocker.get("attack", 0))',
            'blocker["health"] = int(blocker.get("health", 0)) - int(attacker.get("attack", 0))',
            'unblocked_damage += int(attacker.get("attack", 0))',
            'defender.life = max(0, defender.life - unblocked_damage)',
            'if int(creature.get("health", 0)) <= 0:',
            'graveyard.append(str(creature.get("id", "")))',
        ]:
            self.assertIn(snippet, content)

    def test_battle_controller_uses_simplified_combat_in_combat_phase(self):
        content = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            "func resolve_creature_attack(attacker, defender, attacker_label: String) -> void:",
            "var result: Dictionary = attacker.resolve_simplified_combat_against(defender)",
            'int(result.get("attackers", 0))',
            'int(result.get("blocked_count", 0))',
            'int(result.get("unblocked_damage", 0))',
            'int(result.get("dead_attackers", 0))',
            'int(result.get("dead_blockers", 0))',
            "bloquées",
            "non bloqués infligent",
            "meurent au combat",
        ]:
            self.assertIn(snippet, content)

    def test_battle_scene_mentions_simplified_blocking(self):
        scene = SCENE.read_text(encoding="utf-8")
        for snippet in [
            "Blocage automatique simple",
            "Combat automatique",
        ]:
            self.assertIn(snippet, scene)

    def test_readme_and_roadmap_mark_t020_done(self):
        readme = README.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")
        self.assertIn("### T020 — Attaque et blocage simplifiés", readme)
        self.assertIn("blocage automatique", readme.lower())
        self.assertIn("créatures non bloquées", readme.lower())
        self.assertIn("T020 — Attaque et blocage simplifiés", roadmap)


if __name__ == "__main__":
    unittest.main()
