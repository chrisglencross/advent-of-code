#!/usr/bin/python3
# Advent of code 2025 day 3
# See https://adventofcode.com/2025/day/3

import aoc2025.modules as aoc
aoc.download_input("2025", "3")

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


def joltage(bank, n):
    digits = ""
    for i in range(1-n, 1):
        digit = max(bank if i == 0 else bank[0:i])
        digits += digit
        bank = bank[bank.index(digit)+1:]
    return int(digits)


print(sum(joltage(line, 2) for line in lines))
print(sum(joltage(line, 12) for line in lines))
