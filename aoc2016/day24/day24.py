#!/usr/bin/python3
# Advent of code 2016 day 24
# See https://adventofcode.com/2016/day/24
import itertools
from functools import lru_cache

import networkx as nx

from aoc2016.modules import grid as g


def is_navigable(grid, from_coord, to_coord):
    return grid[from_coord] in ".0123456789" and grid[to_coord] in ".0123456789"


grid = g.load_grid("input.txt")
graph = grid.build_graph(is_navigable=is_navigable)

destinations = {}
for i in range(1, 9):
    cells = grid.find_cells(str(i))
    if cells:
        assert len(cells) == 1
        destinations[i] = cells[0]


@lru_cache
def get_distance(location, next_location):
    return nx.shortest_path_length(graph, location, next_location)


# False for Part 1, True for Part 2
return_to_base = True

shortest_length = 100000
shortest_route = None
start_location = grid.find_cells("0")[0]
count = 0
for route in itertools.permutations(destinations.keys()):
    location = start_location
    length = 0
    for destination in route:
        next_location = destinations[destination]
        length += get_distance(location, next_location)
        location = next_location
    if return_to_base:
        length += get_distance(location, start_location)
    if length < shortest_length:
        shortest_length = length
        shortest_route = route

print(shortest_route)
print(shortest_length)
