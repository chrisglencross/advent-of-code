#!/usr/bin/python3
# Advent of code 2025 day 8
# See https://adventofcode.com/2025/day/8
import itertools

import aoc2025.modules as aoc
aoc.download_input("2025", "8")

with open("input.txt") as f:
    coords = [tuple(int(v) for v in line.split(",")) for line in f.readlines()]

def distance_squared(pair):
    c1 = pair[0]
    c2 = pair[1]
    return (c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2

def sort_distances(coords):
    return sorted([pair for pair in itertools.combinations(coords, 2)], key=distance_squared, reverse=True)

def connect_groups(connected_groups, j0, j1):
    g0 = connected_groups[j0]
    if j1 in g0:
        return g0  # already connected
    g1 = connected_groups[j1]
    g = g0 | g1
    for j in list(g):
        connected_groups[j] = g
    return g

def part1():
    connected_groups = {j: {j} for j in coords}
    remaining_distances = sort_distances(coords)
    for i in range(0, 1000):
        j0, j1 = remaining_distances.pop()
        connect_groups(connected_groups, j0, j1)
    group_sizes = [len(s) for s in set(frozenset(g) for g in connected_groups.values())]
    sizes = sorted(group_sizes, reverse=True)
    return sizes[0] * sizes[1] * sizes[2]

def part2():
    connected_groups = {j: {j} for j in coords}
    remaining_distances = sort_distances(coords)
    while True:
        j0, j1 = remaining_distances.pop()
        g = connect_groups(connected_groups, j0, j1)
        if len(g) == len(coords):
            return j0[0] * j1[0]

print(part1())
print(part2())
