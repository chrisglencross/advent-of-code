#!/usr/bin/python3
# Advent of code 2016 day 7
# See https://adventofcode.com/2016/day/7


with open("input.txt") as f:
    lines = f.readlines()

# Intentionally ignoring the regex approach which would be smaller...

# Part 1
count = 0
for line in lines:
    bracket = False
    line = line.strip()
    match = None
    abba = False
    abba_in_brackets = False
    for i, c in enumerate(line):
        if c == '[':
            bracket = True
        elif c == ']':
            bracket = False
        elif i < len(line) - 3:
            if c == line[i + 3] and c != line[i + 1] and line[i + 1] == line[i + 2] and line[i + 1] not in "[]":
                if bracket:
                    abba_in_brackets = True
                else:
                    abba = True
    if abba and not abba_in_brackets:
        count += 1
print(count)

# Part 2
count = 0
for line in lines:
    bracket = False
    line = line.strip()
    match = None
    abas = set()
    reverse_babs = set()
    for i, c in enumerate(line):
        if c == '[':
            bracket = True
        elif c == ']':
            bracket = False
        elif i < len(line) - 2:
            if c == line[i + 2] and c != line[i + 1] and line[i + 1] not in "[]":
                if bracket:
                    reverse_babs.add((line[i + 1], line[i]))
                else:
                    abas.add((line[i], line[i + 1]))
    if reverse_babs.intersection(abas):
        count += 1
print(count)
