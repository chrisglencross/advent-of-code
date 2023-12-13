#!/usr/bin/python3
# Advent of code 2023 day 12
# See https://adventofcode.com/2023/day/12
from functools import cache


@cache
def count_possible_matches(pattern, ranges):

    if not pattern and ranges:
        return 0

    if not ranges:
        return 0 if any(c == "#" for c in pattern) else 1

    if pattern[0] == ".":
        return count_possible_matches(pattern[1:], ranges)

    next_range_length = ranges[0]
    is_possible_start_of_range = next_range_length <= len(pattern) and \
        all(c != "." for c in pattern[0:next_range_length]) and \
        (next_range_length == len(pattern) or pattern[next_range_length] != "#")

    dot_matches = 0 if pattern[0] == "#" else count_possible_matches(pattern[1:], ranges)
    hash_matches = 0 if not is_possible_start_of_range else count_possible_matches(pattern[next_range_length+1:], ranges[1:])
    return dot_matches + hash_matches


with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

# Part 1
print(sum(count_possible_matches(p1, tuple(int(n) for n in p2.split(",")))
          for p1, p2 in [line.split() for line in lines]))

# Part 2
print(sum(count_possible_matches("?".join([p1] * 5), tuple(int(n) for n in p2.split(","))*5)
          for p1, p2 in [line.split() for line in lines]))

