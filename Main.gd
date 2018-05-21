extends Node

var step_time = float()

var input_turn_mod = 10
var input_turn = float()

var player_ship

func _ready():
	player_ship = preload("res://entity/ship/Ship.tscn").instance()
	player_ship.position.x = ProjectSettings.get_setting("display/window/size/width") / 2
	player_ship.position.y = ProjectSettings.get_setting("display/window/size/height") / 2
	player_ship.add_to_group("updated")
	add_child(player_ship)

func _process(dt):
	if Input.is_action_pressed("input_quit"):
		get_tree().quit()
		return

	player_ship.input_turn = 0
	if Input.is_action_pressed("input_left"):
		input_turn = max(-1, input_turn - input_turn_mod * dt)
	elif Input.is_action_pressed("input_right"):
		input_turn = min(1, input_turn + input_turn_mod * dt)
	else:
		input_turn = 0
	player_ship.input_turn = input_turn
	player_ship.input_thrust = Input.is_action_pressed("input_thrust")
	player_ship.input_fire = Input.is_action_pressed("input_fire")

	step_time += dt
	while step_time > Constants.TIME_STEP:
		get_tree().call_group("updated", "update", step_time)
		step_time -= Constants.TIME_STEP
