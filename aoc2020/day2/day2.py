#!/usr/bin/python3
# Advent of code 2020 day 2
# See https://adventofcode.com/2020/day/2

import re
import itertools


def is_valid1(n1, n2, char, password):
    counts = dict([(c, len(list(cs))) for c, cs in itertools.groupby(sorted(password))])
    return n1 <= counts.get(char, 0) <= n2


def is_valid2(n1, n2, char, password):
    return (password[n1 - 1] == char) != (password[n2 - 1] == char)


def count_valid(is_valid):
    valid = 0
    for line in lines:
        match = re.search("^([0-9]+)-([0-9]+) (.): (.*)$", line.strip())
        if match and is_valid(int(match.group(1)), int(match.group(2)), match.group(3),  match.group(4)):
            valid += 1
    return valid


with open("input.txt") as f:
    lines = f.readlines()

print("Part 1:", count_valid(is_valid1))
print("Part 2:", count_valid(is_valid2))
