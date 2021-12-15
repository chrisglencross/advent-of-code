#!/usr/bin/python3
# Advent of code 2021 day 15
# See https://adventofcode.com/2021/day/15

import networkx as nx
from aoc2021.modules import grid as g


def find_route(grid):
    graph = grid.build_digraph(distance_function=lambda grid, _, to_coords: int(grid[to_coords]))
    tx, ty = grid.get_size()
    return nx.shortest_path_length(graph, (0, 0), (tx-1, ty-1), weight="distance")


# Part 1
grid = g.load_grid("input.txt")
print(find_route(grid))

# Part 2
big_rows = []
for i in range(5):
    for y in range(grid.get_height()):
        big_row = []
        for j in range(5):
            for x in range(grid.get_width()):
                big_row.append(str((int(grid[(x, y)]) + i + j - 1) % 9 + 1))
        big_rows.append("".join(big_row))

grid = g.parse_grid("\n".join(big_rows))
print(find_route(grid))

