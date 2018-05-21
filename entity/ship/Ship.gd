extends 'res://entity/Base.gd'

export (float) var acceleration = 5
export (float) var max_velocity = 12
export (float) var friction = 1.2

export (float) var turn_acceleration = 18
export (float) var min_angular_velocity = 1
export (float) var max_angular_velocity = 18
export (float) var angular_friction = 0.5

var next_position
var next_rotation

var input_turn = float()
var input_thrust = bool()
var input_fire = bool()

func _ready():
	turn_acceleration = deg2rad(turn_acceleration)
	min_angular_velocity = deg2rad(min_angular_velocity)
	max_angular_velocity = deg2rad(max_angular_velocity)

	next_position = position
	next_rotation = rotation

func update(dt):
	position = next_position
	rotation = next_rotation

	angular_velocity *= angular_friction
	if abs(angular_velocity) < min_angular_velocity:
		angular_velocity = 0
	angular_velocity += clamp(input_turn, -1, 1) * turn_acceleration
	angular_velocity = clamp(angular_velocity, -max_angular_velocity, max_angular_velocity)

	var speed
	if input_thrust:
		velocity += Vector2(0, -1).rotated(rotation) * acceleration
		speed = min(velocity.length(), max_velocity)
# 		velocity = Vector2(max_velocity * 20, 0)
# 		rotation = deg2rad(90)
	else:
		speed = max(0, velocity.length() - friction)
	velocity = velocity.clamped(speed)

	next_position = position + velocity
	next_rotation = rotation + angular_velocity