#!/usr/bin/python3
# Advent of code 2022 day 8
# See https://adventofcode.com/2022/day/8

import math
import aoc2022.modules.grid as g
grid = g.load_grid("input.txt")


def get_viewing_distance(grid, coords, dir):
    h = grid.get(coords)
    d = 0
    while True:
        coords = dir.move(coords)
        h2 = grid.get(coords)
        if h2 is None:
            return d
        if h2 >= h:
            return d + 1
        d += 1


def get_score(grid, coords):
    return math.prod(get_viewing_distance(grid, coords, dir)
                     for dir in g.COMPASS_DIRECTIONS.values())


print(max(get_score(grid, coords) for coords in grid.keys()))
