#!/usr/bin/python3
# Advent of code 2019 day 10

import math

import numpy

with open("input.txt") as f:
    grid = f.readlines()

coords = set()
for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell == "#":
            coords.add((x, y))

# Part 1
counts = {}
for xb, yb in coords:
    count = 0
    for xt, yt in coords:
        dx = xt - xb
        dy = yt - yb
        if dx == 0 and dy == 0:
            continue
        gcd = numpy.gcd(dx, dy)
        dx_step = dx // gcd
        dy_step = dy // gcd
        visible = True
        for i in range(1, gcd):
            blocker = (i * dx_step + xb, i * dy_step + yb)
            if blocker in coords:
                # print(f"{blocker} blocks {xt, yt} from view by {xb, yb}")
                visible = False
                break
        if visible:
            count = count + 1
    counts[(xb, yb)] = count

base_x, base_y = max(counts.keys(), key=lambda coord: counts[coord])
print(counts[(base_x, base_y)])


# Part 2
# Convention is -90 degrees is up & angle becomes more positive clockwise: zero=right; wraps 270 to -90
def angle_from_base(x, y):
    if (x - base_x) == 0:
        if y > base_y:
            result = 90.0
        else:
            result = -90.0
    else:
        result = math.degrees(math.atan((y - base_y) / (x - base_x)))
    if x < base_x:
        result = result - 180
    return result


# Remove the base
coords.remove((base_x, base_y))

asteroid_angles = {}
for x, y in coords:
    asteroid_angles[(x, y)] = angle_from_base(x, y)

# Find the first angle
next_angle = min([angle for angle in asteroid_angles.values() if angle >= -90.0])

count = 0
while True:

    # Find the closest asteroid at angle next_angle
    matching_angle = [coords for coords, angle in asteroid_angles.items() if angle == next_angle]
    matching_angle.sort(key=lambda c: abs(c[0] - base_x) + abs(c[1] - base_y))
    next_hit = matching_angle[0]
    count = count + 1
    # print(f"Hit number {count} of {next_hit} at angle {next_angle} degrees")
    if count == 200:
        print(f"Result is {100 * next_hit[0] + next_hit[1]}")
        break

    # Remove destroyed asteroid and rotate to the next angle
    del asteroid_angles[next_hit]
    remaining_in_sweep = [angle for angle in asteroid_angles.values() if angle > next_angle]
    if not remaining_in_sweep:
        print("Wrapping around")
        remaining_in_sweep = [angle for angle in asteroid_angles.values()]
    next_angle = min(remaining_in_sweep)
