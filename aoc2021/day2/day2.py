#!/usr/bin/python3
# Advent of code 2021 day 2
# See https://adventofcode.com/2021/day/2

import re

with open("input.txt") as f:
    lines = f.readlines()


def follow_commands(lines, forward, depth):
    p, d, aim = 0, 0, 0
    for line in lines:
        match re.search("^([a-z]+) ([0-9]+)$", line.strip()).groups():
            case ["forward", x]:
                p, d, aim = forward(p, d, aim, int(x))
            case ["up", x]:
                p, d, aim = depth(p, d, aim, -int(x))
            case ["down", x]:
                p, d, aim = depth(p, d, aim, int(x))
    print(p * d)


follow_commands(lines,
                lambda p, d, aim, x: (p + x, d, aim),
                lambda p, d, aim, x: (p, d + x, aim))
follow_commands(lines,
                lambda p, d, aim, x: (p + x, d + (x * aim), aim),
                lambda p, d, aim, x: (p, d, aim + x))
