#!/usr/bin/python3
# Advent of code 2016 day 3
# See https://adventofcode.com/2016/day/3

import re

with open("input.txt") as f:
    lines = f.readlines()

rows = []
for line in lines:
    match = re.search("^([0-9]+) +([0-9]+) +([0-9]+)$", line.strip())
    if match:
        rows.append([int(s) for s in match.groups()])

# Part 1
count = 0
for row in rows:
    longest, *others = sorted(row, reverse=True)
    if longest < sum(others):
        count += 1
print(count)

# Part 2
count = 0
for row in range(0, len(rows), 3):
    for col in range(0, 3):
        longest, *others = sorted([rows[row][col], rows[row + 1][col], rows[row + 2][col]], reverse=True)
        if longest < sum(others):
            count += 1
print(count)
