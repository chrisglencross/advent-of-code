#!/usr/bin/python3
# Advent of code 2016 day 13
# See https://adventofcode.com/2016/day/13
import networkx as nx

from aoc2016.modules import grid as g


def get_cell(x, y):
    value = x * x + 3 * x + 2 * x * y + y + y * y + 1350
    bits = sum([int(bit) for bit in "{0:b}".format(value)])
    return "." if bits % 2 == 0 else "#"


cells = {}
for x in range(0, 100):
    for y in range(0, 100):
        cells[(x, y)] = get_cell(x, y)
grid = g.Grid(cells)

graph = grid.build_graph()
lengths = nx.shortest_path_length(graph, (1, 1))
print("Part 1:", lengths[(31, 39)])
print("Part 2:", len([(loc, length) for loc, length in lengths.items() if length <= 50]))
