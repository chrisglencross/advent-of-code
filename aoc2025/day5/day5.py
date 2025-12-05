#!/usr/bin/python3
# Advent of code 2025 day 5
# See https://adventofcode.com/2025/day/5
import functools

import aoc2025.modules as aoc

aoc.download_input("2025", "5")

with open("input.txt") as f:
    blocks = [block.strip() for block in f.read().replace('\r', '').split('\n\n')]

def ranges_containing(ranges, value):
    return [r for r in ranges if r[0] <= value <= r[1]]

def ranges_contained_by(ranges, other):
    return [r for r in ranges if r[0] >= other[0] and r[1] <= other[1]]

def merge(ranges):
    result = set()
    for new_range in ranges:
        overlapping = ranges_containing(result, new_range[0]) + ranges_containing(result, new_range[1]) + ranges_contained_by(result, new_range)
        result.difference_update(overlapping)
        new_range = functools.reduce(lambda r0, r1: (min(r0[0], r1[0]), max(r0[1], r1[1])), overlapping, new_range)
        result.add(new_range)
    return result

input_ranges = [tuple(int(s) for s in line.split('-')) for line in blocks[0].split('\n')]
merged_ranges = merge(input_ranges)

print(sum(1 for line in blocks[1].split('\n') if ranges_containing(merged_ranges, int(line))))
print(sum(h - l + 1 for l, h in merged_ranges))