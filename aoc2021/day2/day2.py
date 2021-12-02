#!/usr/bin/python3
# Advent of code 2021 day 2
# See https://adventofcode.com/2021/day/2

import re

with open("input.txt") as f:
    lines = f.readlines()


def follow_commands(lines, forward, depth):
    p = d = aim = 0
    for line in lines:
        match = re.search("^([a-z]+) ([0-9]+)$", line.strip())
        command = match.group(1)
        x = int(match.group(2))
        if command == "forward":
            p, d, aim = forward(p, d, aim, x)
        elif command == "up":
            p, d, aim = depth(p, d, aim, -x)
        elif command == "down":
            p, d, aim = depth(p, d, aim, x)
    print(p * d)


follow_commands(lines,
                lambda p, d, aim, x: (p + x, d, aim),
                lambda p, d, aim, x: (p, d + x, aim))
follow_commands(lines,
                lambda p, d, aim, x: (p + x, d + (x * aim), aim),
                lambda p, d, aim, x: (p, d, aim + x))
