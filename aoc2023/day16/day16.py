#!/usr/bin/python3
# Advent of code 2023 day 16
# See https://adventofcode.com/2023/day/16

from aoc2023.modules import grid as g
from aoc2023.modules.directions import COMPASS_DIRECTIONS

grid = g.load_grid("input.txt")


def move_ray(coords, direction):
    cell = grid[coords]
    if cell == ".":
        new_directions = [direction]
    else:
        new_directions = {
            ("E", "/"): ["N"],
            ("E", "\\"): ["S"],
            ("E", "|", ): ["N", "S"],
            ("E", "-"): ["E"],
            ("S", "/"): ["W"],
            ("S", "\\"): ["E"],
            ("S", "|"): ["S"],
            ("S", "-"): ["E", "W"],
            ("W", "/"): ["S"],
            ("W", "\\"): ["N"],
            ("W", "|", ): ["S", "N"],
            ("W", "-"): ["W"],
            ("N", "/"): ["E"],
            ("N", "\\"): ["W"],
            ("N", "|"): ["N"],
            ("N", "-"): ["W", "E"]
        }[(direction, cell)]
    return {(c, d) for c, d in [(COMPASS_DIRECTIONS[nd].move(coords), nd) for nd in new_directions] if c in grid.keys()}


def count_energised_cells(ray):
    all_rays = {ray}
    new_rays = move_ray(*ray)
    while True:
        new_rays = new_rays.difference(all_rays)
        if not new_rays:
            break
        all_rays.update(new_rays)
        new_rays = {new_ray for r in new_rays for new_ray in move_ray(*r)}
    return len({c for c, _ in all_rays})


# Part 1
print(count_energised_cells(((0, 0), "E")))

# Part 2
starts = [((x, 0), "S") for x in range(0, grid.get_width())] + \
         [((x, grid.get_height()-1), "N") for x in range(0, grid.get_width())] + \
         [((0, y), "E") for y in range(0, grid.get_height())] + \
         [((grid.get_width()-1, y), "W") for y in range(0, grid.get_height())]
print(max(count_energised_cells(r) for r in starts))
