import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "data" / "cards.json"
COMBATANT = ROOT / "scripts" / "battle" / "Combatant.gd"
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"
SCENE = ROOT / "scenes" / "battle" / "BattleScene.tscn"
README = ROOT / "README.md"
ROADMAP = ROOT / "docs" / "roadmap.md"


class PersistentCreaturesStaticTests(unittest.TestCase):
    def test_creature_cards_are_permanents_not_immediate_damage(self):
        cards = json.loads(CARDS.read_text(encoding="utf-8"))
        creatures = [card for card in cards if card.get("type") == "creature"]
        self.assertGreaterEqual(len(creatures), 4)

        for card in creatures:
            self.assertEqual(card.get("zone_after_play"), "battlefield")
            self.assertIn("attack", card)
            self.assertIn("health", card)
            self.assertGreater(card["attack"], 0)
            self.assertGreater(card["health"], 0)
            self.assertNotEqual(card.get("effect"), "damage")
            self.assertIn("permanent", card.get("text", "").lower())

    def test_combatant_tracks_battlefield_and_graveyard_zones(self):
        content = COMBATANT.read_text(encoding="utf-8")
        for snippet in [
            "var battlefield: Array = []",
            "var graveyard: Array = []",
            "func summon_creature(card: Dictionary) -> void:",
            '"name": str(card.get("name", card_id))',
            '"attack": int(card.get("attack", 0))',
            '"health": int(card.get("health", 1))',
            "battlefield.append(creature)",
            "func attack_with_creatures(target) -> int:",
            "for creature in battlefield:",
            "target.life = max(0, target.life - total_damage)",
            "func move_to_graveyard(card_id: String) -> void:",
            "graveyard.append(card_id)",
        ]:
            self.assertIn(snippet, content)

    def test_combatant_creatures_do_not_use_spell_effect_path(self):
        content = COMBATANT.read_text(encoding="utf-8")
        for snippet in [
            'if str(card.get("type", "")) == "creature":',
            "summon_creature(card)",
            "move_to_graveyard(card_id)",
            "apply_card_effect(card, target)",
        ]:
            self.assertIn(snippet, content)

    def test_battle_controller_runs_automatic_creature_attacks_each_turn(self):
        content = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            "func resolve_creature_attack(attacker, defender, attacker_label: String) -> void:",
            "var damage := attacker.attack_with_creatures(defender)",
            '"créatures attaquent"',
            "resolve_creature_attack(player, enemy, \"Tes\")",
            "resolve_creature_attack(enemy, player, enemy.name)",
            "refresh_battlefield_ui()",
        ]:
            self.assertIn(snippet, content)

    def test_battle_scene_displays_creatures_in_play(self):
        scene = SCENE.read_text(encoding="utf-8")
        script = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            "PlayerBattlefieldContainer",
            "EnemyBattlefieldContainer",
            "Champ de bataille joueur",
            "Champ de bataille ennemi",
        ]:
            self.assertIn(snippet, scene)
        for snippet in [
            "@onready var player_battlefield_container",
            "@onready var enemy_battlefield_container",
            "func refresh_battlefield_ui() -> void:",
            "func populate_battlefield(container: HBoxContainer, creatures: Array) -> void:",
            '"%s\\n%d/%d"',
        ]:
            self.assertIn(snippet, script)

    def test_readme_and_roadmap_mark_t016_done(self):
        readme = README.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")
        self.assertIn("### T016 — Créatures persistantes", readme)
        self.assertIn("permanents", readme)
        self.assertIn("champ de bataille", readme)
        self.assertIn("16. T016 — Créatures persistantes", roadmap)


if __name__ == "__main__":
    unittest.main()
