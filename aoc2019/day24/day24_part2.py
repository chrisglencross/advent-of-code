#!/usr/bin/python3
# Advent of code 2019 day 24

from aoc2019.modules import directions
from aoc2019.modules import grid as g

TOP_ROW = set([(x, 0) for x in range(0, 5)])
BOTTOM_ROW = set([(x, 4) for x in range(0, 5)])
LEFT_COL = set([(0, y) for y in range(0, 5)])
RIGHT_COL = set([(4, y) for y in range(0, 5)])


def count_cells(grid, coords):
    return sum([1 for c in coords if grid[c] == "#"])


def add_cell(grid, coords):
    if grid[coords] == "#":
        return 1
    else:
        return 0


def count_neighbours(grids, x, y, depth):
    neighbours = 0

    if (x, y) != (2, 2):
        # Direct neighbours
        for direction in directions.COMPASS_DIRECTIONS.values():
            neighbour = grids[depth].get(direction.move((x, y)), ".")
            if neighbour == "#":
                neighbours += 1

    # Neighbours down a level
    if (x, y) == (2, 1) and depth > 0:
        neighbours += count_cells(grids[depth - 1], TOP_ROW)
    elif (x, y) == (1, 2) and depth > 0:
        neighbours += count_cells(grids[depth - 1], LEFT_COL)
    elif (x, y) == (3, 2) and depth > 0:
        neighbours += count_cells(grids[depth - 1], RIGHT_COL)
    elif (x, y) == (2, 3) and depth > 0:
        neighbours += count_cells(grids[depth - 1], BOTTOM_ROW)

    # Neighbours up a level
    if x == 0 and depth < grid_levels - 1:
        neighbours += add_cell(grids[depth + 1], (1, 2))
    elif x == 4 and depth < grid_levels - 1:
        neighbours += add_cell(grids[depth + 1], (3, 2))

    if y == 0 and depth < grid_levels - 1:
        neighbours += add_cell(grids[depth + 1], (2, 1))
    elif y == 4 and depth < grid_levels - 1:
        neighbours += add_cell(grids[depth + 1], (2, 3))

    return neighbours


def tick(grids):
    new_grids = [g.Grid(dict()) for i in range(0, len(grids))]
    for depth, grid in enumerate(grids):
        for y in range(0, 5):
            for x in range(0, 5):
                neighbours = count_neighbours(grids, x, y, depth)
                if grid[(x, y)] == "#":
                    new_grids[depth][(x, y)] = "#" if neighbours == 1 else "."
                else:
                    new_grids[depth][(x, y)] = "#" if 1 <= neighbours <= 2 else "."
    return new_grids


def count_all_grid_cells(grids):
    total = 0
    for grid in grids:
        total += sum([1 for cell in grid.values() if cell == "#"])
    return total


iterations = 200
grid_levels = iterations + 3  # 2 more than actually required
min_grid_level = 0 - grid_levels // 2

grids = [g.Grid({}) for i in range(0, grid_levels)]
grids[grid_levels // 2] = g.load_grid("input.txt")

for i in range(0, iterations):
    print(f"Iteration {i}")
    grids = tick(grids)

for i in range(0, grid_levels):
    print(f"Depth {i + min_grid_level}:")
    grids[i].print()

print(count_all_grid_cells(grids))
