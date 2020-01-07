#!/usr/bin/python3
# Advent of code 2016 day 1
# See https://adventofcode.com/2016/day/1

from aoc2016.modules import directions

location = (0, 0)
direction = directions.COMPASS_DIRECTIONS["N"]
visited_locations = set()
visited_locations.add(location)
hq = None

with open("input.txt") as f:
    lines = f.readlines()
for step in lines[0].split(", "):
    turn = step[0]
    move = int(step[1:])
    if turn == "L":
        direction = direction.turn_left()
    elif turn == "R":
        direction = direction.turn_right()
    for i in range(move):
        location = direction.move(location)
        if hq is None and location in visited_locations:
            hq = location
        visited_locations.add(location)

print(sum([abs(v) for v in location]))
print(sum([abs(v) for v in hq]))
