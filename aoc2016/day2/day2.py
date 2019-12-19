#!/usr/bin/python3
# Advent of code 2016 day 2
# See https://adventofcode.com/2016/day/2


moves = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


def parse_grid(grid_cells):
    grid = {}
    for y, line in enumerate([line for line in grid_cells.split("\n") if line.strip()]):
        print(y, line)
        for x, char in enumerate(line):
            grid[(x, y)] = char
    return grid


def get_pin(grid, location):
    result = []
    for line in lines:
        for c in line.strip():
            move = moves[c]
            new_location = (location[0] + move[0], location[1] + move[1])
            if new_location in grid.keys() and grid.get(new_location) != " ":
                location = new_location
        if grid.get(location):
            result.append(grid.get(location))
    return result


with open("input.txt") as f:
    lines = f.readlines()

# Part 1
grid = parse_grid("""
123
456
789
""")
result = get_pin(grid, (1, 1))
print("".join(result))

# Part 2
grid = parse_grid("""
  1
 234
56789
 ABC
  D
""")
result = get_pin(grid, (0, 2))
print("".join(result))
