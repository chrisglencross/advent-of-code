#!/usr/bin/python3
# Advent of code 2015 day 18
# See https://adventofcode.com/2015/day/18

import aoc2015.modules.grid as g
from aoc2015.modules import directions


def run(corners_stuck_on=False):
    grid = g.load_grid("input.txt")
    (min_x, min_y), (max_x, max_y) = grid.get_bounds()

    for tick in range(0, 100):
        next_grid = {}
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                neighbours = len([direction for direction in directions.COMPASS_DIRECTIONS_8.values() if
                                  grid[direction.move((x, y))] == "#"])
                if grid[(x, y)] == "#" and 2 <= neighbours <= 3:
                    next_grid[(x, y)] = "#"
                elif grid[(x, y)] != "#" and neighbours == 3:
                    next_grid[(x, y)] = "#"
                else:
                    next_grid[(x, y)] = "."

        if corners_stuck_on:
            for y in (min_y, max_y):
                for x in (min_x, max_x):
                    next_grid[(x, y)] = "#"

        grid = g.Grid(next_grid)

    return len(grid.find_cells("#"))


print("Part 1:", run(corners_stuck_on=False))
print("Part 2:", run(corners_stuck_on=True))
