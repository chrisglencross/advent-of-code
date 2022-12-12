#!/usr/bin/python3
# Advent of code 2022 day 12
# See https://adventofcode.com/2022/day/12

import aoc2022.modules.grid as g
import networkx as nx


def distance_function(grid, from_coord, to_coord):
    return 1 if ord(grid[from_coord]) + 1 >= ord(grid[to_coord]) else None


grid = g.load_grid("input.txt")
start = grid.find_cell("S")
grid[start] = 'a'
end = grid.find_cell("E")
grid[end] = 'z'
graph = grid.build_digraph(distance_function=distance_function)

# Part 1
print(nx.shortest_path_length(graph, start, end))

# Part 2
all_path_lengths = nx.shortest_path_length(graph, target=end)
print(min(all_path_lengths[start] for start in grid.find_cells('a') if start in all_path_lengths))

