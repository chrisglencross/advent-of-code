#!/usr/bin/python3
# Advent of code 2021 day 13
# See https://adventofcode.com/2021/day/13
import re
from functools import reduce

from aoc2021.modules import grid as g

with open("input.txt") as f:
    blocks = f.read().split("\n\n")
    paper = set((int(x), int(y)) for x, y in [line.split(",") for line in blocks[0].split("\n")])
    instructions = [(xy, int(n))
                    for line in blocks[1].split("\n")
                    for xy, n in [re.search("^fold along ([xy])=([0-9]+)$", line).groups()]]


def fold(paper, instruction):
    xy, line_no = instruction
    return set(((x, 2 * line_no - y if y > line_no else y) if xy == 'y' else (2 * line_no - x if x > line_no else x, y))
               for x, y in paper)


# Part 1
print(len(fold(paper, instructions[0])))

# Part 2
g.Grid(dict((coords, '#') for coords in reduce(fold, instructions, paper))).print()
