#!/usr/bin/python3
# Advent of code 2020 day 1
# See https://adventofcode.com/2020/day/1

import itertools
from operator import mul
from functools import reduce

with open("input.txt") as f:
    values = [int(line) for line in f.readlines()]


def solve(items):
    return [reduce(mul, c) for c in itertools.combinations(values, items) if sum(c) == 2020]


print(solve(2))
print(solve(3))
