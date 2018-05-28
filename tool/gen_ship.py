from math import *
from os import path
from PIL import Image, ImageMode

def sub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

def length(v):
    return sqrt( v[0] ** 2 + v[1] ** 2 )

def dist(p1, p2):
    return length( sub(p1, p2) )

def normalize(v):
    l = length(v)
    return (v[0] / l, v[1] / l)

def dot (v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1];

def dist_seq(p, l1, l2, check_borders = True):
    v = normalize( sub(l2, l1) )
    if check_borders and (dot(v, sub(p, l1) ) < 0 or dot(v, sub(p, l2) ) > 0):
        return -1

    e = normalize( (-v[1], v[0]) )
    return dot(e, (p[0] - l1[0], p[1] - l1[1]) )

def dist2color(r):
    r_r = round(r)
    r1 = (r - r_r) * 255
    r1_r = round(r1)
    return (min(255, r_r), r1_r, 0)

size = 17.5
glow_radius = 35
scale = 2

w = h = int((size + glow_radius) * 2 * scale)

# y is up

p0 = (0, size)
p1 = (sin(pi * 0.75) * size, cos(pi * 0.75) * size)
p2 = (0, -0.5 * size)

### hull.png

im = Image.new("RGB", (w, h))
pix = im.load()

for j in range(0, h):
    for i in range(0, w):
        x = (0.5 + i - w / 2) / scale
        if x < 0: x = -x # ship is symmetrical
        y = (0.5 + h / 2 - j) / scale
        p = (x, y)

        d1 = dist_seq(p, p0, p1)
        d2 = dist_seq(p, p1, p2)

        if d1 >= 0:
            r = d1
            #  pix[i, j] = (0, 0, 255)
        elif y >= p0[1]:
            r = dist(p, p0)
            #  pix[i, j] = (0, 255, 0)
        elif d2 >= 0:
            r = d2
            #  pix[i, j] = (0, 255, 255)
        elif x >= p1[0] or y <= p1[1]:
            r = dist(p, p1)
            #  pix[i, j] = (255, 0, 0)
        else:
            d1 = dist_seq(p, p1, p0, False)
            d2 = dist_seq(p, p2, p1, False)
            if d1 < 0 or d2 < 0:
                raise Exception("something is wrong")

            r = min(d1, d2)

            #  if d1 < d2:
                #  pix[i, j] = (255, 0, 255)
            #  else:
                #  pix[i, j] = (255, 255, 0)

        #  if dist(p, p0) < 1 or dist(p, p1) < 1 or dist(p, p2) < 1:
            #  pix[i, j] = (255, 255, 255)

        pix[i, j] = dist2color(r)

im.show()
out_path = path.join(path.dirname(path.realpath(__file__)), '..', 'entity', 'ship', 'hull.png')
im.save(out_path, "PNG")

### part_front.png

part_size = dist(p0, p1)
w = int(glow_radius * 2 * scale)
h = int((glow_radius * 2 + part_size) * scale)

im = Image.new("RGB", (w, h))
pix = im.load()

p3 = (0, part_size / 2)

for j in range(0, h):
    for i in range(0, w):
        x = (0.5 + i - w / 2) / scale
        if x < 0: x = -x
        y = (0.5 + h / 2 - j) / scale
        if y < 0: y = -y
        p = (x, y)
        if y < p3[1]:
            r = x
        else:
            r = dist(p, p3)

        pix[i, j] = dist2color(r)

im.show()
out_path = path.join(path.dirname(path.realpath(__file__)), '..', 'entity', 'ship', 'part_front.png')
im.save(out_path, "PNG")

### part_back.png

part_size = dist(p1, p2)
w = int(glow_radius * 2 * scale)
h = int((glow_radius * 2 + part_size) * scale)

im = Image.new("RGB", (w, h))
pix = im.load()

p4 = (0, part_size / 2)

for j in range(0, h):
    for i in range(0, w):
        x = (0.5 + i - w / 2) / scale
        if x < 0: x = -x
        y = (0.5 + h / 2 - j) / scale
        if y < 0: y = -y
        p = (x, y)
        if y < p4[1]:
            r = x
        else:
            r = dist(p, p4)

        pix[i, j] = dist2color(r)

im.show()
out_path = path.join(path.dirname(path.realpath(__file__)), '..', 'entity', 'ship', 'part_back.png')
im.save(out_path, "PNG")
