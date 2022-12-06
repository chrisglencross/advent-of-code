#!/usr/bin/python3
# Advent of code 2022 day 6
# See https://adventofcode.com/2022/day/6


def find_distinct_characters(line, d):
    return next(i for i in range(d, len(line)) if len(set(line[i-d:i])) == d)


with open("input.txt") as f:
    line = f.read().strip()
print(find_distinct_characters(line, 4))
print(find_distinct_characters(line, 14))
