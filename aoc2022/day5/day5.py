#!/usr/bin/python3
# Advent of code 2022 day 5
# See https://adventofcode.com/2022/day/5

import re


def init_stacks(start_stacks):
    stacks = []
    start_stacks = list(reversed(start_stacks))
    for i in range(0, (len(start_stacks[0]) + 2) // 4):
        stacks.append(list())
    for row in start_stacks[1:]:
        for i, stack in enumerate(stacks):
            col = i * 4 + 1
            if len(row) > col and row[col] != ' ':
                stack.append(row[col])
    return stacks


def move_stacks_part1(stacks, steps):
    for line in steps:
        count, from_stack, to_stack = (int(x) for x in re.match("^move ([0-9]+) from ([0-9]+) to ([0-9]+)$", line).groups())
        for i in range(0, count):
            crate = stacks[from_stack-1].pop()
            stacks[to_stack-1].append(crate)
    return "".join(stack[-1] for stack in stacks)


def move_stacks_part2(stacks, steps):
    for line in steps:
        count, from_stack, to_stack = (int(x) for x in re.match("^move ([0-9]+) from ([0-9]+) to ([0-9]+)$", line).groups())
        crates = stacks[from_stack-1][0-count:]
        stacks[to_stack-1].extend(crates)
        del stacks[from_stack-1][0-count:]
    return "".join(stack[-1] for stack in stacks)


with open("input.txt") as f:
    start_stacks, steps = (x.split("\n") for x in f.read().split("\n\n"))
print(move_stacks_part1(init_stacks(start_stacks), steps))
print(move_stacks_part2(init_stacks(start_stacks), steps))

