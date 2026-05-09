import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "scripts" / "main" / "Main.gd"
GAMESTATE = ROOT / "scripts" / "core" / "GameState.gd"
REWARD_SCRIPT = ROOT / "scripts" / "reward" / "RewardController.gd"
REWARD_SCENE = ROOT / "scenes" / "reward" / "RewardScene.tscn"
REWARDS = ROOT / "data" / "rewards.json"
CARDS = ROOT / "data" / "cards.json"
ENEMIES = ROOT / "data" / "enemies.json"


class RewardFlowStaticTests(unittest.TestCase):
    def test_reward_data_exists_and_references_valid_cards(self):
        rewards = json.loads(REWARDS.read_text(encoding="utf-8"))
        cards = {card["id"] for card in json.loads(CARDS.read_text(encoding="utf-8"))}
        self.assertIn("weak_reward", rewards)
        self.assertIn("medium_reward", rewards)
        for pool_id, pool in rewards.items():
            self.assertGreaterEqual(len(pool), 3, pool_id)
            for card_id in pool:
                self.assertIn(card_id, cards)

    def test_non_boss_enemies_have_reward_pools(self):
        rewards = json.loads(REWARDS.read_text(encoding="utf-8"))
        enemies = json.loads(ENEMIES.read_text(encoding="utf-8"))
        for enemy in enemies:
            if enemy.get("is_boss"):
                self.assertIsNone(enemy.get("reward_pool"))
            else:
                self.assertIn(enemy.get("reward_pool"), rewards)

    def test_gamestate_can_add_rewards_to_deck(self):
        content = GAMESTATE.read_text(encoding="utf-8")
        for snippet in [
            "func add_card_to_deck(card_id: String) -> void:",
            "player_deck.append(card_id)",
            "cards_added += 1",
            'reward_pending = false',
            'pending_reward_pool = ""',
        ]:
            self.assertIn(snippet, content)

    def test_main_routes_victory_to_reward_scene(self):
        content = MAIN.read_text(encoding="utf-8")
        for snippet in [
            'const REWARD_SCENE := preload("res://scenes/reward/RewardScene.tscn")',
            'func show_after_battle() -> void:',
            'func show_reward() -> void:',
            'GameState.last_battle_won and GameState.pending_reward_pool != ""',
            'current_scene.reward_finished.connect(show_world_map)',
        ]:
            self.assertIn(snippet, content)

    def test_reward_controller_presents_three_choices_and_adds_card(self):
        content = REWARD_SCRIPT.read_text(encoding="utf-8")
        for snippet in [
            'signal reward_finished',
            'const DataLoaderScript = preload("res://scripts/core/DataLoader.gd")',
            'var data_loader := DataLoaderScript.new()',
            'func show_rewards() -> void:',
            'func choose_reward(card_id: String) -> void:',
            'GameState.add_card_to_deck(card_id)',
            'reward_finished.emit()',
            'for i in range(min(3, pool.size())):',
            'button.pressed.connect(choose_reward.bind(card_id))',
        ]:
            self.assertIn(snippet, content)

    def test_reward_scene_has_required_nodes(self):
        content = REWARD_SCENE.read_text(encoding="utf-8")
        for snippet in [
            'RewardScene',
            'RewardController.gd',
            'RewardChoices',
            'StatusLabel',
            'Choisis une récompense',
        ]:
            self.assertIn(snippet, content)


if __name__ == "__main__":
    unittest.main()
