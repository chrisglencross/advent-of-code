#!/usr/bin/python3
# Advent of code 2019 day 24

from aoc2019.modules import directions
from aoc2019.modules import grid as g


def tick(grid):
    new_grid = {}
    for y in range(0, 5):
        for x in range(0, 5):
            neighbours = 0
            for direction in directions.COMPASS_DIRECTIONS.values():
                neighbour = grid.get(direction.move((x, y)), ".")
                if neighbour == "#":
                    neighbours += 1
            if grid[(x, y)] == "#":
                new_grid[(x, y)] = "#" if neighbours == 1 else "."
            else:
                new_grid[(x, y)] = "#" if 1 <= neighbours <= 2 else "."
    return g.Grid(new_grid)


def get_biodiversity(grid):
    bit = 1
    result = 0
    for y in range(0, 5):
        for x in range(0, 5):
            if grid.get((x, y), ".") == "#":
                result = result | bit
            bit *= 2
    return result


grid = g.load_grid("input.txt")
grid.print()

biodiveristies = set()
while True:
    b = get_biodiversity(grid)
    if b in biodiveristies:
        print(b)
        break
    biodiveristies.add(b)
    grid = tick(grid)
