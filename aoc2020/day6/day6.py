#!/usr/bin/python3
# Advent of code 2020 day 6
# See https://adventofcode.com/2020/day/6
from functools import reduce

with open("input.txt") as f:
    blocks = f.read().replace("\r", "").split("\n\n")

print(sum([len({c for l in b.split("\n") for c in l}) for b in blocks]))
print(sum([len(reduce(lambda s, o: s.intersection(o), [set(l) for l in b.split("\n")])) for b in blocks]))
