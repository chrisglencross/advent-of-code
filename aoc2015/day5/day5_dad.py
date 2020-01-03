#!/usr/bin/python3
# Advent of code 2015 day 5
# See https://adventofcode.com/2015/day/5

import re


def count(pattern, text):
    return len(re.findall(pattern, text))


with open("input.txt") as f:
    lines = f.readlines()

nice1 = 0
nice2 = 0
for line in lines:
    if count("[aeiou]", line) >= 3 and count('(.)\\1', line) >= 1 and count("(ab|cd|pq|xy)", line) == 0:
        nice1 += 1
    if count("(..).*\\1", line) >= 1 and count("(.).\\1", line) >= 1:
        nice2 += 1

print("Part 1", nice1)
print("Part 2", nice2)
