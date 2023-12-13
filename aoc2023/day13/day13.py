#!/usr/bin/python3
# Advent of code 2023 day 13
# See https://adventofcode.com/2023/day/13

from aoc2023.modules import grid as g

with open("input.txt") as f:
    grids = [g.parse_grid(s.strip()) for s in f.read().split("\n\n")]


def get_total(grids, expected_mismatches):
    total = 0
    for i, grid in enumerate(grids):

        for xr in range(0, grid.get_width()-1):
            mismatches = 0
            for x in range(0, xr+1):
                for y in range(0, grid.get_height()):
                    r = grid.get((2*xr-x+1, y))
                    if r and not grid[(x, y)] == r:
                        mismatches += 1
            if mismatches == expected_mismatches:
                total += xr + 1

        for yr in range(0, grid.get_height()-1):
            mismatches = 0
            for y in range(0, yr+1):
                for x in range(0, grid.get_width()):
                    r = grid.get((x, 2*yr-y+1))
                    if r and not grid[(x, y)] == r:
                        mismatches += 1
            if mismatches == expected_mismatches:
                total += (yr + 1) * 100

    return total


print(get_total(grids, 0))
print(get_total(grids, 1))