import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "data" / "cards.json"
DECKS = ROOT / "data" / "decks.json"
ENEMIES = ROOT / "data" / "enemies.json"
README = ROOT / "README.md"
ROADMAP = ROOT / "docs" / "roadmap.md"


class V1BalanceStaticTests(unittest.TestCase):
    def setUp(self):
        self.cards = {card["id"]: card for card in json.loads(CARDS.read_text(encoding="utf-8"))}
        self.decks = json.loads(DECKS.read_text(encoding="utf-8"))
        self.enemies = json.loads(ENEMIES.read_text(encoding="utf-8"))

    def card_cost(self, card_id):
        return int(self.cards[card_id].get("cost", 0))

    def non_land_cards(self, deck_id):
        return [card_id for card_id in self.decks[deck_id] if self.cards[card_id]["type"] != "land"]

    def test_starting_deck_has_stable_v1_mana_curve(self):
        starter = self.decks["player_start"]
        non_lands = self.non_land_cards("player_start")
        self.assertGreaterEqual(starter.count("forest"), 7)
        self.assertGreaterEqual(len(starter), 16)
        self.assertGreaterEqual(sum(1 for card_id in non_lands if self.card_cost(card_id) <= 2), 6)
        self.assertNotIn("air_elemental", starter)
        self.assertNotIn("craw_wurm", starter)

    def test_weak_enemies_stay_early_game_safe(self):
        weak_enemy_decks = {
            enemy["deck_id"] for enemy in self.enemies if enemy.get("reward_pool") == "weak_reward"
        }
        weak_lives = [enemy["life"] for enemy in self.enemies if enemy.get("reward_pool") == "weak_reward"]
        self.assertLessEqual(max(weak_lives), 13)
        for deck_id in weak_enemy_decks:
            non_lands = self.non_land_cards(deck_id)
            self.assertGreaterEqual(self.decks[deck_id].count("forest"), 5)
            self.assertLessEqual(max(self.card_cost(card_id) for card_id in non_lands), 3)
            self.assertNotIn("lightning_bolt", self.decks[deck_id])
            self.assertNotIn("craw_wurm", self.decks[deck_id])

    def test_medium_and_boss_danger_progression_is_clear(self):
        weak_life_max = max(enemy["life"] for enemy in self.enemies if enemy.get("reward_pool") == "weak_reward")
        medium_enemies = [enemy for enemy in self.enemies if enemy.get("reward_pool") == "medium_reward"]
        boss = next(enemy for enemy in self.enemies if enemy.get("is_boss"))

        self.assertTrue(all(enemy["life"] > weak_life_max for enemy in medium_enemies))
        self.assertGreater(boss["life"], max(enemy["life"] for enemy in medium_enemies))

        for enemy in medium_enemies:
            deck = self.decks[enemy["deck_id"]]
            medium_threats = [card_id for card_id in self.non_land_cards(enemy["deck_id"]) if 4 <= self.card_cost(card_id) <= 5]
            self.assertGreaterEqual(deck.count("forest"), 6)
            self.assertGreaterEqual(len(medium_threats), 2)
            self.assertNotIn("craw_wurm", deck)

        boss_deck = self.decks[boss["deck_id"]]
        self.assertGreaterEqual(boss_deck.count("forest"), 8)
        self.assertIn("craw_wurm", boss_deck)
        self.assertIn("air_elemental", boss_deck)
        self.assertGreaterEqual(boss_deck.count("lightning_bolt"), 2)

    def test_readme_and_roadmap_mark_t022_done(self):
        readme = README.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")
        self.assertIn("### T022 — Playtest & équilibrage V1", readme)
        self.assertIn("courbe de mana", readme)
        self.assertIn("danger progressif", readme)
        self.assertIn("T022 — Playtest & équilibrage V1", roadmap)


if __name__ == "__main__":
    unittest.main()
