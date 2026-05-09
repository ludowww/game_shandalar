import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATALOADER = ROOT / "scripts" / "core" / "DataLoader.gd"
PROJECT = ROOT / "project.godot"


class DataLoaderStaticTests(unittest.TestCase):
    def test_dataloader_script_exposes_json_loading_api(self):
        content = DATALOADER.read_text(encoding="utf-8")

        expected_snippets = [
            "extends Node",
            "func load_json_file(path: String)",
            "FileAccess.file_exists(path)",
            "FileAccess.open(path, FileAccess.READ)",
            "JSON.parse_string",
            "push_error",
            "return null",
        ]

        for snippet in expected_snippets:
            self.assertIn(snippet, content)

    def test_dataloader_script_exposes_v0_data_helpers(self):
        content = DATALOADER.read_text(encoding="utf-8")

        expected_snippets = [
            "func load_cards()",
            "func load_decks()",
            "func load_enemies()",
            "func load_map()",
            "func load_rewards()",
            '"res://data/cards.json"',
            '"res://data/decks.json"',
            '"res://data/enemies.json"',
            '"res://data/map_mvp.json"',
            '"res://data/rewards.json"',
        ]

        for snippet in expected_snippets:
            self.assertIn(snippet, content)

    def test_dataloader_is_registered_as_autoload(self):
        content = PROJECT.read_text(encoding="utf-8")

        self.assertIn("[autoload]", content)
        self.assertIn('DataLoader="*res://scripts/core/DataLoader.gd"', content)


if __name__ == "__main__":
    unittest.main()
