#!/usr/bin/python3
# Advent of code 2020 day 12
# See https://adventofcode.com/2020/day/12
from functools import reduce

from aoc2020.modules.directions import COMPASS_DIRECTIONS

with open("input.txt") as f:
    lines = f.readlines()


def part1():
    ship = (0, 0)
    direction = COMPASS_DIRECTIONS["E"]
    for line in lines:
        cmd, qty = line[0], int(line[1:])
        if cmd in COMPASS_DIRECTIONS:
            ship = COMPASS_DIRECTIONS[cmd].move(ship, qty)
        elif cmd == "F":
            ship = direction.move(ship, qty)
        elif cmd == "L":
            direction = direction.turn_left(qty // 90)
        elif cmd == "R":
            direction = direction.turn_right(qty // 90)
    print(abs(ship[0]) + abs(ship[1]))


def part2():
    ship = (0, 0)
    waypoint = (10, -1)
    for line in lines:
        cmd, qty = line[0], int(line[1:])
        if cmd in COMPASS_DIRECTIONS:
            waypoint = COMPASS_DIRECTIONS[cmd].move(waypoint, qty)
        elif cmd == "F":
            ship = (ship[0] + waypoint[0] * qty, ship[1] + waypoint[1] * qty)
        elif cmd == "L":
            waypoint = reduce(lambda c, _: (c[1], 0 - c[0]), range(0, qty // 90), waypoint)
        elif cmd == "R":
            waypoint = reduce(lambda c, _: (0 - c[1], c[0]), range(0, qty // 90), waypoint)
    print(abs(ship[0]) + abs(ship[1]))


part1()
part2()
