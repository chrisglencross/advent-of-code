#!/usr/bin/python3
# Advent of code 2021 day 12
# See https://adventofcode.com/2021/day/12

import itertools


def get_paths(connections, part1):
    complete_paths = []
    paths = [['start']]
    while paths:
        new_paths = []
        for path in paths:
            lower_revisited = any(len(list(visits)) > 1 for node, visits in itertools.groupby(sorted(path)))
            for next_node in connections.get(path[-1], []):
                new_path = path + [next_node]
                if next_node == 'end':
                    complete_paths.append(new_path)
                elif next_node == 'start' or (next_node.islower() and next_node in path and (part1 or lower_revisited)):
                    pass
                else:
                    new_paths.append(new_path)
        paths = new_paths
    return complete_paths


with open("input.txt") as f:
    cs = {}
    for n1, n2 in [line.strip().split("-") for line in f.readlines()]:
        cs.setdefault(n1, list()).append(n2)
        cs.setdefault(n2, list()).append(n1)

print(len(get_paths(cs, True)))
print(len(get_paths(cs, False)))
