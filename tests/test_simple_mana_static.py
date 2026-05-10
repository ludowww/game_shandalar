import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "data" / "cards.json"
DECKS = ROOT / "data" / "decks.json"
COMBATANT = ROOT / "scripts" / "battle" / "Combatant.gd"
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"
AI = ROOT / "scripts" / "battle" / "SimpleAI.gd"
SCENE = ROOT / "scenes" / "battle" / "BattleScene.tscn"
README = ROOT / "README.md"
ROADMAP = ROOT / "docs" / "roadmap.md"


class SimpleManaStaticTests(unittest.TestCase):
    def test_cards_define_simple_lands_and_generic_costs(self):
        cards = json.loads(CARDS.read_text(encoding="utf-8"))
        land_cards = [card for card in cards if card.get("type") == "land"]
        non_land_cards = [card for card in cards if card.get("type") != "land"]

        self.assertGreaterEqual(len(land_cards), 1)
        for card in land_cards:
            self.assertEqual(card.get("zone_after_play"), "lands")
            self.assertEqual(card.get("mana_value"), 1)
            self.assertEqual(card.get("cost", 0), 0)

        for card in non_land_cards:
            self.assertIn("cost", card)
            self.assertGreaterEqual(card["cost"], 1)

    def test_decks_include_lands_for_player_and_enemies(self):
        cards = {card["id"]: card for card in json.loads(CARDS.read_text(encoding="utf-8"))}
        decks = json.loads(DECKS.read_text(encoding="utf-8"))
        for deck_id, card_ids in decks.items():
            lands = [card_id for card_id in card_ids if cards[card_id].get("type") == "land"]
            self.assertGreaterEqual(len(lands), 3, f"{deck_id} should include simple lands")

    def test_combatant_tracks_lands_mana_and_blocks_unpayable_cards(self):
        content = COMBATANT.read_text(encoding="utf-8")
        for snippet in [
            'const ZONE_LANDS := "Terrains"',
            "var lands: Array = []",
            "var current_mana := 0",
            "var land_played_this_turn := false",
            "func start_turn_resources() -> void:",
            "current_mana = total_mana_from_lands()",
            "land_played_this_turn = false",
            "func can_play_card(card: Dictionary) -> bool:",
            'if str(card.get("type", "")) == "land":',
            "return not land_played_this_turn",
            "return current_mana >= int(card.get(\"cost\", 0))",
            "func play_land(card: Dictionary) -> void:",
            "lands.append(land)",
            "land_played_this_turn = true",
            "func pay_mana_for(card: Dictionary) -> void:",
            "current_mana -= int(card.get(\"cost\", 0))",
            "hand.insert(card_index, card_id)",
        ]:
            self.assertIn(snippet, content)

    def test_creatures_and_spells_keep_existing_destinations_after_mana_payment(self):
        content = COMBATANT.read_text(encoding="utf-8")
        for snippet in [
            "pay_mana_for(card)",
            "summon_creature(card)",
            "apply_card_effect(card, target)",
            "move_to_graveyard(card_id)",
            '"lands": lands.size()',
            '"mana": current_mana',
        ]:
            self.assertIn(snippet, content)

    def test_battle_ui_shows_mana_and_lands_and_disables_unplayable_cards(self):
        scene = SCENE.read_text(encoding="utf-8")
        controller = BATTLE.read_text(encoding="utf-8")
        for snippet in ["ManaLabel", "Mana", "Terrains"]:
            self.assertIn(snippet, scene)
        for snippet in [
            "@onready var mana_label: Label = %ManaLabel",
            "func refresh_mana_ui() -> void:",
            "Mana joueur",
            "Terrains joueur",
            "Mana ennemi",
            "Terrains ennemi",
            "refresh_mana_ui()",
            "not player.can_play_card(card)",
            "Coût: %d",
            "Mana insuffisant ou terrain déjà joué.",
        ]:
            self.assertIn(snippet, controller)

    def test_ai_chooses_only_playable_cards(self):
        content = AI.read_text(encoding="utf-8")
        for snippet in [
            "for i in range(combatant.hand.size()):",
            "combatant.can_play_card(card)",
            "card_database",
        ]:
            self.assertIn(snippet, content)

    def test_readme_and_roadmap_mark_t018_done(self):
        readme = README.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")
        self.assertIn("### T018 — Mana simplifié / terrains", readme)
        self.assertIn("mana générique", readme.lower())
        self.assertIn("Terrains", readme)
        self.assertIn("T018 — Mana simplifié / terrains", roadmap)


if __name__ == "__main__":
    unittest.main()
