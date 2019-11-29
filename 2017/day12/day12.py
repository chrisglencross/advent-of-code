#!/usr/bin/python3
# Advent of code 2017 day 12
# See https://adventofcode.com/2017/day/12

import re

import networkx as nx

G = nx.Graph()

if __name__ == "__main__":

    with open("input.txt") as f:
        lines = f.readlines()

    for line in lines:
        # 2 <-> 0, 3, 4
        match = re.search("^([0-9]+) <-> ([0-9, ]+)$", line.strip())
        if match:
            from_node = match.group(1)
            to_nodes = match.group(2).replace(" ", "").split(",")
            G.add_edges_from([(from_node, to_node) for to_node in to_nodes])
        else:
            raise Exception("Could not parse: " + line)

    # Part 1
    print([len(subgraph) for subgraph in nx.connected_components(G) if "0" in subgraph])

    # Part 2
    print(len([subgraph for subgraph in nx.connected_components(G)]))
