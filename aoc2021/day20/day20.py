#!/usr/bin/python3
# Advent of code 2021 day 20
# See https://adventofcode.com/2021/day/20

from aoc2021.modules import grid as g

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

algo = lines[0]
grid = g.parse_grid("\n".join(lines[2:]))


def tick(grid, background, algo):
    new_grid = g.Grid({})
    (min_x, min_y), (max_x, max_y) = grid.get_bounds()
    for y in range(min_y-1, max_y+1):
        for x in range(min_x-1, max_x+1):
            index = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    cell = grid.get((x+dx, y+dy), background)
                    index = 2 * index + (1 if cell == '#' else 0)
            new_value = algo[index]
            new_grid[(x, y)] = new_value
    background = algo[0] if background == '.' else algo[511]
    return new_grid, background


# background is content of cells in the infinite space beyond grid
background = '.'
for i in range(0, 50):
    grid, background = tick(grid, background, algo)
    # grid.print()

print(len(grid.index_repeating_cells({"#"})['#']))
