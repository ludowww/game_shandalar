import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"
CARDS = ROOT / "data" / "cards.json"
DECKS = ROOT / "data" / "decks.json"
ENEMIES = ROOT / "data" / "enemies.json"


class BattlePlayabilityStaticTests(unittest.TestCase):
    def test_player_draws_after_playing_a_card(self):
        content = BATTLE.read_text(encoding="utf-8")
        self.assertIn("func draw_player_card() -> void:", content)
        self.assertIn("draw_player_card()", content)
        self.assertIn("player.draw_card()", content)

    def test_starting_deck_has_enough_damage_for_first_enemy(self):
        cards = {card["id"]: card for card in json.loads(CARDS.read_text(encoding="utf-8"))}
        decks = json.loads(DECKS.read_text(encoding="utf-8"))
        enemies = {enemy["id"]: enemy for enemy in json.loads(ENEMIES.read_text(encoding="utf-8"))}
        starting_pressure = sum(
            int(cards[card_id].get("value", 0)) if cards[card_id].get("effect") == "damage" else int(cards[card_id].get("attack", 0))
            for card_id in decks["player_start"]
            if cards[card_id].get("effect") == "damage" or cards[card_id].get("type") == "creature"
        )
        self.assertGreaterEqual(starting_pressure, enemies["goblin_weak_01"]["life"])


if __name__ == "__main__":
    unittest.main()
