#!/usr/bin/python3
# Advent of code 2025 day 4
# See https://adventofcode.com/2025/day/4

from aoc2025.modules import grid as g
from aoc2025.modules import directions

import aoc2025.modules as aoc
aoc.download_input("2025", "4")

grid = g.load_grid("input.txt")

def count_neighbour_rolls(roll):
    return sum(1 for direction in directions.COMPASS_DIRECTIONS_8.values() if grid.get(direction.move(roll)) == '@')

def accessible_rolls():
    return [roll for roll in grid.find_cells("@") if count_neighbour_rolls(roll) < 4]

print(len(accessible_rolls()))

def remove_accessible_rolls():
    remove = accessible_rolls()
    for roll in remove:
        grid[roll] = '.'
    return remove

before = len(grid.find_cells("@"))
while remove_accessible_rolls():
    pass
after = len(grid.find_cells("@"))
print(before - after)
