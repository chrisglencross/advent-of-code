#!/usr/bin/python3
# Advent of code 2016 day 20
# See https://adventofcode.com/2016/day/20


def load_ranges():
    with open("input.txt") as f:
        return sorted([tuple([int(value) for value in line.split("-")]) for line in f.readlines()])


def get_next_range_start(ranges, start):
    min_value = start
    for r in ranges:
        if r[0] > min_value:
            return min_value
        min_value = max(min_value, r[1] + 1)


def get_range_end(ranges, range_start):
    return min([r[0] for r in ranges if r[0] > range_start])


ranges = load_ranges()
print("Part 1:", get_next_range_start(ranges, 0))

total = 0
range_end = 0
while True:
    range_start = get_next_range_start(ranges, range_end)
    if range_start is None:
        break
    range_end = get_range_end(ranges, range_start)
    if range_end is None:
        range_end = 4294967295 + 1
    total += range_end - range_start

print("Part 2:", total)
