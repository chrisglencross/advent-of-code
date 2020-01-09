#!/usr/bin/python3
# Advent of code 2016 day 18
# See https://adventofcode.com/2016/day/18


def next_row(a):
    b = [None] * len(a)
    padded_a = ["."] + a + ["."]
    for i in range(0, len(a)):
        l, c, r = padded_a[i:i + 3]
        is_trap = (l == c and l != r) or (r == c and l != r)
        b[i] = "^" if is_trap else "."
    return b


def get_answer(row, rows=400000):
    safe_tiles = 0
    for i in range(0, rows):
        safe_tiles += len([c for c in row if c == "."])
        row = next_row(row)
    return safe_tiles


with open("input.txt") as f:
    initial_row = list(f.read().strip())

print("Part 1:", get_answer(initial_row, 40))
print("Part 2:", get_answer(initial_row, 400000))
