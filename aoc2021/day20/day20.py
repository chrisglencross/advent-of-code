#!/usr/bin/python3
# Advent of code 2021 day 20
# See https://adventofcode.com/2021/day/20

from aoc2021.modules import grid as g

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

algo = lines[0]
grid = g.parse_grid("\n".join(lines[2:]))


def tick(grid, algo):
    new_grid = g.Grid({})
    # Plus and minus infinity...
    for y in range(-100, 201):
        for x in range(-100, 201):
            index = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    cell = grid.get((x+dx, y+dy))
                    index = 2 * index + (1 if cell == '#' else 0)
            new_value = algo[index]
            new_grid[(x, y)] = new_value
    return new_grid


for i in range(0, 50):
    grid = tick(grid, algo)

    # Hacky patch-up of the corner squares which go wrong when algo[0] is a '#'
    # Should solve this for the general case someday, but the previous two days have taken too much time
    if i % 2 == 1 and algo[0] == '#':
        for c in [(-100, -100), (-100, 200), (200, -100), (200, 200)]:
            grid[c] = '.'

    # print()
    # grid.print()
    print(len(grid.index_repeating_cells({"#"})['#']))
    print()

