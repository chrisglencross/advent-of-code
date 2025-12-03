#!/usr/bin/python3
# Advent of code 2025 day 1
# See https://adventofcode.com/2025/day/1

import aoc2025.modules as aoc
aoc.download_input("2025", "1")

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

def rotations(p):
    return p // 100

def dial(p):
    return p % 100

part1 = 0
part2 = 0
p = 50
for line in lines:
    lr = line[0]
    dist = int(line[1:])
    p0 = p
    if lr == "L":
        p -= dist
    else:
        p += dist

    if dial(p) == 0:
        part1 += 1

    part2 += abs(rotations(p) - rotations(p0))
    if dial(p0) == 0 and lr == 'L':
        part2 -= 1
    if dial(p) == 0 and lr == 'L':
        part2 += 1

print(part1)
print(part2)
