#!/usr/bin/python3
# Advent of code 2023 day 11
# See https://adventofcode.com/2023/day/11

from aoc2023.modules import grid as g

grid = g.load_grid("input.txt")
unexpanded = grid.index_repeating_cells("#")["#"]
xs = {x for x, y in unexpanded}
ys = {y for x, y in unexpanded}
empty_cols = [x for x in range(0, grid.get_width()) if x not in xs]
empty_rows = [y for y in range(0, grid.get_height()) if y not in ys]


def expand_coordinate(empties, c, factor):
    return c + (sum(1 for e in empties if e < c) * (factor - 1))


def expand_galaxies(galaxies, factor):
    return [(expand_coordinate(empty_cols, x, factor), expand_coordinate(empty_rows, y, factor)) for x, y in galaxies]


def total_distance(expanded):
    return sum(abs(g1[0] - g2[0]) + abs(g1[1] - g2[1]) for g1 in expanded for g2 in expanded) // 2


print(total_distance(expand_galaxies(unexpanded, 2)))
print(total_distance(expand_galaxies(unexpanded, 1000000)))