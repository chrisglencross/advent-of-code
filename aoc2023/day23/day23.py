#!/usr/bin/python3
# Advent of code 2023 day 23
# See https://adventofcode.com/2023/day/23
from collections import defaultdict

import networkx as nx
from aoc2023.modules import grid as g
from aoc2023.modules.directions import COMPASS_DIRECTIONS

grid = g.load_grid("input.txt")
start = [(x, 0) for x in range(0, grid.get_width()) if grid[(x, 0)] == "."][0]
end = [(x, grid.get_height()-1) for x in range(0, grid.get_width()) if grid[(x, grid.get_height()-1)] == "."][0]


# Part 1
def distance_function1(grid, from_coord, to_coord):
    from_symbol = grid[from_coord]
    to_symbol = grid[to_coord]
    if from_symbol == "." and to_symbol != "#":
        return 1
    direction = {">": "E", "v": "S", "<": "W", "^": "N"}.get(from_symbol)
    if direction and COMPASS_DIRECTIONS[direction].move(from_coord) == to_coord:
        return 1
    return None


graph = grid.build_digraph(distance_function=distance_function1)
longest_path = max((path for path in nx.all_simple_paths(graph, start, end)), key=lambda path: len(list(path)))
print(len(longest_path)-1)


# Part 2

def simplify_node(graph, node):
    to_nodes = list(graph[node])
    if len(to_nodes) == 2:
        node1 = to_nodes[0]
        node2 = to_nodes[1]
        d1 = graph.get_edge_data(node, node1)["distance"]
        d2 = graph.get_edge_data(node, node2)["distance"]
        graph.remove_edge(node, node1)
        graph.remove_edge(node, node2)
        graph.add_edge(node1, node2, distance=d1 + d2)
        graph.remove_node(node)


def simplify_graph(graph):
    for node in list(graph.nodes):
        if node in graph.nodes:
            simplify_node(graph, node)


def distance_function2(grid, from_coord, to_coord):
    return 1 if grid[from_coord] != "#" and grid[to_coord] != "#" else None


graph = grid.build_graph(distance_function=distance_function2)
simplify_graph(graph)
longest_path = max((path for path in nx.all_simple_paths(graph, start, end)), key=lambda path: nx.path_weight(graph, path, "distance"))
print(nx.path_weight(graph, longest_path, "distance"))
