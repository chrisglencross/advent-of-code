#!/usr/bin/python3
# Advent of code 2019 day 19
from itertools import count

from aoc2019.modules import intcode
from aoc2019.modules import textgridprinter

PROGRAM = intcode.load_file("input.txt", input=[0, 0], debug=True)
grid_printer = textgridprinter.TextGridPrinter()


def is_in_grid(x, y):
    program = PROGRAM.snapshot()
    program.input.extend([x, y])
    return program.next_output() == 1


def part1():
    grid = {}
    total = 0
    for y in range(0, 50):
        for x in range(0, 50):
            if is_in_grid(x, y):
                total += 1
                grid[(x, y)] = "#"
            else:
                grid[(x, y)] = " "
    grid_printer.print(grid)
    return total


def approximate_top_ratio():
    top_ratio_approx = 1.00
    top_ratio_min = top_ratio_approx * 0.95
    top_ratio_max = top_ratio_approx * 1.05
    x = 10000000
    previous_y = None
    while True:
        top_ratio_approx = (top_ratio_min + top_ratio_max) / 2
        y = int(top_ratio_approx * x)
        if y == previous_y:
            break
        previous_y = y
        if is_in_grid(x, y):
            top_ratio_max = top_ratio_approx
        else:
            top_ratio_min = top_ratio_approx
    return top_ratio_approx


def approximate_bottom_ratio():
    bottom_ratio_approx = 1.25
    bottom_ratio_min = bottom_ratio_approx * 0.95
    bottom_ratio_max = bottom_ratio_approx * 1.05
    x = 10000000
    previous_y = None
    while True:
        bottom_ratio_approx = (bottom_ratio_min + bottom_ratio_max) / 2
        y = int(bottom_ratio_approx * x)
        if y == previous_y:
            break
        previous_y = y
        if is_in_grid(x, y):
            bottom_ratio_min = bottom_ratio_approx
        else:
            bottom_ratio_max = bottom_ratio_approx
    return bottom_ratio_approx


def part2():
    # Find the slope of the top and bottom parts of the beam
    top_ratio = approximate_top_ratio()
    bottom_ratio = approximate_bottom_ratio()

    # Start searching from the point where the beam has height 100
    start_left_x = int(100 / (bottom_ratio - top_ratio))
    for left_x in count(start_left_x):
        right_x = left_x + 99
        top_y_approx = int(right_x * top_ratio)
        for top_y in range(top_y_approx - 3, top_y_approx + 3):
            bottom_y = top_y + 99
            if is_in_grid(left_x, bottom_y) and is_in_grid(right_x, top_y):
                assert is_in_grid(left_x, top_y)
                assert is_in_grid(right_x, bottom_y)
                assert not is_in_grid(right_x + 1, top_y)
                assert not is_in_grid(right_x, top_y - 1)
                assert not is_in_grid(left_x - 1, bottom_y)
                assert not is_in_grid(left_x, bottom_y + 1)
                return left_x * 10000 + top_y


print("Part 1:", part1())
print("Part 2:", part2())
