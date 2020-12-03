#!/usr/bin/python3
# Advent of code 2020 day 3
# See https://adventofcode.com/2020/day/3
from operator import mul
from functools import reduce

with open("input.txt") as f:
    grid = f.readlines()


def count_trees(right, down):
    width = len(grid[0].strip())
    x = 0
    c = 0
    for y in range(0, len(grid), down):
        if grid[y][x % width] == "#":
            c += 1
        x += right
    return c


print(count_trees(3, 1))
print(reduce(mul, [count_trees(*coords) for coords in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]]))
