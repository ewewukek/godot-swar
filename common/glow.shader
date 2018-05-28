shader_type canvas_item;
render_mode blend_add;

uniform float glow_radius;

void fragment() {
	float line_width = 0.5;

	vec4 texel = texture(TEXTURE, UV);
	float dist = texel.r * 255.0 + texel.g; // distance

	float x = (dist - line_width) / glow_radius;
	float v = (1.0 - x) / (1.0 + 10.0 * x); // gradient curve

	// small trick to avoid extra `if` statement
	// equivalent to `v = (x > 0) ? v : 1`
	float t = sign(1.0 + sign(x));
	v = (1.0 - t) + t * v;

	COLOR = vec4(COLOR.rgb * v, COLOR.a);
}
