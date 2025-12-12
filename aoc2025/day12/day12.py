#!/usr/bin/python3
# Advent of code 2025 day 12
# See https://adventofcode.com/2025/day/12

from functools import lru_cache

import aoc2025.modules as aoc
aoc.download_input("2025", "12")

with open("input.txt") as f:
    blocks = f.read().replace("\r", "").split("\n\n")

shapes = [block.split('\n')[1:] for block in blocks[0:-1]]
lines = [l for line in blocks[-1].split("\n") if (l := line.strip())]

@lru_cache
def get_shape(shape_no: int, flip_x: bool, rotate: int):
    shape = shapes[shape_no]
    output = [list(row) for row in shape]
    for y in range(3):
        for x in range(3):
            if flip_x:
                for i in range(0, 3):
                    output[i][0], output[i][2] = output[i][2], output[i][0]
            for r in range(rotate):
                for j in range(0, 2):
                    temp = output[0][j]
                    output[0][j] = output[2-j][0]
                    output[2-j][0] = output[2][2-j]
                    output[2][2-j] = output[j][2]
                    output[j][2] = temp
    return tuple(tuple(line) for line in output)

@lru_cache
def get_coords_in_shape(shape):
    result = set()
    for y, row in enumerate(shape):
        for x, c in enumerate(row):
            if shape[y][x] == '#':
                result.add((x, y))
    return tuple(sorted(result))

@lru_cache
def get_coords_adjacent_to_shape(shape):
    result = set()
    for x, y in get_coords_in_shape(shape):
        for dx, dy in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            if not 0 <= x+dx < 3 or not 0 <= y+dy < 3 or shape[y+dy][x+dx] == '.':
                result.add((x+dx, y+dy))
    return tuple(sorted(result))

def print_grid(grid):
    for line in grid:
        print("".join(line))
    print()

def is_empty(grid, x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] != '#'

def can_place_shape(shape, x, y, grid):
    for dy, row in enumerate(shape):
        for dx, c in enumerate(row):
            if c == '#' and not is_empty(grid, x+dx, y+dy):
                return False
    return True

def set_shape(shape, x, y, grid, symbol):
    for dy, row in enumerate(shape):
        for dx, c in enumerate(row):
            if c == '#':
                grid[y+dy][x+dx] = symbol

def add_shape(shape, x, y, grid):
    set_shape(shape, x, y, grid, "#")

def remove_shape(shape, x, y, grid):
    set_shape(shape, x, y, grid, ".")

def get_new_try_coords(shape, x, y, grid, try_coords):
    add = set()
    remove = set()
    for dx, dy in get_coords_adjacent_to_shape(shape):
        if is_empty(grid, x+dx, y+dy):
            add.add((x+dx, y+dy))
    for dx, dy in get_coords_in_shape(shape):
        remove.add((x+dx, y+dy))
    return (try_coords - remove) | add

def print_grid_with_try_coords(grid, try_coords):
    print_grid([['?' if (x, y) in try_coords else c for x, c in enumerate(row)] for y, row in enumerate(grid)])
    pass

def place_shape(shape, x, y, grid, shape_counts, try_coords):
    add_shape(shape, x, y, grid)
    new_try_coords = get_new_try_coords(shape, x, y, grid, try_coords)
    # print_grid_with_try_coords(grid, new_try_coords)
    result = try_place_any_shape(grid, shape_counts, new_try_coords)
    remove_shape(shape, x, y, grid)
    return result

def get_placeable_shapes_at_coords(x, y, grid, shape_counts):
    result = []
    for shape_no in range(len(shapes)):
        if shape_counts[shape_no] == 0:
            continue
        attempted_shapes = set()  # In case shape is symmetrical
        for flip_x in [False, True]:
            for rotate in range(0, 4):
                shape = get_shape(shape_no, flip_x, rotate)
                if shape in attempted_shapes:
                    continue
                attempted_shapes.add(shape)
                if can_place_shape(shape, x, y, grid):
                    result.append((shape_no, shape, x, y))
    return result

def not_possible_heuristic(grid, shape_counts, try_coords):
    max_y = max(y for x, y in try_coords)
    height = len(grid)
    width = len(grid[0])
    height_remaining = (height - max_y) + 1
    area_remaining = width * height_remaining
    shapes_remaining = sum(shape_counts)
    guessed_area_required = shapes_remaining * 7  # Guess that we need at least 7 cells per remaining shape in untouched rows
    return guessed_area_required > area_remaining

def try_place_any_shape(grid, shape_counts, try_coords):
    if all(n == 0 for n in shape_counts):
        return True

    if not try_coords:
        return False

    # Heuristic encourages packing from the top and giving up early if not enough free space
    if not_possible_heuristic(grid, shape_counts, try_coords):
        return False

    new_try_coords = set(try_coords)
    possible_placements = []
    for x, y in try_coords:
        possible_placements_at_coord = get_placeable_shapes_at_coords(x, y, grid, shape_counts)
        if not possible_placements_at_coord:
            new_try_coords.remove((x, y)) # Can't place any shapes at this coord (hole too small); no point trying again
        else:
            possible_placements.extend(possible_placements_at_coord)

    # Try to pack from the top first
    for shape_no, shape, x, y in sorted(possible_placements, key=lambda p: p[3]):
        shape_counts[shape_no] -= 1
        success = place_shape(shape, x, y, grid, shape_counts, new_try_coords)
        shape_counts[shape_no] += 1
        if success:
            return True
    return False


def is_solvable(dimensions, shape_counts):
    grid = [["." for _ in range(dimensions[0])] for _ in range(dimensions[1])]
    try_coords = {(0, 0)}
    return try_place_any_shape(grid, shape_counts, try_coords)

def part1():
    result = 0
    for i, line in enumerate(lines):
        p1, p2 = line.split(": ")
        x, y = tuple(int(d) for d in p1.split("x"))
        if x > y:
            x, y = y, x
        shape_counts = [int(c) for c in p2.split(" ")]
        solvable = is_solvable((x, y), shape_counts)
        print(i, line, solvable)
        if solvable:
            result += 1
    return result

print(part1())