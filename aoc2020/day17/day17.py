#!/usr/bin/python3
# Advent of code 2020 day 17
# See https://adventofcode.com/2020/day/17
from typing import Tuple

Coords = Tuple[int, int, int, int]


class Grid:
    def __init__(self, grid):
        self.grid = grid

    def get_bounds(self) -> Tuple[Coords, Coords]:
        if not self.grid:
            return (0, 0, 0, 0), (0, 0, 0, 0)
        xs = set([c[0] for c in self.grid.keys()])
        ys = set([c[1] for c in self.grid.keys()])
        zs = set([c[2] for c in self.grid.keys()])
        ws = set([c[3] for c in self.grid.keys()])
        return (min(xs), min(ys), min(zs), min(ws)), (max(xs)+1, max(ys)+1, max(zs)+1, max(ws)+1)

    def get_cell(self, cell: Coords):
        return self.grid.get(cell, ".")

    def count_neighbours_3d(self, cell: Coords, w=0):
        neighbours = 0
        for z in range(-1, 2):
            for y in range(-1, 2):
                for x in range(-1, 2):
                    if x == 0 and y == 0 and z == 0 and w == 0:
                        pass
                    elif self.get_cell((cell[0] + x, cell[1] + y, cell[2] + z, cell[3] + w)) == "#":
                            neighbours += 1
        return neighbours

    def count_neighbours_4d(self, cell: Coords):
        neighbours = 0
        for w in range(-1, 2):
            neighbours += self.count_neighbours_3d(cell, w)
        return neighbours


def load_grid():
    with open("input.txt") as f:
        lines = f.readlines()
    cells = {}
    for y, row in enumerate(lines):
        for x, cell in enumerate(row.strip()):
            cells[(x, y, 0, 0)] = cell
    return Grid(cells)


def play_game(count_neighbours_function):
    grid = load_grid()

    for i in range(0, 6):
        (min_x, min_y, min_z, min_w), (max_x, max_y, max_z, max_w) = grid.get_bounds()
        new_cells = {}
        for w in range(min_w - 1, max_w + 1):
            for z in range(min_z - 1, max_z + 1):
                for y in range(min_y - 1, max_y + 1):
                    for x in range(min_x - 1, max_x + 1):
                        coords = (x, y, z, w)
                        cell = grid.get_cell(coords)
                        neighbours = count_neighbours_function(grid, coords)
                        if cell == "#":
                            if 2 <= neighbours <= 3:
                                new_cells[coords] = "#"
                        else:
                            if neighbours == 3:
                                new_cells[coords] = "#"
        grid = Grid(new_cells)

    return len([cell for cell in grid.grid.values() if cell == "#"])


print(play_game(lambda g, c: g.count_neighbours_3d(c)))
print(play_game(lambda g, c: g.count_neighbours_4d(c)))

