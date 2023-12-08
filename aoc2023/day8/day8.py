#!/usr/bin/python3
# Advent of code 2023 day 8
# See https://adventofcode.com/2023/day/8
import math
import re

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

instructions = lines[0]

network = {}
for line in lines[2:]:
    f, l, r = re.match("^(.+) = \((.+), (.+)\)$", line).groups()
    network[f] = (l, r)

# Part 1
steps = 0
location = "AAA"
while location != "ZZZ":
    instruction = instructions[steps % len(instructions)]
    location = network[location][0] if instruction == 'L' else network[location][1]
    steps += 1
print(steps)

# Part 2
starts = {l for l in network.keys() if l.endswith("A")}
ends = {l for l in network.keys() if l.endswith("Z")}
repeat_distances = []
for start in starts:
    location = start
    visited_ends = {}
    steps = 0
    while location not in visited_ends:
        if location in ends:
            visited_ends[location] = steps
        instruction = instructions[steps % len(instructions)]
        location = network[location][0] if instruction == 'L' else network[location][1]
        steps += 1
    # Observed in input data that loop only goes back to a single end node and arrives there for the second
    # time after precisely 2x as many steps as arriving the first time. That's not necessarily true of
    # all possible input data, but it makes life much easier here. Assert it's true just to be sure.
    if len(visited_ends) > 1:
        raise NotImplementedError(f"Multiple nodes in cycle for {start}: {visited_ends}")
    distance = list(visited_ends.values())[0]
    if steps / distance != 2.0:
        raise NotImplementedError(f"Irregular repeat interval for {start}: {visited_ends}")
    repeat_distances.append(distance)

print(math.lcm(*repeat_distances))

