#!/usr/bin/python3
# Advent of code 2022 day 22
# See https://adventofcode.com/2022/day/22

import aoc2022.modules.grid as g
from aoc2022.modules.directions import COMPASS_DIRECTIONS

with open("input.txt") as f:
    board, path = f.read().split("\n\n")


def move_with_wrap(grid, coords, dir, hyperspace):
    while True:
        coords = dir.move(coords)
        if (coords, dir.name) in hyperspace:
            # Part 2: Jump to another surface of the cube
            coords, dir_name = hyperspace[(coords, dir.name)]
            return coords, COMPASS_DIRECTIONS[dir_name]
        # Part 1: Just wrap
        coords = coords[0] % grid.get_width(), coords[1] % grid.get_height()
        if grid.get(coords, ' ') != ' ':
            return coords, dir


def plot_route(grid, coords, dir, path, hyperspace):
    for i, step in enumerate(path):
        if i % 100 == 0:
            print(f"Progress: {i * 100 // len(path)}%")
        grid[coords] = dir.name
        if step == 'L':
            dir = dir.turn_left()
        elif step == 'R':
            dir = dir.turn_right()
        else:
            forward = int(step)
            for i in range(0, forward):
                grid[coords] = dir.name
                next_coords, next_dir = move_with_wrap(grid, coords, dir, hyperspace)
                if grid.get(next_coords) == '#':
                    break  # hit a wall
                coords = next_coords
                dir = next_dir
    return coords, dir


path = [step for step in path.replace("R", "\nR\n").replace("L", "\nL\n").split("\n") if step]
dir_score = {"E": 0, "S": 1, "W": 2, "N": 3}

# Part 1
grid = g.parse_grid(board)
coords, dir = plot_route(grid, grid.find_cell("."), COMPASS_DIRECTIONS["E"], path, {})
print(1000*(coords[1]+1) + 4 * (coords[0]+1) + dir_score[dir.name])


# Part 2
def hyperspace_real():
    hyperspace = {}
    # A1
    for x in range(0, 50):
        hyperspace[((x, 99), "N")] = (50, 50+x), "E"
    # A2
    for y in range(50, 100):
        hyperspace[((49, y), "W")] = (y-50, 100), "S"
    # B1
    for x in range(100, 150):
        hyperspace[((x, 50), "S")] = (99, x-50), "W"
    # B2
    for y in range(50, 100):
        hyperspace[((100, y), "E")] = (y+50, 49), "N"
    # C1
    for x in range(50, 100):
        hyperspace[((x, 150), "S")] = (49, x+100), "W"
    # C2
    for y in range(150, 200):
        hyperspace[((50, y), "E")] = (y-100, 149), "N"
    # D1
    for y in range(100, 150):
        hyperspace[((100, y), "E")] = (149, 149-y), "W"
    # D2
    for y in range(0, 50):
        hyperspace[((150, y), "E")] = (99, 149-y), "W"
    # E1
    for y in range(0, 50):
        hyperspace[((49, y), "W")] = (0, 149-y), "E"
    # E2
    for y in range(100, 150):
        hyperspace[((-1, y), "W")] = (50, 149-y), "E"
    # F1
    for x in range(50, 100):
        hyperspace[((x, -1), "N")] = (0, 100+x), "E"
    # F2
    for y in range(150, 200):
        hyperspace[((-1, y), "W")] = (y-100, 0), "S"
    # G1
    for x in range(100, 150):
        hyperspace[((x, -1), "N")] = (x-100, 199), "N"
    # G2
    for x in range(0, 50):
        hyperspace[((x, 200), "S")] = (x+100, 0), "S"
    return hyperspace


def hyperspace_test():
    hyperspace = {}
    # A1
    for x in range(4, 8):
        hyperspace[((x, 3), "N")] = (8, x-4), "E"
    # A2
    for y in range(0, 4):
        hyperspace[((7, y), "W")] = (y+4, 4), "S"
    # B1
    for x in range(0, 4):
        hyperspace[(x, 3), "N"] = (11-x, 0), "S"
    # B2
    for x in range(8, 12):
        hyperspace[(x, -1), "N"] = (11-x, 4), "S"
    # C1
    for y in range(0, 4):
        hyperspace[(12, y), "E"] = (15, 11-y), "W"
    # C2
    for y in range(8, 12):
        hyperspace[(16, y), "E"] = (11, 11-y), "W"
    # D1
    for y in range(4, 8):
        hyperspace[(12, y), "E"] = (15-(y-4), 8), "S"
    # D2
    for x in range(12, 16):
        hyperspace[(x, 7), "N"] = (11, 7-(x-12)), "W"
    # E1
    for x in range(4, 8):
        hyperspace[(x, 8), "S"] = (8, (8-x)+7), "E"
    # E2
    for y in range(8, 12):
        hyperspace[(7, y), "W"] = (12-y+3, 7), "N"
    # F1
    for x in range(0, 4):
        hyperspace[(x, 8), "S"] = (7+(4-x), 11), "N"
    # F2
    for x in range(8, 12):
        hyperspace[(x, 12), "S"] = (0+(11-x), 7), "N"
    # G1
    for y in range(4, 8):
        hyperspace[(-1, y), "W"] = (11+4-(y-4), 11), "N"
    # G2
    for x in range(12, 16):
        hyperspace[(x, 12), "S"] = (0, 3+4-(x-12)), "E"
    return hyperspace


grid = g.parse_grid(board)
if grid.get_width() == 150:
    hyperspace = hyperspace_real()
elif grid.get_width() == 16:
    hyperspace = hyperspace_test()
else:
    raise Exception("Unknown cube layout")

coords, dir = plot_route(grid, grid.find_cell("."), COMPASS_DIRECTIONS["E"], path, hyperspace)
print(1000*(coords[1]+1) + 4 * (coords[0]+1) + dir_score[dir.name])