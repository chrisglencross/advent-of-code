#!/usr/bin/python3
# Advent of code 2025 day 10
# See https://adventofcode.com/2025/day/10
import itertools
import re
from dataclasses import replace

import aoc2025.modules as aoc
aoc.download_input("2025", "10")

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

def get_value(candidate):
    result = 0
    for button in candidate:
        for toggle in button:
            result = result ^ (2**toggle)
    return result

part1 = 0
for line in lines:
    lights, buttons_str, joltage = re.match("^\[(.+)] (\(.+\) )+\{(.+)}$", line).groups()

    toggles = [[int(i) for i in toggle_set_str.split(",")] for toggle_set_str in buttons_str.strip().replace("(", "").replace(")", "").split(" ")]
    toggles.sort(key=len, reverse=True)

    target = int("".join(reversed(lights.replace(".", "0").replace("#", "1"))), 2)
    c = 999999
    for button_count in range(1, len(toggles)+1):
        for candidate in itertools.combinations(toggles, button_count):
            if target == get_value(candidate):
                c = min(c, button_count)
    part1 += c
print(part1)


