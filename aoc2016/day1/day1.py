#!/usr/bin/python3
# Advent of code 2016 day 1
# See https://adventofcode.com/2016/day/1

DIRECTIONS = {
    "north": ((0, -1), {"L": "west", "R": "east"}),
    "south": ((0, 1), {"L": "east", "R": "west"}),
    "east": ((1, 0), {"L": "north", "R": "south"}),
    "west": ((-1, 0), {"L": "south", "R": "north"})
}

location = (0, 0)
direction = "north"
visited_locations = set()
visited_locations.add(location)
hq = None

with open("input.txt") as f:
    lines = f.readlines()
for step in lines[0].split(", "):
    turn = step[0]
    move = int(step[1:])
    direction = DIRECTIONS[direction][1][turn]
    delta = DIRECTIONS[direction][0]
    for i in range(move):
        location = (location[0] + delta[0], location[1] + delta[1])
        if hq is None and location in visited_locations:
            hq = location
        visited_locations.add(location)

print(sum([abs(v) for v in location]))
print(sum([abs(v) for v in hq]))
