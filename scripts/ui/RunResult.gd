extends Control

signal restart_requested

@onready var title_label: Label = %TitleLabel
@onready var stats_label: Label = %StatsLabel
@onready var restart_button: Button = %RestartButton

func _ready() -> void:
	restart_button.pressed.connect(_on_restart_button_pressed)
	refresh_result()

func refresh_result() -> void:
	if GameState.run_won:
		title_label.text = "Victoire"
	else:
		title_label.text = "Défaite"

	stats_label.text = "Ennemis vaincus : %d\nCartes gagnées : %d\nPV restants : %d" % [
		GameState.defeated_encounters.size(),
		GameState.cards_added,
		GameState.player_life,
	]

func _on_restart_button_pressed() -> void:
	restart_requested.emit()
