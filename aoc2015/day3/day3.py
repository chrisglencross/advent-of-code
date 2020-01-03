#!/usr/bin/python3
# Advent of code 2015 day 3
# See https://adventofcode.com/2015/day/3

locations = [(0, 0), (0, 0)]
visited = {(0, 0)}

with open("input.txt") as f:
    lines = f.readlines()

for i, c in enumerate(lines[0]):

    index = i % 2
    location = locations[index]
    if c == "<":
        new_location = (location[0] - 1, location[1])
    if c == ">":
        new_location = (location[0] + 1, location[1])
    if c == "v":
        new_location = (location[0], location[1] - 1)
    if c == "^":
        new_location = (location[0], location[1] + 1)
    locations[index] = new_location
    visited.add(new_location)

print(len(visited))
