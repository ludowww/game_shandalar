import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "scripts" / "main" / "Main.gd"
GAMESTATE = ROOT / "scripts" / "core" / "GameState.gd"
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"
RUN_RESULT_SCRIPT = ROOT / "scripts" / "ui" / "RunResult.gd"
RUN_RESULT_SCENE = ROOT / "scenes" / "ui" / "RunResult.tscn"
README = ROOT / "README.md"


class RunResultStaticTests(unittest.TestCase):
    def test_main_routes_finished_runs_to_result_scene(self):
        content = MAIN.read_text(encoding="utf-8")
        for snippet in [
            'const RUN_RESULT_SCENE := preload("res://scenes/ui/RunResult.tscn")',
            'func show_run_result() -> void:',
            'if GameState.run_finished:',
            'show_run_result()',
            'current_scene.restart_requested.connect(restart_run)',
            'func restart_run() -> void:',
            'GameState.reset_run()',
        ]:
            self.assertIn(snippet, content)

    def test_battle_marks_boss_victory_as_run_win(self):
        content = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            'func is_current_enemy_boss() -> bool:',
            'if is_current_enemy_boss():',
            'GameState.finish_run(true)',
            'GameState.pending_reward_pool = ""',
            'Victoire finale.',
        ]:
            self.assertIn(snippet, content)

    def test_run_result_scene_and_script_exist(self):
        scene = RUN_RESULT_SCENE.read_text(encoding="utf-8")
        script = RUN_RESULT_SCRIPT.read_text(encoding="utf-8")
        for snippet in [
            'RunResult',
            'RunResult.gd',
            'TitleLabel',
            'StatsLabel',
            'RestartButton',
            'Recommencer',
        ]:
            self.assertIn(snippet, scene)
        for snippet in [
            'signal restart_requested',
            '@onready var title_label: Label = %TitleLabel',
            '@onready var stats_label: Label = %StatsLabel',
            '@onready var restart_button: Button = %RestartButton',
            'func refresh_result() -> void:',
            'if GameState.run_won:',
            'Victoire',
            'Défaite',
            'GameState.defeated_encounters.size()',
            'GameState.cards_added',
            'restart_requested.emit()',
        ]:
            self.assertIn(snippet, script)

    def test_gamestate_reset_clears_run_result(self):
        content = GAMESTATE.read_text(encoding="utf-8")
        for snippet in [
            'run_finished = false',
            'run_won = false',
            'cards_added = 0',
            'defeated_encounters = []',
            'player_life = 20',
        ]:
            self.assertIn(snippet, content)

    def test_readme_marks_t011_done(self):
        content = README.read_text(encoding="utf-8")
        self.assertIn('### T011 — Écran fin de run', content)
        self.assertIn('Victoire boss ou défaite joueur affiche un écran de résultat', content)


if __name__ == "__main__":
    unittest.main()
