#!/usr/bin/python3
# Advent of code 2022 day 15
# See https://adventofcode.com/2022/day/15

import re

with open("input.txt") as f:
    lines_data = [
        tuple(int(i) for i in re.match(".*at x=([-0-9]+), y=([-0-9]+): .* x=([-0-9]+), y=([-0-9]+)", line).groups())
        for line in f.readlines()
    ]


def get_no_beacon_ranges(row_y):
    no_beacon_ranges = []
    object_positions = set()
    for sx, sy, bx, by in lines_data:
        if by == row_y:
            object_positions.add(bx)
        if sy == row_y:
            object_positions.add(sx)
        d = abs(bx - sx) + abs(by - sy)
        width_in_y = 2*d - 2*abs(sy - row_y) + 1
        if width_in_y > 0:
            x_range_in_y = ((sx - width_in_y//2), (sx + width_in_y//2 + 1))
            no_beacon_ranges.append(x_range_in_y)
    return sorted(no_beacon_ranges), object_positions


def count_in_ranges(ranges, exclude):
    if not ranges:
        return 0
    t = 0
    r1 = ranges[0][0]
    for r in ranges:
        r0 = max(r1, r[0])
        r1 = max(r1, r[1])
        range_size = r1 - r0
        t += range_size - sum(1 for e in exclude if r0 <= e < r1)
    return t


def get_range_gaps(start, end, ranges):
    end_of_previous_range = start
    gaps = []
    for r in ranges:
        r0 = max(end_of_previous_range, r[0])
        r1 = max(end_of_previous_range, r[1])
        if r0 > end_of_previous_range:
            gaps.append((end_of_previous_range, min(r0, end)))
        end_of_previous_range = max(end_of_previous_range, r1)
    if end_of_previous_range < end:
        gaps.append((end_of_previous_range, end))
    return gaps


# Part 1
ranges, object_positions = get_no_beacon_ranges(2000000)
print(count_in_ranges(ranges, object_positions))

# Part 2
for y in range(0, 4000000+1):
    ranges, _ = get_no_beacon_ranges(y)
    gaps = get_range_gaps(0, 4000000 + 1, ranges)
    if len(gaps) == 1 and (gaps[0][1] - gaps[0][0]) == 1:
        print(gaps[0][0] * 4000000 + y)
        break
