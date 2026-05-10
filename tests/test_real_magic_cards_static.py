import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "data" / "cards.json"
DECKS = ROOT / "data" / "decks.json"
REWARDS = ROOT / "data" / "rewards.json"
README = ROOT / "README.md"
ROADMAP = ROOT / "docs" / "roadmap.md"


class RealMagicCardsStaticTests(unittest.TestCase):
    def setUp(self):
        self.cards = json.loads(CARDS.read_text(encoding="utf-8"))
        self.cards_by_id = {card["id"]: card for card in self.cards}
        self.decks = json.loads(DECKS.read_text(encoding="utf-8"))
        self.rewards = json.loads(REWARDS.read_text(encoding="utf-8"))

    def test_simple_real_magic_cards_are_present(self):
        expected = {
            "grizzly_bears": ("Grizzly Bears", "creature", 2, 2, 2),
            "savannah_lions": ("Savannah Lions", "creature", 1, 2, 1),
            "hill_giant": ("Hill Giant", "creature", 4, 3, 3),
            "lightning_bolt": ("Lightning Bolt", "spell", 1, None, None),
            "shock": ("Shock", "spell", 1, None, None),
            "healing_salve": ("Healing Salve", "spell", 1, None, None),
            "forest": ("Forest", "land", 0, None, None),
        }
        for card_id, (name, card_type, cost, attack, health) in expected.items():
            self.assertIn(card_id, self.cards_by_id)
            card = self.cards_by_id[card_id]
            self.assertEqual(card["name"], name)
            self.assertEqual(card["type"], card_type)
            self.assertEqual(card["cost"], cost)
            self.assertEqual(card.get("source"), "real_magic_simple")
            self.assertIn("magic_card", card)
            if card_type == "creature":
                self.assertEqual(card["attack"], attack)
                self.assertEqual(card["health"], health)
                self.assertEqual(card["zone_after_play"], "battlefield")
            if card_type == "land":
                self.assertEqual(card["zone_after_play"], "lands")
                self.assertEqual(card["mana_value"], 1)

    def test_real_magic_cards_use_supported_simple_effects_only(self):
        supported_effects = {"summon", "damage", "heal", "mana"}
        for card in self.cards:
            self.assertIn(card["effect"], supported_effects)
            self.assertNotIn("stack", card)
            self.assertNotIn("priority", card)
            self.assertNotIn("instant_timing", card)

    def test_decks_and_rewards_use_real_magic_cards(self):
        all_real_ids = {card["id"] for card in self.cards if card.get("source") == "real_magic_simple"}
        for deck_id, card_ids in self.decks.items():
            self.assertTrue(set(card_ids).issubset(all_real_ids), f"{deck_id} contains non-real placeholder cards")
            self.assertGreaterEqual(card_ids.count("forest"), 4)

        for pool_id, card_ids in self.rewards.items():
            self.assertTrue(set(card_ids).issubset(all_real_ids), f"{pool_id} contains non-real placeholder cards")
            self.assertGreaterEqual(len(card_ids), 4)

    def test_readme_and_roadmap_mark_t021_done(self):
        readme = README.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")
        self.assertIn("### T021 — Cartes Magic simples réelles", readme)
        self.assertIn("Grizzly Bears", readme)
        self.assertIn("Lightning Bolt", readme)
        self.assertIn("Forest", readme)
        self.assertIn("T021 — Cartes Magic simples réelles", roadmap)


if __name__ == "__main__":
    unittest.main()
