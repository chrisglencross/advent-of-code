#!/usr/bin/python3
# Advent of code 2021 day 6
# See https://adventofcode.com/2021/day/6
import itertools

with open("input.txt") as f:
    lines = f.readlines()

counters = [int(v) for v in lines[0].split(",")]
lanterns = [(c, len(list(i))) for c, i in itertools.groupby(sorted(counters))]

print(f"Initial state: {lanterns}", lanterns)
for day in range(0, 256):
    breeders = sum(qty for timer, qty in lanterns if timer == 0)
    lanterns = [(timer - 1 if timer > 0 else 6, qty) for timer, qty in lanterns]
    lanterns.append((8, breeders))

    # Coalesce
    lanterns = [(timer, sum(entry[1] for entry in fish))
                for timer, fish in itertools.groupby(sorted(lanterns), key=lambda pair: pair[0])]

    total = sum([pair[1] for pair in lanterns])
    print(f"After {day + 1} day: {lanterns} (Total={total})")
