#!/usr/bin/python3
# Advent of code 2015 day 17
# See https://adventofcode.com/2015/day/17
import itertools

with open("input.txt") as f:
    containers = [int(line) for line in f.readlines()]

result = 0
min_containers = len(containers)
for i in range(1, len(containers) + 1):
    for c in itertools.combinations(containers, i):
        if sum(c) == 150:
            result += 1
            min_containers = min(min_containers, i)

print("Part 1:", result)
print("Part 2:", len([c for c in itertools.combinations(containers, min_containers) if sum(c) == 150]))
