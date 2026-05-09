import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORLD_MAP = ROOT / "scripts" / "world" / "WorldMap.gd"
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"
MAIN = ROOT / "scripts" / "main" / "Main.gd"


class AutoloadReferenceStaticTests(unittest.TestCase):
    def test_runtime_scripts_do_not_depend_on_bare_dataloader_identifier(self):
        for path in [WORLD_MAP, BATTLE]:
            content = path.read_text(encoding="utf-8")
            self.assertNotIn("DataLoader.load_", content, f"{path} should use a local data_loader instance")
            self.assertIn('preload("res://scripts/core/DataLoader.gd")', content)
            self.assertIn("data_loader", content)

    def test_main_preloads_battle_by_path_not_uid_only(self):
        content = MAIN.read_text(encoding="utf-8")
        self.assertIn('preload("res://scenes/battle/BattleScene.tscn")', content)
        self.assertNotIn('uid://battlescenev0', content)


if __name__ == "__main__":
    unittest.main()
