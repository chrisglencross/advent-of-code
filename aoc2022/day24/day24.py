#!/usr/bin/python3
# Advent of code 2022 day 24
# See https://adventofcode.com/2022/day/24
import math
import networkx as nx

import aoc2022.modules.grid as g
import aoc2022.modules.directions as d

grid = g.load_grid("input.txt")
grid_width = grid.get_width()
grid_height = grid.get_height()

entry_coords = (1, 0)
exit_coords = (grid_width - 2, grid_height - 1)

interval = math.lcm(grid.get_width()-2, grid.get_height()-2)

directions = {
    '^': d.UDLR_DIRECTIONS["U"],
    'v': d.UDLR_DIRECTIONS["D"],
    '<': d.UDLR_DIRECTIONS["L"],
    '>': d.UDLR_DIRECTIONS["R"],
}


def move_blizzard(symbol, location):
    direction = directions[symbol]
    x, y = direction.move(location)
    if x == 0:
        x = grid_width - 2
    elif x == grid_width - 1:
        x = 1
    if y == 0:
        y = grid_height - 2
    elif y == grid_height - 1:
        y = 1
    return x, y


blizzards = grid.index_repeating_cells(symbols="^v<>")

blank_grid = g.Grid(dict(grid.grid))
for location in [location for locations in blizzards.values() for location in locations]:
    blank_grid[location] = '.'

grids = []
for i in range(0, interval):
    grid = g.Grid(dict(blank_grid.grid))
    for symbol, locations in blizzards.items():
        for location in locations:
            if grid[location] == '.':
                grid[location] = symbol
            else:
                grid[location] = '*'
    grids.append(grid)
    blizzards = {
        symbol: [move_blizzard(symbol, location) for location in locations]
        for symbol, locations in blizzards.items()
    }

entry_marker = (-1, entry_coords)
exit_marker = (-1, exit_coords)
graph = nx.DiGraph()
for i, grid in enumerate(grids):
    next_i = (i + 1) % len(grids)
    next_grid = grids[next_i]
    for space in grid.find_cells("."):
        if next_grid[space] == ".":
            graph.add_edge((i, space), (next_i, space), distance=1)  # Can stand still
        for dir in d.UDLR_DIRECTIONS.values():
            target_space = dir.move(space)
            if next_grid.get(target_space) == ".":
                graph.add_edge((i, space), (next_i, target_space), distance=1)  # Can move to adjacent target space
    graph.add_edge((i, exit_coords), exit_marker, distance=0)
    graph.add_edge((i, entry_coords), entry_marker, distance=0)

# Part 1
print(nx.shortest_path_length(graph, (0, entry_coords), exit_marker, weight="distance"))

# Part 2
pass1 = nx.shortest_path(graph, (0, entry_coords), exit_marker, weight="distance")[0:-1]
pass1_endtime, pass1_endcoords = pass1[-1]

pass2 = nx.shortest_path(graph, (pass1_endtime+1, pass1_endcoords), entry_marker, weight="distance")[0:-1]
pass2_endtime, pass2_endcoords = pass2[-1]

pass3 = nx.shortest_path(graph, (pass2_endtime+1, pass2_endcoords), exit_marker, weight="distance")[0:-1]
print(len(pass1) + len(pass2) + len(pass3) - 1)
