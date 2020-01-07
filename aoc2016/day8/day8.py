#!/usr/bin/python3
# Advent of code 2016 day 8
# See https://adventofcode.com/2016/day/8

import re

from aoc2016.modules import grid as g

data = {}
for x in range(0, 50):
    for y in range(0, 6):
        data[(x, y)] = "."
grid = g.Grid(data)

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

for line in lines:
    new_grid = g.Grid(dict(grid.grid))

    if match := re.fullmatch(r"rect (\d+)x(\d+)", line):
        for x in range(0, int(match.group(1))):
            for y in range(0, int(match.group(2))):
                new_grid[(x, y)] = "#"

    elif match := re.fullmatch(r"rotate row y=(\d+) by (\d+)", line):
        y = int(match.group(1))
        r = int(match.group(2))
        for x in range(0, 50):
            new_grid[(x, y)] = grid[((x - r) % 50, y)]

    elif match := re.fullmatch(r"rotate column x=(\d+) by (\d+)", line):
        x = int(match.group(1))
        r = int(match.group(2))
        for y in range(0, 6):
            new_grid[(x, y)] = grid[(x, (y - r) % 6)]

    grid = new_grid

print(len(grid.find_cells("#")))
grid.print()
