#!/usr/bin/python3
# Advent of code 2025 day 9
# See https://adventofcode.com/2025/day/9
import itertools

import aoc2025.modules as aoc

aoc.download_input("2025", "9")

with open("input.txt") as f:
    coords = [tuple(int(c) for c in line.split(",")) for line in [line.strip() for line in f.readlines()]]

def rectangle_area(c0, c1):
    return (abs(c1[0] - c0[0]) + 1) * (abs(c1[1] - c0[1]) + 1)

print("Part 1:", max(rectangle_area(c0, c1)
                     for c0, c1 in itertools.permutations(coords, 2)))

# Vertical and horizontal edges of border
v_edges= []
h_edges = []
for c0, c1 in itertools.pairwise(coords + coords[0:1]):
    if c0[0] == c1[0]:
        v_edges.append(tuple(sorted([c0, c1])))
    else:
        h_edges.append(tuple(sorted([c0, c1])))

def any_edge_intersects_rectangle_interior(c0, c1):
    min_x, min_y = min(c0[0], c1[0]), min(c0[1], c1[1])
    max_x, max_y = max(c0[0], c1[0]), max(c0[1], c1[1])
    return (any(min_x < v0[0] < max_x and (v0[1] < max_y and v1[1] > min_y) for v0, v1 in v_edges) or
            any(min_y < h0[1] < max_y and (h0[0] < max_x and h1[0] > min_x) for h0, h1 in h_edges))

print("Part 2:", max(rectangle_area(c0, c1)
                     for c0, c1 in itertools.permutations(coords, 2)
                     if not any_edge_intersects_rectangle_interior(c0, c1)))
