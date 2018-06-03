from math import *
from os import path
from PIL import Image, ImageMode

def sub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

def mul(p, k):
    return (p[0] * k, p[1] * k)

def length(v):
    return sqrt( v[0] ** 2 + v[1] ** 2 )

def normalize(v):
    l = length(v)
    return (v[0] / l, v[1] / l)

def dot (v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1];

def vec_dist_seq(p, l1, l2, check_borders = True):
    v = normalize( sub(l2, l1) )
    if check_borders and (dot(v, sub(p, l1) ) < 0 or dot(v, sub(p, l2) ) > 0):
        return (-1, (0, 0))

    e = normalize( (-v[1], v[0]) )
    r = dot(e, (p[0] - l1[0], p[1] - l1[1]) )
    return (r, e)

def float2int(x, f): # [-1.0, 1.0] => [0, f-1]
    x = max(-1.0, min(1.0, x))
    c = (x / 2.0 + 0.5) * (f - 1)
    if x >= 0.0:
        return ceil(c)
    else:
        return floor(c)

def vec2color(d, v):
    d_i = float2int(d, 1 << 16)

    x_i = float2int(v[0], 1 << 8)
    y_i = float2int(v[1], 1 << 8)

    return (x_i, y_i, d_i & 255, 255 - (d_i >> 8))

size = 17.5
glow_radius = 35
scale = 2

w = h = int((size + glow_radius) * 2 * scale)

# y is up

p0 = (0, size)
p1 = (sin(pi * 0.75) * size, cos(pi * 0.75) * size)
p2 = (0, -0.5 * size)

### hull.png

im = Image.new("RGBA", (w, h))
pix = im.load()

for j in range(0, h):
    for i in range(0, w):
        x = (i - w / 2 + 0.5) / scale
        y = -(j - h / 2 + 0.5) / scale

        if x < 0:
            x = -x
            x_mul = -1
        else:
            x_mul = 1

        p = (x, y)

        (d1, v1) = vec_dist_seq(p, p0, p1)
        (d2, v2) = vec_dist_seq(p, p1, p2)

        if d1 >= 0:
            (d, v) = (d1, v1)
        elif y >= p0[1]:
            v = sub(p, p0)
            (d, v) = (length(v), normalize(v))
        elif d2 >= 0:
            (d, v) = (d2, v2)
        elif x >= p1[0] or y <= p1[1]:
            v = sub(p, p1)
            (d, v) = (length(v), normalize(v))
        else:
            (d1, v1) = vec_dist_seq(p, p1, p0, False)
            (d2, v2) = vec_dist_seq(p, p2, p1, False)
            assert d1 >= 0.0 and d2 >= 0.0

            if d1 < d2:
                (d, v) = (-d1, v1)
            else:
                (d, v) = (-d2, v2)

        v = (v[0] * x_mul, v[1])
        pix[i, j] = vec2color(d / glow_radius, v)

im.show()
out_path = path.join(path.dirname(path.realpath(__file__)), '..', 'entity', 'ship', 'hull.png')
im.save(out_path, "PNG")

### part_front.png

part_size = length(sub(p0, p1))
w = int(glow_radius * 2 * scale)
h = int((glow_radius * 2 + part_size) * scale)

im = Image.new("RGBA", (w, h))
pix = im.load()

p3 = (0, part_size / 2)

for j in range(0, h):
    for i in range(0, w):
        x = (i - w / 2 + 0.5) / scale
        y = -(j - h / 2 + 0.5) / scale

        if y < 0:
            y = -y
            y_mul = -1
        else:
            y_mul = 1

        p = (x, y)

        if y < p3[1]:
            v = (x, 0)
        else:
            v = sub(p, p3)

        d = length(v)
        v = normalize(v)

        v = (v[0], v[1] * y_mul)
        pix[i, j] = vec2color(d / glow_radius, v)

im.show()
out_path = path.join(path.dirname(path.realpath(__file__)), '..', 'entity', 'ship', 'part_front.png')
im.save(out_path, "PNG")

### part_back.png

part_size = length(sub(p1, p2))
w = int(glow_radius * 2 * scale)
h = int((glow_radius * 2 + part_size) * scale)

im = Image.new("RGBA", (w, h))
pix = im.load()

p4 = (0, part_size / 2)

for j in range(0, h):
    for i in range(0, w):
        x = (i - w / 2 + 0.5) / scale
        y = -(j - h / 2 + 0.5) / scale

        if y < 0:
            y = -y
            y_mul = -1
        else:
            y_mul = 1

        p = (x, y)

        if y < p4[1]:
            v = (x, 0)
        else:
            v = sub(p, p4)

        d = length(v)
        v = normalize(v)

        v = (v[0], v[1] * y_mul)
        pix[i, j] = vec2color(d / glow_radius, v)

im.show()
out_path = path.join(path.dirname(path.realpath(__file__)), '..', 'entity', 'ship', 'part_back.png')
im.save(out_path, "PNG")


### particle.png

glow_radius = 10

w = int(glow_radius * 2 * scale)
h = int(glow_radius * 2 * scale)

im = Image.new("RGBA", (w, h))
pix = im.load()

for j in range(0, h):
    for i in range(0, w):
        x = (i - w / 2 + 0.5) / scale
        y = -(j - h / 2 + 0.5) / scale

        v = (x, y)
        d = length(v)
        v = normalize(v)

        pix[i, j] = vec2color(d / glow_radius, v)

im.show()
out_path = path.join(path.dirname(path.realpath(__file__)), '..', 'entity', 'particle.png')
im.save(out_path, "PNG")
