#!/usr/bin/python3
# Advent of code 2020 day 1
# See https://adventofcode.com/2020/day/1

import itertools

with open("input.txt") as f:
    values = [int(line) for line in f.readlines()]

for pairs in itertools.combinations(values, 2):
    if sum(pairs) == 2020:
        print(pairs[0] * pairs[1])

for triples in itertools.combinations(values, 3):
    if sum(triples) == 2020:
        print(triples[0] * triples[1] * triples[2])
