#!/usr/bin/python3
# Advent of code 2022 day 13
# See https://adventofcode.com/2022/day/13

from functools import cmp_to_key

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


def compare(p0, p1):
    if type(p0) == int and type(p1) == int:
        return 0 if p0 == p1 else -1 if p0 < p1 else 1
    if type(p0) == list and type(p1) == int:
        return compare(p0, [p1])
    if type(p0) == int and type(p1) == list:
        return compare([p0], p1)
    for i0, i1 in zip(p0, p1):
        r = compare(i0, i1)
        if r != 0:
            return r
    return compare(len(p0), len(p1))


# Part 1
t = 0
packets = []
for i in range(0, len(lines), 3):
    p0 = eval(lines[i])
    p1 = eval(lines[i+1])
    packets.extend([p0, p1])
    if compare(p0, p1) <= 0:
        t += (i//3) + 1
print(t)

# Part 2
packets.extend([[2], [6]])
packets.sort(key=cmp_to_key(compare))
i0 = packets.index([2]) + 1
i1 = packets.index([6]) + 1
print(i0 * i1)
