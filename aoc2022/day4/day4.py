#!/usr/bin/python3
# Advent of code 2022 day 4
# See https://adventofcode.com/2022/day/4

import re

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

total1 = 0
total2 = 0
for line in lines:
    e1s, e1e, e2s, e2e = (int(i) for i in re.match("^([0-9]+)-([0-9]+),([0-9]+)-([0-9]+)$", line).groups())
    s1 = set(range(e1s, e1e+1))
    s2 = set(range(e2s, e2e+1))
    overlap = len(s1.intersection(s2))
    if overlap == min(len(s1), len(s2)):
        total1 += 1
    if overlap > 0:
        total2 += 1
print(total1)
print(total2)
