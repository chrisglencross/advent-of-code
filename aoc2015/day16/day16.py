#!/usr/bin/python3
# Advent of code 2015 day 16
# See https://adventofcode.com/2015/day/16

import re

expected_sue_properties = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def sue_matches_part1(sue_properties):
    return set(expected_sue_properties.items()).issuperset(set(sue_properties.items()))


def sue_matches_part2(sue_properties):
    for key, value in sue_properties.items():
        expected_value = expected_sue_properties[key]
        if key in ["cats", "trees"]:
            if value <= expected_value:
                return False
        elif key in ["pomeranians", "goldfish"]:
            if value >= expected_value:
                return False
        elif value != expected_value:
            return False
    return True


def find_sue(lines, matcher_fn):
    for line in lines:
        match = re.search("^Sue ([0-9]+): (.*)$", line.strip())
        if match:
            sue_no = match.group(1)
            properties = {}
            rest = match.group(2)
            for p in rest.split(", "):
                name, value = p.split(": ", 2)
                properties[name] = int(value)
            if matcher_fn(properties):
                return sue_no


with open("input.txt") as f:
    lines = f.readlines()

print("Part 1:", find_sue(lines, sue_matches_part1))
print("Part 2:", find_sue(lines, sue_matches_part2))
