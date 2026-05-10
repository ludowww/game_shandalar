import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATTLE = ROOT / "scripts" / "battle" / "BattleController.gd"
SCENE = ROOT / "scenes" / "battle" / "BattleScene.tscn"
README = ROOT / "README.md"
ROADMAP = ROOT / "docs" / "roadmap.md"


class SimplifiedMagicTurnStaticTests(unittest.TestCase):
    def test_battle_controller_defines_simplified_magic_phases(self):
        content = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            'const PHASE_BEGIN := "Début de tour"',
            'const PHASE_UNTAP := "Dégagement / ressources"',
            'const PHASE_DRAW := "Pioche"',
            'const PHASE_MAIN := "Phase principale"',
            'const PHASE_COMBAT := "Combat automatique"',
            'const PHASE_END := "Fin de tour"',
            'var current_phase := PHASE_BEGIN',
            'func set_phase(phase_name: String) -> void:',
            'phase_label.text = "Phase : %s" % current_phase',
        ]:
            self.assertIn(snippet, content)

    def test_turn_flow_clarifies_resources_draw_main_combat_and_end(self):
        content = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            'func begin_player_turn() -> void:',
            'set_phase(PHASE_BEGIN)',
            'set_phase(PHASE_UNTAP)',
            'player.start_turn_resources()',
            '"mana disponible"',
            'set_phase(PHASE_DRAW)',
            'draw_player_card()',
            '"pioche"',
            'set_phase(PHASE_MAIN)',
            '"phase principale"',
            'func resolve_player_combat_step() -> bool:',
            'set_phase(PHASE_COMBAT)',
            'resolve_creature_attack(player, enemy, "Tes")',
            'player.ready_creatures_for_next_turn()',
            'set_phase(PHASE_END)',
        ]:
            self.assertIn(snippet, content)

    def test_enemy_turn_uses_same_simplified_phase_steps(self):
        content = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            'func enemy_turn() -> void:',
            'set_phase(PHASE_BEGIN)',
            'set_phase(PHASE_UNTAP)',
            'enemy.start_turn_resources()',
            'set_phase(PHASE_DRAW)',
            'enemy.draw_card()',
            'set_phase(PHASE_MAIN)',
            'ai.choose_card_index(enemy, card_database)',
            'set_phase(PHASE_COMBAT)',
            'resolve_creature_attack(enemy, player, enemy.name)',
            'enemy.ready_creatures_for_next_turn()',
            'set_phase(PHASE_END)',
        ]:
            self.assertIn(snippet, content)

    def test_battle_scene_displays_current_phase(self):
        scene = SCENE.read_text(encoding="utf-8")
        controller = BATTLE.read_text(encoding="utf-8")
        for snippet in [
            "PhaseLabel",
            "Phase : Début de tour",
        ]:
            self.assertIn(snippet, scene)
        self.assertIn("@onready var phase_label: Label = %PhaseLabel", controller)
        self.assertIn("set_phase(current_phase)", controller)

    def test_readme_and_roadmap_mark_t019_done(self):
        readme = README.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")
        self.assertIn("### T019 — Tour Magic simplifié", readme)
        self.assertIn("Début de tour", readme)
        self.assertIn("Dégagement / reset ressources", readme)
        self.assertIn("Pioche", readme)
        self.assertIn("Phase principale", readme)
        self.assertIn("Combat automatique", readme)
        self.assertIn("Fin de tour", readme)
        self.assertIn("T019 — Tour Magic simplifié", roadmap)


if __name__ == "__main__":
    unittest.main()
