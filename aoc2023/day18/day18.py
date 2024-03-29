#!/usr/bin/python3
# Advent of code 2023 day 18
# See https://adventofcode.com/2023/day/18
import itertools

from aoc2023.modules.directions import UDLR_DIRECTIONS

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


def to_lines(instructions):
    vlines = []
    hlines = []
    coords = (0, 0)
    for steps, direction in instructions:
        new_coords = UDLR_DIRECTIONS[direction].move(coords, int(steps))
        if direction in "UD":
            vlines.append((coords[0], min(coords[1], new_coords[1]), max(coords[1], new_coords[1])))
        else:
            hlines.append((coords[1], min(coords[0], new_coords[0]), max(coords[0], new_coords[0])))
        coords = new_coords
    return hlines, vlines


def get_rectangle_regions(hlines, vlines):
    x_values = sorted(list({v for v, _, _ in vlines}))
    y_values = sorted(list({v for v, _, _ in hlines}))
    regions = []
    for y0, y1 in zip(y_values, y_values[1:]):
        for x0, x1 in zip(x_values, x_values[1:]):
            regions.append(((x0, y0), (x1, y1)))
    return regions


def measure_area(instructions):

    hlines, vlines = to_lines(instructions)
    regions = get_rectangle_regions(hlines, vlines)

    filled_region_total = 0
    corners = set()
    for (rx0, ry0), (rx1, ry1) in regions:
        hlines_above = sum([1 for y, x0, x1 in hlines if x0 <= rx0 < x1 and y <= ry0])
        vlines_left = sum([1 for x, y0, y1 in vlines if y0 <= ry0 < y1 and x <= rx0])

        if hlines_above % 2 == 1 and vlines_left % 2 == 1:

            # This rectangle is inside the boundary of the shape

            # Rectangle coordinates are inclusive top/left exclusive bottom/right
            # If there is a boundary touching the bottom/right of this region we need to be inclusive of that
            boundary_on_right = any([True for x, y0, y1 in vlines if y0 <= ry0 < y1 and x == rx1])
            boundary_on_bottom = any([True for y, x0, x1 in hlines if x0 <= rx0 < x1 and y == ry1])

            # If there is a concave bottom/right corner on the boundary we will double count it to the bottom/left of
            # one region and to the top/right of another. Deduplicate these corners.
            overlapped_corners = 0

            width = rx1 - rx0
            if boundary_on_right:
                width += 1
                top_right_corner = (rx1, ry0)
                overlapped_corners += 1 if top_right_corner in corners else 0
                corners.add(top_right_corner)

            height = ry1 - ry0
            if boundary_on_bottom:
                height += 1
                bottom_left_corner = (rx0, ry1)
                overlapped_corners += 1 if bottom_left_corner in corners else 0
                corners.add(bottom_left_corner)

            filled_region_total += width * height - overlapped_corners

    return filled_region_total


# Part 1
instructions = [(int(steps), direction)
                for direction, steps, _ in [line.split() for line in lines]]
print(measure_area(instructions))

# Part 2
instructions = [(int(rgb[2:-2], 16), {"0": "R", "1": "D", "2": "L", "3": "U"}[rgb[-2]])
                for _, _, rgb in [line.split() for line in lines]]
print(measure_area(instructions))