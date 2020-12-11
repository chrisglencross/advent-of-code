#!/usr/bin/python3
# Advent of code 2020 day 11
# See https://adventofcode.com/2020/day/11

from itertools import count

from aoc2020.modules import directions, imagegridprinter, textgridprinter, grid as g


def run(name, tick_function):
    printer = imagegridprinter.ImageGridPrinter(max_width=800, max_height=800, duration=200, filename=f"{name}.gif",
                                                colour_map={"L": (64, 255, 64), "#": (255, 64, 64), ".": (0, 0, 0)})
    # printer = textgridprinter.TextGridPrinter()
    grid = g.load_grid("input.txt")
    for i in count():
        printer.print(grid)
        new_grid = tick_function(grid)
        if new_grid.grid == grid.grid:
            print(len([v for v in grid.values() if v == '#']))
            break
        grid = new_grid

    printer.close()


def tick1(grid):
    new_grid = {}
    (min_x, min_y), (max_x, max_y) = grid.get_bounds()
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            neighbours = 0
            for direction in directions.COMPASS_DIRECTIONS_8.values():
                neighbour = grid.get(direction.move((x, y)), ".")
                if neighbour == "#":
                    neighbours += 1
            if grid[(x, y)] == "L":
                new_grid[(x, y)] = "#" if neighbours == 0 else "L"
            elif grid[(x, y)] == "#":
                new_grid[(x, y)] = "L" if neighbours >= 4 else "#"
            else:
                new_grid[(x, y)] = grid[(x, y)]
    return g.Grid(new_grid)


def can_see(grid: g.Grid, pos, direction: directions.Direction):
    while True:
        pos = direction.move(pos)
        cell = grid.get(pos)
        if cell is None or cell == "L":
            return False
        if cell == "#":
            return True


def tick2(grid):
    new_grid = {}
    (min_x, min_y), (max_x, max_y) = grid.get_bounds()
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            neighbours = 0
            for direction in directions.COMPASS_DIRECTIONS_8.values():
                if can_see(grid, (x, y), direction):
                    neighbours += 1
            if grid[(x, y)] == "L":
                new_grid[(x, y)] = "#" if neighbours == 0 else "L"
            elif grid[(x, y)] == "#":
                new_grid[(x, y)] = "L" if neighbours >= 5 else "#"
            else:
                new_grid[(x, y)] = grid[(x, y)]
    return g.Grid(new_grid)


run("part1", tick1)
run("part2", tick2)
