#!/usr/bin/python3
# Advent of code 2023 day 24
# See https://adventofcode.com/2023/day/24
import itertools
import re

import aoc2023.modules as aoc
aoc.download_input("2023", "24")

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

hailstones = []
for line in lines:
    x, y, z, dx, dy, dz = [int(n)
                           for n in
                           re.match("^(.+), (.+), (.+) @ (.+), (.+), (.+)$", line).groups()]
    hailstones.append(((x, y, z), (dx, dy, dz)))

def get_c(coords, velocity):
    x, y = coords
    dx, dy = velocity
    return y - (dy/dx) * x

def intersect_line(l1, l2):
    (x1, y1, z1), (dx1, dy1, dz1) = l1
    (x2, y2, z2), (dx2, dy2, dz2) = l2
    if dy1/dx1 == dy2/dx2:
        return None, None
    c1 = get_c((x1, y1), (dx1, dy1))
    c2 = get_c((x2, y2), (dx2, dy2))
    x = (c2 - c1) / (dy1/dx1 - dy2/dx2)
    y = (dy1/dx1) * x + c1
    return x, y

def get_t(l1, x_intersect):
    (x1, y1, z1), (dx1, dy1, z1) = l1
    return (x_intersect - x1) / dx1


def intersect_in_range(l1, l2):
    x, y = intersect_line(l1, l2)
    if x is None or y is None:
        return False
    t1 = get_t(l1, x)
    t2 = get_t(l2, x)
    # return t1 >= 0 and t2 >= 0 and 7 <= x <= 27 and 7 <= y <= 27
    return t1 >= 0 and t2 >= 0 and 200000000000000 <= x <= 400000000000000 and 200000000000000 <= y <= 400000000000000

# Part 1
total = 0
for i, h1 in enumerate(hailstones):
    for h2 in hailstones[i+1:]:
        if intersect_in_range(h1, h2):
            total += 1
print(total)

# Part 2: Observe that for our test inputs there is a duplicate y=252498326441926, vy=25
# This means that to intersect both hailstones, rock must start at the same Y coordinate and have the same y velocity
xs = set()
ys = set()
zs = set()
for (x, y, z), (vx, vy, vz) in hailstones:
    if (x, vx) in xs:
        print(f"Dupe x={x}, vx={vx}")
    if (y, vy) in ys:
        print(f"Dupe y={y}, vy={vy}")
    if (z, vz) in zs:
        print(f"Dupe z={y}, vz={vz}")
    xs.add((x, vx))
    ys.add((y, vy))
    zs.add((z, vz))

Y = 252498326441926
VY = 25

# Print some simultaneous equations to solve by hand
for i, ((x, y, z), (vx, vy, vz)) in enumerate(hailstones[0:5]):
    t = chr(ord('a') + i)  # Unique t variable name for intersection time for each hailstone
    print(f"{x} + {vx}{t} = X + VX*{t}")
    print(f"{y} + {vy}{t} = {Y} + {VY}*{t}")
    print(f"{z} + {vz}{t} = Z + VZ*{t}")

print(f"Y={Y}")

# Solve simultaneous equations by hand
# 234316020446107 + 46a = Y + VY*a
# 234316020446107 + 46a = 252498326441926 + 25*a
a = (234316020446107 - 252498326441926) / (25 - 46)
print(f"a={a}")
# a=865824095039.0

# 153541424014705 + 128b = Y + VY*b
# 153541424014705 + 128b = 252498326441926 + 25*b
b = (153541424014705-252498326441926)/(25-128)
print(f"b={b}")
# b=960746625507.0

# 40684667846753 + 196b = X + VX*b
# 40684667846753 + 196 * 960746625507 = X + VX*960746625507
# 228991006446125 = X + VX*960746625507

# 37387660420460 + 235a = X + VX*a
# 37387660420460 + 235 * 865824095039 = X + VX*865824095039
# 240856322754625 = X + VX*865824095039

# 228991006446125 = X + VX*960746625507
# 240856322754625 = X + VX*865824095039

# 228991006446125 - 240856322754625 = VX(960746625507 - 865824095039)
VX = (228991006446125 - 240856322754625)/(960746625507 - 865824095039)
X = (37387660420460 + 235*a) - (VX*a)
print(f"X={X}")
# X = 349084334634500

# 382716912714218 = Z + VZ*960746625507
# 356897984426922 = Z + VZ*865824095039
VZ = (382716912714218-356897984426922) /(960746625507-865824095039)
Z = 382716912714218 - 960746625507 * VZ
print(f"Z={Z}")
# Z = 121393830576314

print(X + Y + Z)
