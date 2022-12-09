#!/usr/bin/python3
# Advent of code 2022 day 9
# See https://adventofcode.com/2022/day/9

from aoc2022.modules.directions import UDLR_DIRECTIONS

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


def trace_route(knot_count):

    knots = [(0, 0)] * (knot_count+1)
    tail_visited = set()
    tail_visited.add(knots[-1])

    for line in lines:
        d, c = line.split(" ")
        for i in range(0, int(c)):
            knots[0] = UDLR_DIRECTIONS[d].move(knots[0])
            for k in range(1, len(knots)):
                h = knots[k-1]
                t = knots[k]
                if abs(h[0] - t[0]) > 1 or abs(h[1] - t[1]) > 1:
                    dx = max(min(h[0] - t[0], 1), -1)
                    dy = max(min(h[1] - t[1], 1), -1)
                    t = (t[0] + dx, t[1] + dy)
                    knots[k] = t
            tail_visited.add(knots[-1])

    return len(tail_visited)


print(trace_route(1))
print(trace_route(9))
