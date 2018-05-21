extends KinematicBody2D

var velocity = Vector2()
var angular_velocity = float()

func _process(dt):
	dt /= Constants.TIME_STEP
	position += velocity * dt
	rotation += angular_velocity * dt
