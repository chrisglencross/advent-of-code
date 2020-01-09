#!/usr/bin/python3
# Advent of code 2016 day 15
# See https://adventofcode.com/2016/day/15
import itertools
import re

with open("input.txt") as f:
    lines = f.readlines()

discs = []
for line in lines:
    # Disc #1 has 13 positions; at time=0, it is at position 10.
    if match := re.fullmatch(r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)\.", line.strip()):
        disc = int(match.group(1))
        positions = int(match.group(2))
        start = int(match.group(3))
        discs.append((disc, positions, start))

# Part 2 only
discs.append((len(discs) + 1, 11, 0))

for tick in itertools.count():
    if all((start + disc + tick) % positions == 0 for disc, positions, start in discs):
        print(tick)
        break
