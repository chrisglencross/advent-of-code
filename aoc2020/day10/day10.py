#!/usr/bin/python3
# Advent of code 2020 day 10
# See https://adventofcode.com/2020/day/10
import itertools
from functools import cache

with open("input.txt") as f:
    values = sorted([0] + [int(line) for line in f.readlines()])

# Part 1
groups = dict([(k, len(list(v))) for k, v in itertools.groupby(sorted([n-p for p, n in zip(values, values[1:] + [values[-1]+3])]))])
print(groups[1] * groups[3])

# Part 2
@cache
def count_options(prev, remaining):
    if len(remaining) <= 1:
        return 1
    options = count_options(remaining[0], remaining[1:])
    if remaining[1] - prev <= 3:
        options += count_options(prev, remaining[1:])
    return options

print(count_options(values[0], tuple(values[1:])))
