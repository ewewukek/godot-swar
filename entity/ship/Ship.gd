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
	else:
		speed = max(0, velocity.length() - friction)
	velocity = velocity.clamped(speed)

	next_position = position + velocity
	next_rotation = rotation + angular_velocity

	get_node("EffectExhaust").emitting = input_thrust

func add_part(texture, pivot):
	var part = preload("res://entity/ship/Part.tscn").instance()
	part.modulate = $Sprite.modulate
	part.texture = texture
	part.position = pivot.global_position
	part.rotation = pivot.global_rotation
	part.velocity = (pivot.position * 0.1).rotated(rotation)
	part.velocity += velocity * 0.1
	part.angular_velocity = (randf() - 0.5) * 0.1
	get_parent().add_child(part)

func explode():
	var front = preload("res://entity/ship/part_front.png")
	var back = preload("res://entity/ship/part_back.png")
	add_part(front, $Parts/FrontRight)
	add_part(front, $Parts/FrontLeft)
	add_part(back, $Parts/BackRight)
	add_part(back, $Parts/BackLeft)
