#!/usr/bin/python3
# Advent of code 2023 day 9
# See https://adventofcode.com/2023/day/9

def calculate_next(row):
    rows = [row]
    while not all(v == 0 for v in row):
        row = [v2 - v1 for v1, v2 in zip(row, row[1:])]
        rows.append(row)
    return sum([row[-1] for row in reversed(rows)])


with open("input.txt") as f:
    lines = [[int(i) for i in line.split()] for line in f.readlines()]
print(sum(calculate_next(line) for line in lines))
print(sum(calculate_next(list(reversed(line))) for line in lines))
