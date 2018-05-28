extends "res://entity/Base.gd"

export (float) var lifetime = 1.2

func _process(dt):
	modulate.a = min(1, lifetime)
	lifetime -= dt
	if lifetime <= 0:
		queue_free()