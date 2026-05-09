extends Control

const WORLD_MAP_SCENE := preload("res://scenes/world/WorldMap.tscn")
const BATTLE_SCENE := preload("res://scenes/battle/BattleScene.tscn")

var current_scene: Node = null

func _ready() -> void:
	print("game_shandalar V0: Main scene loaded")
	show_world_map()

func show_world_map() -> void:
	_replace_scene(WORLD_MAP_SCENE)
	if current_scene.has_signal("battle_requested"):
		current_scene.battle_requested.connect(show_battle)

func show_battle() -> void:
	_replace_scene(BATTLE_SCENE)
	if current_scene.has_signal("battle_finished"):
		current_scene.battle_finished.connect(show_world_map)

func _replace_scene(scene: PackedScene) -> void:
	if current_scene != null:
		current_scene.queue_free()

	for child in get_children():
		child.queue_free()

	current_scene = scene.instantiate()
	add_child(current_scene)
