extends Control

const WORLD_MAP_SCENE := preload("res://scenes/world/WorldMap.tscn")
const BATTLE_SCENE := preload("res://scenes/battle/BattleScene.tscn")
const REWARD_SCENE := preload("res://scenes/reward/RewardScene.tscn")
const MERCHANT_SCENE := preload("res://scenes/merchant/MerchantScene.tscn")
const RUN_RESULT_SCENE := preload("res://scenes/ui/RunResult.tscn")

var current_scene: Node = null

func _ready() -> void:
	print("game_shandalar V0: Main scene loaded")
	show_world_map()

func show_world_map() -> void:
	if GameState.run_finished:
		show_run_result()
		return
	_replace_scene(WORLD_MAP_SCENE)
	if current_scene.has_signal("battle_requested"):
		current_scene.battle_requested.connect(show_battle)
	if current_scene.has_signal("reward_requested"):
		current_scene.reward_requested.connect(show_reward)
	if current_scene.has_signal("shop_requested"):
		current_scene.shop_requested.connect(show_merchant)

func show_battle() -> void:
	_replace_scene(BATTLE_SCENE)
	if current_scene.has_signal("battle_finished"):
		current_scene.battle_finished.connect(show_after_battle)

func show_after_battle() -> void:
	if GameState.run_finished:
		show_run_result()
	elif GameState.last_battle_won and GameState.pending_reward_pool != "":
		show_reward()
	else:
		show_world_map()

func show_reward() -> void:
	_replace_scene(REWARD_SCENE)
	if current_scene.has_signal("reward_finished"):
		current_scene.reward_finished.connect(show_world_map)

func show_merchant() -> void:
	_replace_scene(MERCHANT_SCENE)
	if current_scene.has_signal("merchant_finished"):
		current_scene.merchant_finished.connect(show_world_map)

func show_run_result() -> void:
	_replace_scene(RUN_RESULT_SCENE)
	if current_scene.has_signal("restart_requested"):
		current_scene.restart_requested.connect(restart_run)

func restart_run() -> void:
	GameState.reset_run()
	show_world_map()

func _replace_scene(scene: PackedScene) -> void:
	if current_scene != null:
		current_scene.queue_free()

	for child in get_children():
		child.queue_free()

	current_scene = scene.instantiate()
	add_child(current_scene)
