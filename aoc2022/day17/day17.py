#!/usr/bin/python3
# Advent of code 2022 day 17
# See https://adventofcode.com/2022/day/17
import itertools
import aoc2022.modules.grid as g

with open("input.txt") as f:
    jets = f.readline().strip()

# Shapes with origins at the bottom left corner
shapes = [
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((1, 0), (0, -1), (1, -1), (2, -1), (1, -2)),
    ((0, 0), (1, 0), (2, 0), (2, -1), (2, -2)),
    ((0, 0), (0, -1), (0, -2), (0, -3)),
    ((0, 0), (1, 0), (0, -1), (1, -1))
]

grid = g.Grid({})

# Add bottom of grid at y=-1
grid[-1, 1] = '+'
for x in range(0, 7):
    grid[x, 1] = '-'
grid[7, 1] = '+'

height = grid.get_height() - 1
shape_index = 0
shape_x = 2
shape_y = 0 - height - 3


def print_grid():
    grid_copy = g.Grid(dict(grid.grid))
    for x, y in shape:
        grid_copy[(x + shape_x, y + shape_y)] = '@'
    grid_copy.print()


def is_collision(grid, shape, shape_x, shape_y):
    return any(grid.get((x + shape_x, y + shape_y), '.') != '.' for x, y in shape) or \
        any((x + shape_x == 7 or x + shape_x == -1) for x, y in shape)

for tick in itertools.count():
    shape = shapes[shape_index % len(shapes)]

    # Move sideways
    jet = jets[tick % len(jets)]
    if jet == '>' and not is_collision(grid, shape, shape_x + 1, shape_y):
            shape_x += 1
    if jet == '<' and not is_collision(grid, shape, shape_x - 1, shape_y):
            shape_x -= 1

    if is_collision(grid, shape, shape_x, shape_y + 1):
        # Can't move down: come to rest and move to next shape
        for x, y in shape:
            grid[(x + shape_x, y + shape_y)] = '#'
        height = grid.get_height() - 1
        shape_index += 1
        if shape_index == 2022:
            print(f"Part 1 result: {height}")
        if shape_index == 1405:
            print(f"Part 2 additional shapes height: {height}")
        if shape_index % len(shapes) == 0 and tick % len(jets) == 24:
            print(f"Part 2 cycle: shapes={shape_index} height={height}")
        shape_x = 2
        shape_y = 0 - height - 3
    else:
        # Move down
        shape_y += 1
