#!/usr/bin/python3
# Advent of code 2022 day 8
# See https://adventofcode.com/2022/day/8

import aoc2022.modules.grid as g

grid = g.load_grid("input.txt")


def is_visible_from(grid, coords, dir, h):
    neighbour = dir.move(coords)
    h2 = grid.get(neighbour)
    return h2 is None or (h2 < h and is_visible_from(grid, neighbour, dir, h))


print(len(set(coords
              for coords in grid.keys()
              for dir in g.COMPASS_DIRECTIONS.values()
              if is_visible_from(grid, coords, dir, grid.get(coords)))))
