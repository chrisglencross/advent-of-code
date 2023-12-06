#!/usr/bin/python3
# Advent of code 2023 day 2
# See https://adventofcode.com/2023/day/2
from functools import reduce
from operator import mul
import re

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

total = 0
power = 0

for line in lines:

    game, reveals = re.match("^Game ([0-9]+): (.*)$", line).groups()
    draws = [{d.split(" ")[1]: int(d.split(" ")[0]) for d in cubes.split(", ")} for cubes in reveals.split("; ")]
    rgbs = [[draw.get(color, 0) for color in ["red", "green", "blue"]] for draw in draws]

    if all(component <= limit for rgb in rgbs for component, limit in zip(rgb, (12, 13, 14))):
        total += int(game)

    min_rgb = reduce(lambda rgb1, rgb2: [max(p) for p in zip(rgb1, rgb2)], rgbs)
    power += reduce(mul, min_rgb)

print(total)
print(power)
