shader_type canvas_item;
render_mode blend_add;

uniform float glow_radius;

vec2 read_dir(vec4 texel) {
	return normalize(texel.rg * 2.0 - 1.0);
}

float read_dist(vec4 texel) {
	return ((1.0 - texel.a) * 255.0 + texel.b) / 128.0 - 1.0;
}

void fragment() {
	float line_width = 0.5 / glow_radius;

	vec4 texel = texture(TEXTURE, UV);
	float dist = read_dist(texel);

	if (abs(dist) >= 1.0) discard;

	if (dist >= 0.0) {
	} else {
		dist = -dist;
	}

	float x = (dist - line_width / glow_radius);
	float v = (1.0 - x) / (1.0 + 10.0 * x); // gradient curve

	// small trick to avoid extra `if` statement
	// equivalent to `v = (x > 0) ? v : 1`
	float t = sign(1.0 + sign(x));
	v = (1.0 - t) + t * v;

	COLOR = vec4(COLOR.rgb * v, COLOR.a);
}
