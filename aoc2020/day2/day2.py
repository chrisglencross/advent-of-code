#!/usr/bin/python3
# Advent of code 2020 day 2
# See https://adventofcode.com/2020/day/2

import re
import itertools


def is_valid1(minimum, maximum, char, password):
    counts = dict([(c, len(list(cs))) for c, cs in itertools.groupby(sorted(password))])
    return minimum <= counts.get(char, 0) <= maximum


def is_valid2(minimum, maximum, char, password):
    return (password[minimum-1] == char) != (password[maximum-1] == char)


def count_valid(lines, is_valid):
    valid = 0
    for line in lines:
        match = re.search("^([0-9]+)-([0-9]+) (.): (.*)$", line.strip())
        if match:
            minimum = int(match.group(1))
            maximum = int(match.group(2))
            char = match.group(3)
            password = match.group(4)
            if is_valid(minimum, maximum, char, password):
                valid += 1
    return valid


with open("input.txt") as f:
    lines = f.readlines()
print("Part 1:", count_valid(lines, is_valid1))
print("Part 2:", count_valid(lines, is_valid2))
