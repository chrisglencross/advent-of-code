#!/usr/bin/python3
# Advent of code 2023 day 25
# See https://adventofcode.com/2023/day/25

import networkx as nx
from networkx.algorithms import approximation as approx

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

graph = nx.Graph()
for line in lines:
    c0, rest = line.split(": ")
    for c1 in rest.split():
        graph.add_edge(c0, c1)

node0 = list(graph.nodes)[0]
this_half = {node0}
other_half = set()
for node1 in [n for n in graph.nodes if n != node0]:
    # local_node_connectivity(n1, n2) returns the minimum number edges to remove in order to disconnect n1 and n2.
    # If we can disconnect them by removing 3 edges, then they will be in opposite halves (based on an understanding
    # from the question that there is only one set of 3 edges which will split the graph).
    # https://networkx.org/documentation/stable/_modules/networkx/algorithms/approximation/connectivity.html#node_connectivity
    connectivity = approx.local_node_connectivity(graph, node0, node1, cutoff=4)
    half = this_half if connectivity > 3 else other_half
    half.add(node1)
print(len(this_half) * len(other_half))
