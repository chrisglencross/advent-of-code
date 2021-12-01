#!/usr/bin/python3
# Advent of code 2021 day 1
# See https://adventofcode.com/2021/day/1

with open("input.txt") as f:
    depths = [int(line) for line in f.readlines()]

print(sum([1 if d1 > d0 else 0 for d0, d1 in zip(depths, depths[1:])]))

# Two of the three values in the sliding window are always equal, so we just need to compare first and last
print(sum([1 if d3 > d0 else 0 for d0, d3 in zip(depths, depths[3:])]))
