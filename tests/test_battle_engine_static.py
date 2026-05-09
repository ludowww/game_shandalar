import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"
DECK = ROOT / "scripts" / "battle" / "Deck.gd"
COMBATANT = ROOT / "scripts" / "battle" / "Combatant.gd"
AI = ROOT / "scripts" / "battle" / "SimpleAI.gd"
SCENE = ROOT / "scenes" / "battle" / "BattleScene.tscn"


class BattleEngineStaticTests(unittest.TestCase):
    def test_deck_exposes_shuffle_draw_and_empty_handling(self):
        content = DECK.read_text(encoding="utf-8")
        for snippet in [
            "extends RefCounted",
            "func setup(card_ids: Array) -> void:",
            "func draw()",
            "func draw_many(count: int) -> Array:",
            "cards.shuffle()",
            "return null",
        ]:
            self.assertIn(snippet, content)

    def test_combatant_exposes_life_deck_hand_and_card_effects(self):
        content = COMBATANT.read_text(encoding="utf-8")
        for snippet in [
            "extends RefCounted",
            "var life := 20",
            "var deck := Deck.new()",
            "var hand: Array = []",
            "func draw_card()",
            "func apply_card_effect(card: Dictionary, target)",
            '"damage"',
            '"heal"',
            "func is_dead() -> bool:",
        ]:
            self.assertIn(snippet, content)

    def test_simple_ai_plays_first_card(self):
        content = AI.read_text(encoding="utf-8")
        for snippet in [
            "extends RefCounted",
            "func choose_card_index(combatant) -> int:",
            "return 0",
            "return -1",
        ]:
            self.assertIn(snippet, content)

    def test_battle_controller_initializes_turns_and_resolution(self):
        content = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            "extends Control",
            "const Deck = preload(\"res://scripts/battle/Deck.gd\")",
            "const Combatant = preload(\"res://scripts/battle/Combatant.gd\")",
            "const SimpleAI = preload(\"res://scripts/battle/SimpleAI.gd\")",
            "func start_battle(enemy_id: String) -> void:",
            "func play_player_card(card_index: int) -> void:",
            "func enemy_turn() -> void:",
            "func check_battle_end() -> bool:",
            "GameState.current_enemy_id",
            "data_loader.load_cards()",
            "data_loader.load_decks()",
            "data_loader.load_enemies()",
        ]:
            self.assertIn(snippet, content)

    def test_battle_scene_exists_and_uses_controller(self):
        content = SCENE.read_text(encoding="utf-8")
        self.assertIn('path="res://scripts/battle/BattleController.gd"', content)
        self.assertIn('PlayerLifeLabel', content)
        self.assertIn('EnemyLifeLabel', content)
        self.assertIn('HandContainer', content)
        self.assertIn('LogLabel', content)


if __name__ == "__main__":
    unittest.main()
