import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "data" / "cards.json"
DECKS = ROOT / "data" / "decks.json"
ENEMIES = ROOT / "data" / "enemies.json"
MAP = ROOT / "data" / "map_mvp.json"


class GameDataStaticTests(unittest.TestCase):
    def setUp(self):
        self.cards = json.loads(CARDS.read_text(encoding="utf-8"))
        self.decks = json.loads(DECKS.read_text(encoding="utf-8"))
        self.enemies = json.loads(ENEMIES.read_text(encoding="utf-8"))
        self.map_data = json.loads(MAP.read_text(encoding="utf-8"))
        self.card_ids = {card["id"] for card in self.cards}

    def test_cards_define_v0_damage_heal_and_creature_effects(self):
        card_ids = self.card_ids
        for required_id in ["soldier_2_2", "wolf_3_1", "firebolt", "healing_light"]:
            self.assertIn(required_id, card_ids)

        effects = {card.get("effect") for card in self.cards}
        self.assertIn("damage", effects)
        self.assertIn("heal", effects)

        for card in self.cards:
            self.assertIn("id", card)
            self.assertIn("name", card)
            self.assertIn("type", card)
            self.assertIn("text", card)
            self.assertIn(card["type"], ["spell", "creature"])
            if card.get("effect") in ["damage", "heal"]:
                self.assertIsInstance(card.get("value"), int)
                self.assertGreater(card["value"], 0)

    def test_decks_reference_existing_cards(self):
        for required_deck in ["player_start", "goblin_weak", "mage_medium", "boss_seal_guardian"]:
            self.assertIn(required_deck, self.decks)
            self.assertGreaterEqual(len(self.decks[required_deck]), 4)

        for deck_id, card_refs in self.decks.items():
            self.assertIsInstance(card_refs, list)
            for card_id in card_refs:
                self.assertIn(card_id, self.card_ids, f"{deck_id} references missing card {card_id}")

    def test_enemies_reference_existing_decks_and_map_enemy_ids(self):
        deck_ids = set(self.decks.keys())
        enemy_ids = {enemy["id"] for enemy in self.enemies}
        map_enemy_ids = {
            tile["enemy_id"]
            for tile in self.map_data["tiles"]
            if tile.get("type") in ["enemy", "boss"]
        }

        self.assertTrue(map_enemy_ids.issubset(enemy_ids))

        for enemy in self.enemies:
            self.assertIn("id", enemy)
            self.assertIn("name", enemy)
            self.assertIn("life", enemy)
            self.assertIn("deck_id", enemy)
            self.assertIn(enemy["deck_id"], deck_ids)
            self.assertGreater(enemy["life"], 0)

        boss = next(enemy for enemy in self.enemies if enemy["id"] == "boss_seal_guardian")
        self.assertTrue(boss.get("is_boss"))
        self.assertIsNone(boss.get("reward_pool"))


if __name__ == "__main__":
    unittest.main()
