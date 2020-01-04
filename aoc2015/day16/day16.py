#!/usr/bin/python3
# Advent of code 2015 day 16
# See https://adventofcode.com/2015/day/16

import re

my_sue = {
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
my_sue_set = set(my_sue.items())

with open("input.txt") as f:
    lines = f.readlines()

for line in lines:
    # Sue 494: akitas: 4, cars: 4, vizslas: 9
    match = re.search("^Sue ([0-9]+): (.*)$", line.strip())
    if match:
        sue_no = match.group(1)
        properties = {}
        rest = match.group(2)
        for p in rest.split(", "):
            name, value = p.split(": ", 2)
            properties[name] = int(value)
        if my_sue_set.issuperset(set(properties.items())):
            print(sue_no)
