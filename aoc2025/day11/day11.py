#!/usr/bin/python3
# Advent of code 2025 day 11
# See https://adventofcode.com/2025/day/11

from functools import lru_cache

import aoc2025.modules as aoc
aoc.download_input("2025", "11")

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

tree = {f: t.split(" ") for f, t in [line.split(": ") for line in lines]}

@lru_cache
def count_paths1(d):
    if d == "out":
        return 1
    return sum(count_paths1(nd) for nd in tree[d])

@lru_cache(1000)
def count_paths2(d, dac, fft):
    if d == "out":
        return 1 if dac and fft else 0
    return sum(count_paths2(nd, dac or nd == "dac", fft or nd == "fft") for nd in tree[d])

print(count_paths1("you"))
print(count_paths2("svr", False, False))

