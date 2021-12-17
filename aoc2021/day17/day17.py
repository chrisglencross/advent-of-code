#!/usr/bin/python3
# Advent of code 2021 day 17
# See https://adventofcode.com/2021/day/17
import re

with open("input.txt") as f:
    bounds = [int(value) for value in re.match("^target area: x=([-0-9]+)..([-0-9]+), y=([-0-9]+)..([-0-9]+)$", f.readline().strip()).groups()]


def hit_target(fire_dx, fire_dy, bounds):
    x, y = 0, 0
    dx, dy = fire_dx, fire_dy
    max_height = y
    while x <= bounds[1] and y >= bounds[2]:
        if dx == 0 and x < bounds[0]:
            break  # Not enough x velocity to reach the target
        max_height = max(max_height, y)
        if bounds[0] <= x <= bounds[1] and bounds[2] <= y <= bounds[3]:
            return max_height
        x += dx
        y += dy
        dx = max(0, dx - 1)
        dy -= 1
    return None


max_height = 0
count = 0
for fire_dx in range(0, bounds[1]+1):
    for fire_dy in range(bounds[2], 1000):
        h = hit_target(fire_dx, fire_dy, bounds)
        if h is not None:
            max_height = max(max_height, h)
            count += 1
print(max_height)
print(count)