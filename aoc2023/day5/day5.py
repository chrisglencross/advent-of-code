#!/usr/bin/python3
# Advent of code 2023 day 5
# See https://adventofcode.com/2023/day/5

import re

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

seeds = [int(seed) for seed in lines[0].split(": ")[1].split()]
maps = {}
for line in lines[1:]:
    header = re.match("^([a-z]+)-to-([a-z]+) map:$", line)
    if header:
        from_type, to_type = header.groups()
    elif line:
        to_start, from_start, length = (int(i) for i in line.split())
        maps[(from_type, from_start, from_start + length)] = (to_type, to_start, to_start + length)


def map_range(range_type, range_start, range_end):
    result = []
    for ((from_type, from_start, from_end), (to_type, to_start, to_end)) in sorted(maps.items()):
        if range_type == from_type:
            result_type = to_type
        if range_type == from_type and range_end > from_start and range_start < from_end:
            overlap_start = max(range_start, from_start)
            overlap_end = min(range_end, from_end)
            shift = to_start - from_start
            if range_start < from_start:
                result.append((to_type, range_start, overlap_start))
            result.append((to_type, overlap_start + shift, overlap_end + shift))
            range_start = overlap_end
    if range_end > range_start:
        result.append((result_type, range_start, range_end))
    return result


def get_min_location(seed_ranges):
    locations = []
    for seed_start, seed_length in seed_ranges:
        ranges = [("seed", seed_start, seed_start + seed_length)]
        while ranges[0][0] != "location":
            new_ranges = []
            for r in ranges:
                new_ranges.extend(map_range(*r))
            ranges = new_ranges
        locations.extend(ranges)
    return min(s for _, s, _ in locations)


print(get_min_location([(seed, 1) for seed in seeds]))
print(get_min_location(zip(seeds[::2], seeds[1::2])))
