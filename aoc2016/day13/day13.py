#!/usr/bin/python3
# Advent of code 2016 day 13
# See https://adventofcode.com/2016/day/13
import networkx as nx

from aoc2016.modules import grid as g


def get_cell(x, y):
    value = x * x + 3 * x + 2 * x * y + y + y * y + 1350
    bits = sum([int(bit) for bit in "{0:b}".format(value)])
    return "." if bits % 2 == 0 else "#"


def load_graph():
    cells = {}
    for x in range(0, 100):
        for y in range(0, 100):
            cells[(x, y)] = get_cell(x, y)
    return g.Grid(cells).build_graph()


distances = nx.shortest_path_length(load_graph(), (1, 1))
print("Part 1:", distances[(31, 39)])
print("Part 2:", len([distance for distance in distances.values() if distance <= 50]))
