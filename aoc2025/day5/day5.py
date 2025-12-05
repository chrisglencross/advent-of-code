#!/usr/bin/python3
# Advent of code 2025 day 5
# See https://adventofcode.com/2025/day/5

import aoc2025.modules as aoc

aoc.download_input("2025", "5")

with open("input.txt") as f:
    blocks = [block.strip() for block in f.read().replace('\r', '').split('\n\n')]

def ranges_containing(ranges, value):
    return [(l, h) for l, h in ranges if l <= value <= h]

def ranges_contained_by(ranges, l0, h0):
    return [(l, h) for l, h in ranges if l >= l0 and h <= h0]

def merge(ranges):
    result = set()
    for new_range in ranges:
        l, h = new_range
        overlapping = ranges_containing(result, l) + ranges_containing(result, h) + ranges_contained_by(result, l, h)
        result.difference_update(overlapping)
        for old_range in overlapping:
            new_range = (min(old_range[0], new_range[0]), max(old_range[1], new_range[1]))
        result.add(new_range)
    return result

input_ranges = [tuple(int(s) for s in line.split('-')) for line in blocks[0].split('\n')]
merged_ranges = merge(input_ranges)

print(sum(1 for line in blocks[1].split('\n') if ranges_containing(merged_ranges, int(line))))
print(sum(h - l + 1 for l, h in merged_ranges))