#!/usr/bin/python3
# Advent of code 2025 day 7
# See https://adventofcode.com/2025/day/7
from functools import lru_cache

from aoc2025.modules import grid as g

import aoc2025.modules as aoc
aoc.download_input("2025", "7")

grid = g.load_grid("input.txt")
start_x, start_y = grid.find_cell('S')

@lru_cache
def splitters(x, y) -> set[tuple[int, int]]:
    match grid.get((x, y+1)):
        case '^':
            return {(x, y + 1)} | splitters(x - 1, y + 1) | splitters(x + 1, y + 1)
        case '.':
            return splitters(x, y + 1)
        case _:
            return set()

print(len(splitters(start_x, start_y)))

@lru_cache
def timelines(x, y) -> int:
    match grid.get((x, y+1)):
        case '^':
            return timelines(x-1, y+1) + timelines(x+1, y+1)
        case '.':
            return timelines(x, y+1)
        case _:
            return 1

print(timelines(start_x, start_y))