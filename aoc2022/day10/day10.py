#!/usr/bin/python3
# Advent of code 2022 day 10
# See https://adventofcode.com/2022/day/10

import aoc2022.modules.grid as g

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


def get_values(lines):
    x = 1
    for line in lines:
        match line.split(" "):
            case ["addx", dx]:
                yield x
                yield x
                x += int(dx)
            case ["noop"]:
                yield x

# Part 1
print(
    sum((cycle * x)
        for cycle, x in enumerate(get_values(lines), 1)
        if cycle in [20, 60, 100, 140, 180, 220])
)


# Part 2
grid = g.Grid({})
for i, x in enumerate(get_values(lines)):
    col = i % 40
    row = i // 40
    fill = "#" if abs(col - x) <= 1 else " "
    grid[(col, row)] = fill
grid.print()
