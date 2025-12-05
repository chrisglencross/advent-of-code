#!/usr/bin/python3
# Advent of code 2025 day 5
# See https://adventofcode.com/2025/day/5

import aoc2025.modules as aoc

aoc.download_input("2025", "5")

with open("input.txt") as f:
    blocks = [block.strip() for block in f.read().replace('\r', '').split('\n\n')]

def find_ranges_containing(ranges, i):
    return [(l, h) for l, h in ranges if l <= i <= h]

def find_ranges_contained_by(ranges, l0, h0):
    return [(l, h) for l, h in ranges if l >= l0 and h <= h0]

def merge(ranges):
    result = set()
    for l, h in ranges:
        merge_with_lo = find_ranges_containing(result, l)
        merge_with_hi = find_ranges_containing(result, h)
        eliminate = find_ranges_contained_by(result, l, h)
        result.difference_update(merge_with_lo + merge_with_hi + eliminate)
        new_range = (l, h)
        for merge_range in merge_with_lo + merge_with_hi:
            new_range = (min(merge_range[0], new_range[0]), max(merge_range[1], new_range[1]))
        result.add(new_range)
    return result

input_ranges = [tuple(int(s) for s in line.split('-')) for line in blocks[0].split('\n')]
merged_ranges = merge(input_ranges)

print(sum(1 for line in blocks[1].split('\n') if find_ranges_containing(merged_ranges, int(line))))
print(sum(h - l + 1 for l, h in merged_ranges))