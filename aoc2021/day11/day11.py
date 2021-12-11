#!/usr/bin/python3
# Advent of code 2021 day 11
# See https://adventofcode.com/2021/day/11
import itertools

from aoc2019.modules.imagegridprinter import ImageGridPrinter
from aoc2021.modules import directions
from aoc2021.modules import grid as g


def print_grid(grid):
    for row in grid:
        print("".join([str(cell) for cell in row]))


def increment(symbol):
    if symbol in '9+':
        return '+'  # Pending explosion
    elif symbol == '*':
        return '*'  # Exploded
    else:
        return str(int(symbol) + 1)


def do_step(grid):
    # Phase 1: Increment
    for coords, value in grid.items():
        grid[coords] = increment(value)

    # Phase 2: Cascade explosions
    while '+' in grid.values():
        for coords, value in grid.items():
            if value == '+':
                grid[coords] = '*'
                for direction in directions.COMPASS_DIRECTIONS_8.values():
                    neighbour = direction.move(coords)
                    if neighbour in grid.keys():
                        grid[neighbour] = increment(grid[neighbour])

    # Phase 3: Reset
    explosions = 0
    for coords, value in grid.items():
        if value == '*':
            grid[coords] = '0'
            explosions += 1

    return explosions


# Part 1
grid = g.load_grid("input.txt")
total_explosions = 0
for i in range(100):
    total_explosions += do_step(grid)
print(total_explosions)

# Part 2
grid_printer = ImageGridPrinter(filename="image.gif", max_height=200, max_width=200, duration=200, colour_map={
    "1": (0, 0, 0),
    "2": (0, 0, 255),
    "3": (0, 128, 255),
    "4": (0, 255, 255),
    "5": (0, 255, 128),
    "6": (0, 255, 0),
    "7": (128, 255, 0),
    "8": (255, 255, 0),
    "9": (255, 128, 0),
    "0": (255, 0, 0)
})

grid = g.load_grid("input.txt")
grid_printer.print(grid)
for i in itertools.count(1):
    explosions = do_step(grid)
    grid_printer.print(grid)
    if explosions == len(grid.grid):
        for j in range(5):
            grid_printer.print(grid)
        print(i)
        break
grid_printer.close()
