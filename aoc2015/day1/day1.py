#!/usr/bin/python3
# Advent of code aoc2015 day 1
# See https://adventofcode.com/aoc2015/day/1

with open("input.txt") as f:
    lines = f.readlines()

line = lines[0]
floor = 0
for i, c in enumerate(line):
    if c == "(":
        floor += 1
    if c == ")":
        floor -= 1
    if floor == -1:
        print("Reached floor -1 on step", i + 1)

print("Final floor is", floor)
