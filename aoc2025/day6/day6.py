#!/usr/bin/python3
# Advent of code 2025 day 6
# See https://adventofcode.com/2025/day/6
import functools
import operator

import numpy

import aoc2025.modules as aoc
aoc.download_input("2025", "6")

with open("input.txt") as f:
    lines = [line.rstrip() for line in f.readlines()]

def get_func(op: str):
    return operator.mul if op == "*" else operator.add

def part1():
    numbers = []
    for line in lines[0:-1]:
        numbers.append([int(c) for c in line.split(" ") if c != ""])
    numbers = numpy.transpose(numbers)
    ops = [c for c in lines[-1].split(" ") if c != ""]
    return sum(functools.reduce(get_func(op), numbers[i]) for i, op in enumerate(ops))

def char(line, x):
    return ' ' if x >= len(line) else line[x]

def part2():
    total = 0
    numbers = []
    max_width = max(len(line) for line in lines)
    for x in range(max_width-1, -1, -1):
        digits = "".join([char(line, x) for line in lines[0:-1]]).strip()
        if digits:
            numbers.append(int(digits))
        op = char(lines[-1], x)
        if op != ' ':
            total += functools.reduce(get_func(op), numbers)
            numbers = []
    return total

print(part1())
print(part2())
