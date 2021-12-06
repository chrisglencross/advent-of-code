#!/usr/bin/python3
# Advent of code 2021 day 6
# See https://adventofcode.com/2021/day/6
import itertools

with open("input.txt") as f:
    lines = f.readlines()

counters = [int(v) for v in lines[0].split(",")]
lanterns = dict((c, len(list(i))) for c, i in itertools.groupby(sorted(counters)))

print(f"Initial state: {lanterns}", lanterns)
for day in range(256):
    breeders = lanterns.get(0, 0)
    lanterns = dict((timer - 1, qty) for timer, qty in lanterns.items() if timer != 0)
    lanterns[6] = lanterns.get(6, 0) + breeders
    lanterns[8] = breeders

    total = sum(lanterns.values())
    print(f"After {day + 1} day: {lanterns} (Total={total})")
