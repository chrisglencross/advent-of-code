#!/usr/bin/python3
# Advent of code 2022 day 14
# See https://adventofcode.com/2022/day/14
import itertools
import aoc2022.modules.grid as g

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


def load_grid(lines):
    grid = g.Grid({})
    for line in lines:
        points = [(int(c[0]), int(c[1])) for c in [coords.split(",") for coords in line.split(" -> ")]]
        c = points[0]
        grid[c] = "#"
        for p in points[1:]:
            while c != p:
                if c[0] < p[0]:
                    c = (c[0] + 1, c[1])
                elif c[0] > p[0]:
                    c = (c[0] - 1, c[1])
                if c[1] < p[1]:
                    c = (c[0], c[1] + 1)
                elif c[1] > p[1]:
                    c = (c[0], c[1] - 1)
                grid[c] = '#'
    return grid


def drop_sand(grid: g.Grid, x, y):
    bottom = grid.get_bounds()[1][1]
    while y < bottom:
        c = next((c for c in [(x, y+1), (x-1, y+1), (x+1, y+1)] if grid.get(c, '.') == '.'), None)
        if c:
            x, y = c
        else:
            grid[(x, y)] = "O"
            return False
    return True


# Part 1
grid = load_grid(lines)
for i in itertools.count():
    if drop_sand(grid, 500, 0):
        print(i)
        break

# Part 2
grid = load_grid(lines)
bottom = grid.get_bounds()[1][1]
for x in range(0, 1000):
    grid[(x, bottom+1)] = "#"
for i in itertools.count():
    drop_sand(grid, 500, 0)
    if grid.get((500, 0), '.') != '.':
        print(i+1)
        break
