#!/usr/bin/python3
# Advent of code 2023 day 14
# See https://adventofcode.com/2023/day/14

import re

from aoc2023.modules import grid as g
from aoc2023.modules import directions as d

grid = g.load_grid("input.txt")
rocks = tuple(grid.find_cells("O"))
squares = set(grid.find_cells("#"))


def move(rocks, direction):
    move_dir = d.COMPASS_DIRECTIONS[direction]
    sort_order = {
        "N": lambda rock: rock[1],
        "E": lambda rock: 0-rock[0],
        "S": lambda rock: 0-rock[1],
        "W": lambda rock: rock[0],
    }[direction]
    new_rocks = set()
    for rock in sorted(rocks, key=sort_order):
        r = move_dir.move(rock)
        while r in grid.keys() and r not in new_rocks and r not in squares:
            rock = r
            r = move_dir.move(r)
        new_rocks.add(rock)
    return new_rocks


# Part 1
rocks = move(rocks, "N")
print(sum(grid.get_height() - y for x, y in rocks))

# Part 2
def cycle(rocks):
    for dir in ["N", "W", "S", "E"]:
        rocks = move(rocks, dir)
    return rocks


states = {}
CYCLES = 1000000000
repeated = False
for i in range(0, CYCLES):
    key = tuple(rocks)
    if key in states:
        repeated = True
        repeat_start = states[key]
        repeat_end = i
        break
    states[key] = i
    rocks = cycle(rocks)

if repeated:
    repeat_length = repeat_end - repeat_start
    remaining_repeats = (CYCLES - i) // repeat_length
    for i in range(repeat_end + remaining_repeats * repeat_length, CYCLES):
        rocks = cycle(rocks)

print(sum(grid.get_height() - y for x, y in rocks))
