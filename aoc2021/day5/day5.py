#!/usr/bin/python3
# Advent of code 2021 day 5
# See https://adventofcode.com/2021/day/5

import re


def load_grid(lines, diagonals):
    grid = {}
    for line in lines:
        match = re.search("^([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)$", line.strip())
        x0, y0, x1, y1 = [int(group) for group in match.groups()]
        dx = 1 if x1 > x0 else -1 if x1 < x0 else 0
        dy = 1 if y1 > y0 else -1 if y1 < y0 else 0
        if diagonals or dx == 0 or dy == 0:
            steps = max(max(x0, x1) - min(x0, x1), max(y0, y1) - min(y0, y1)) + 1
            for i in range(steps):
                x, y = x0 + i * dx, y0 + i * dy
                v = grid.setdefault((x, y), 0)
                grid[(x, y)] = v + 1
    return grid


with open("input.txt") as f:
    lines = f.readlines()

grid = load_grid(lines, False)
print(len([v for v in grid.values() if v > 1]))

grid = load_grid(lines, True)
print(len([v for v in grid.values() if v > 1]))
