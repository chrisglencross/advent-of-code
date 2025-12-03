#!/usr/bin/python3
# Advent of code 2025 day 2
# See https://adventofcode.com/2025/day/2

import aoc2025.modules as aoc
aoc.download_input("2025", "2")

with open("input.txt") as f:
    ranges = f.readline().strip().split(",")


def get_invalid_ids(r: str, repeats: int) -> set[int]:
    start, end = r.split("-")
    start_value, end_value = int(start), int(end)
    invalid_ids = set()
    repeat_digits = len(start) // repeats
    if repeat_digits > 0:
        prefix = int(start[0:repeat_digits])
    else:
        prefix = 0
    while True:
        value = int(str(prefix) * repeats)
        if value > end_value:
            break
        if start_value <= value <= end_value:
            invalid_ids.add(value)
        prefix += 1
    return invalid_ids


def part1():
    result = 0
    for r in ranges:
        result += sum(get_invalid_ids(r, 2))
    return result


def part2():
    result = 0
    for r in ranges:
        invalid_ids = set()
        for repeats in range(2, len(r)):
            invalid_ids.update(get_invalid_ids(r, repeats))
        result += sum(invalid_ids)
    return result


print(part1())
print(part2())

