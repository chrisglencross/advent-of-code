#!/usr/bin/python3
# Advent of code 2021 day 13
# See https://adventofcode.com/2021/day/13
import re
from functools import reduce

from aoc2021.modules import grid as g

with open("input.txt") as f:
    blocks = f.read().replace("\r", "").split("\n\n")
    paper = set((int(x), int(y)) for x, y in [line.split(",") for line in blocks[0].split("\n")])
    instructions = [(xy, int(n))
                    for line in blocks[1].split("\n")
                    for xy, n in [re.search("^fold along ([xy])=([0-9]+)$", line).groups()]]


def fold(paper, instruction):
    xy, line_no = instruction
    new_paper = set()
    for x, y in paper:
        if xy == 'y':
            if y < line_no:
                new_paper.add((x, y))
            elif y > line_no:
                new_paper.add((x, 2 * line_no - y))
        elif xy == 'x':
            if x < line_no:
                new_paper.add((x, y))
            elif x > line_no:
                new_paper.add((2 * line_no - x, y))
    return new_paper


# Part 1
print(len(fold(paper, instructions[0])))

# Part 2
paper = reduce(fold, instructions, paper)
grid = g.Grid(dict((coords, '#') for coords in paper))
grid.print()
