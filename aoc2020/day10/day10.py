#!/usr/bin/python3
# Advent of code 2020 day 10
# See https://adventofcode.com/2020/day/10
from itertools import groupby
from functools import cache

with open("input.txt") as f:
    adapters = [int(line) for line in f.readlines()]
jolts = [0] + sorted(adapters) + [max(adapters) + 3]


def part1():
    diffs = [j2 - j1 for j1, j2 in zip(jolts[:-1], jolts[1:])]
    groups = dict([(k, len(list(v))) for k, v in groupby(sorted(diffs))])
    print(groups[1] * groups[3])


def part2():
    @cache
    def count_options(prev, remaining):
        if len(remaining) <= 1:
            return 1
        options = count_options(remaining[0], remaining[1:])
        if remaining[1] - prev <= 3:
            options += count_options(prev, remaining[1:])
        return options
    print(count_options(jolts[0], tuple(jolts[1:])))


part1()
part2()