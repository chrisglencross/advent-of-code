#!/usr/bin/python3
# Advent of code 2021 day 25
# See https://adventofcode.com/2021/day/25
import itertools

from aoc2021.modules import grid as g
from aoc2021.modules.directions import COMPASS_DIRECTIONS, Direction


def move(to_move, others, direction, bounds):
    moveable = []
    for location in to_move:
        target = direction.move(location)
        target = target[0] % bounds[0], target[1] % bounds[1]
        if target not in to_move and target not in others:
            moveable.append((location, target))
    for location, target in moveable:
        to_move.remove(location)
        to_move.add(target)
    return len(moveable)


grid = g.load_grid("input.txt")
rs = set(grid.find_cells('>'))
ds = set(grid.find_cells('v'))
size = grid.get_size()
for i in itertools.count(1):
    if move(rs, ds, COMPASS_DIRECTIONS['E'], size) + move(ds, rs, COMPASS_DIRECTIONS['S'], size) == 0:
        print(i)
        break



