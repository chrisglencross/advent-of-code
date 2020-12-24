#!/usr/bin/python3
# Advent of code 2020 day 24
# See https://adventofcode.com/2020/day/24

WHITE = 0
BLACK = 1

DIRECTIONS = {
    "ne": (1, -1),
    "e": (2, 0),
    "se": (1, 1),
    "sw": (-1, 1),
    "w": (-2, 0),
    "nw": (-1, -1)
}


def get_coords(line: str):
    chars = [c for c in line.strip()]
    x, y = 0, 0
    while chars:
        d = chars.pop(0)
        if d in ['s', 'n']:
            d += chars.pop(0)
        dx, dy = DIRECTIONS.get(d)
        x, y = x + dx, y + dy
    return x, y


def get_all_neighbours(x, y):
    result = []
    for dx, dy in DIRECTIONS.values():
        result.append((x + dx, y + dy))
    return result


def count_neighbours(grid, x, y):
    return sum([grid.get((nx, ny), 0) for nx, ny in get_all_neighbours(x, y)])


with open("input.txt") as f:
    lines = f.readlines()

grid = {}
for line in lines:
    x, y = get_coords(line)
    grid[(x, y)] = 1 - grid.get((x, y), WHITE)
print("Part 1", sum(grid.values()))

for i in range(0, 100):
    evaluate = set()
    for x, y in grid.keys():
        evaluate.add((x, y))
        evaluate.update(get_all_neighbours(x, y))
    new_grid = {}
    for x, y in evaluate:
        tile = grid.get((x, y), 0)
        black_neighbours = count_neighbours(grid, x, y)
        if tile == BLACK and (black_neighbours == 0 or black_neighbours > 2):
            pass  # default is white
        elif tile == WHITE and black_neighbours == 2:
            new_grid[(x, y)] = BLACK
        elif tile == BLACK:
            new_grid[(x, y)] = BLACK
        else:
            pass  # default is white
    grid = new_grid

print("Part 2", sum(grid.values()))
