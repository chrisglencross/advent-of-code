#!/usr/bin/python3
# Advent of code 2021 day 14
# See https://adventofcode.com/2021/day/14
import re
from collections import defaultdict

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

polymer = list(lines[0])
rules = dict((tuple(match), insert)
             for match, insert
             in (re.match("^(.*) -> (.*)$", line).groups() for line in lines[2:]))

quantities = defaultdict(int)
for item in polymer:
    quantities[item] += 1

polymer_pairs = defaultdict(int)
for pair in zip(polymer, polymer[1:]):
    polymer_pairs[pair] += 1

for i in range(40):
    new_polymer_pairs = defaultdict(int)
    for pair, qty in polymer_pairs.items():
        insert = rules.get(pair)
        if insert:
            quantities[insert] += qty
            new_polymer_pairs[(pair[0], insert)] += qty
            new_polymer_pairs[(insert, pair[1])] += qty
    polymer_pairs = new_polymer_pairs

letter_frequencies = sorted(list(quantities.values()))
print(letter_frequencies[-1] - letter_frequencies[0])
