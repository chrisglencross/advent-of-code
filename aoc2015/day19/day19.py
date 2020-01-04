#!/usr/bin/python3
# Advent of code 2015 day 19
# See https://adventofcode.com/2015/day/19
import re

with open("input.txt") as f:
    lines = f.readlines()

replacements = []
medicine = None
for line in lines:
    line = line.strip()
    match = re.search("^(.+) => (.+)$", line)
    if match:
        replacements.append((match.group(1), match.group(2)))
    elif line:
        medicine = line


def reduce(replacements, formula, depth):
    """Reduces the formula back towards its initial state, by performing reverse substitutions. Attempts
    the most reducing steps first."""
    if formula == "e":
        return depth
    for r, s in replacements:
        parts = formula.split(s)
        for i in range(1, len(parts)):
            molecule = s.join(parts[0:i]) + r + s.join(parts[i:])
            reduction_steps = reduce(replacements, molecule, depth + 1)
            if reduction_steps is not None:
                return reduction_steps
    return None


def part1():
    molecules = set()
    for s, r in replacements:
        parts = medicine.split(s)
        for i in range(1, len(parts)):
            molecule = s.join(parts[0:i]) + r + s.join(parts[i:])
            molecules.add(molecule)
    print("Part 1:", len(molecules))


def part2():
    sorted_replacements = sorted(replacements, key=lambda r: len(r[0]) - len(r[1]))
    print("Part 2:", reduce(sorted_replacements, medicine, 0))


part1()
part2()
