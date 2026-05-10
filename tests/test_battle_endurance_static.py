import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECK_SCRIPT = ROOT / "scripts" / "battle" / "Deck.gd"
COMBATANT_SCRIPT = ROOT / "scripts" / "battle" / "Combatant.gd"
CARDS = ROOT / "data" / "cards.json"
DECKS = ROOT / "data" / "decks.json"
ENEMIES = ROOT / "data" / "enemies.json"
REWARDS = ROOT / "data" / "rewards.json"


class BattleEnduranceStaticTests(unittest.TestCase):
    def test_deck_recycles_discard_when_empty(self):
        deck = DECK_SCRIPT.read_text(encoding="utf-8")
        combatant = COMBATANT_SCRIPT.read_text(encoding="utf-8")
        for snippet in [
            "var discard_pile: Array = []",
            "func discard(card_id: String) -> void:",
            "func reshuffle_discard_into_deck() -> void:",
            "reshuffle_discard_into_deck()",
        ]:
            self.assertIn(snippet, deck)
        self.assertIn("deck.discard(card_id)", combatant)

    def test_cards_and_decks_have_enough_variety_for_boss_run(self):
        cards = {card["id"]: card for card in json.loads(CARDS.read_text(encoding="utf-8"))}
        decks = json.loads(DECKS.read_text(encoding="utf-8"))
        enemies = {enemy["id"]: enemy for enemy in json.loads(ENEMIES.read_text(encoding="utf-8"))}

        self.assertGreaterEqual(len(cards), 10)
        self.assertGreaterEqual(len(set(decks["player_start"])), 7)
        self.assertGreaterEqual(len(decks["player_start"]), 10)
        self.assertGreaterEqual(len(set(decks["boss_seal_guardian"])), 7)
        self.assertGreaterEqual(len(decks["boss_seal_guardian"]), 10)

        player_pressure = sum(
            int(cards[card_id].get("value", 0)) if cards[card_id].get("effect") == "damage" else int(cards[card_id].get("attack", 0))
            for card_id in decks["player_start"]
            if cards[card_id].get("effect") == "damage" or cards[card_id].get("type") == "creature"
        )
        boss_life = enemies["boss_seal_guardian"]["life"]
        self.assertGreaterEqual(player_pressure, boss_life)

    def test_reward_pools_offer_more_than_three_options(self):
        rewards = json.loads(REWARDS.read_text(encoding="utf-8"))
        for pool_id, pool in rewards.items():
            self.assertGreaterEqual(len(pool), 5, pool_id)
            self.assertGreaterEqual(len(set(pool)), 5, pool_id)


if __name__ == "__main__":
    unittest.main()
