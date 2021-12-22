#!/usr/bin/python3
# Advent of code 2021 day 22
# See https://adventofcode.com/2021/day/22
import itertools
import re
from dataclasses import dataclass
from typing import Tuple, List

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

# Part 1
grid = set()
for line in lines:
    on_off, *nums = re.match(r"^(on|off) x=([-0-9]+)\.\.([-0-9]+),y=([-0-9]+)\.\.([-0-9]+),z=([-0-9]+)\.\.([-0-9]+)$",
                             line).groups()
    min_x, max_x = max(int(nums[0]), -50), min(int(nums[1]), 50)
    min_y, max_y = max(int(nums[2]), -50), min(int(nums[3]), 50)
    min_z, max_z = max(int(nums[4]), -50), min(int(nums[5]), 50)
    for x, y, z in itertools.product(range(min_x, max_x + 1), range(min_y, max_y + 1), range(min_z, max_z + 1)):
        if on_off == "on":
            grid.add((x, y, z))
        else:
            grid.discard((x, y, z))
print(len(grid))


# Part 2

@dataclass
class Shape:
    on: bool
    region: Tuple[Tuple[int, int, int], Tuple[int, int, int]]
    exclusion: List["Shape"]

    def volume(self):
        self_volume = volume(self.region)
        for shape in self.exclusion:
            self_volume -= shape.intersected_volume(self.region)
        return self_volume

    def add_exclusion(self, other: "Shape"):
        if intersected_region(self.region, other.region):
            self.exclusion.append(other)

    def intersected_volume(self, other_coords):
        intersection = intersected_region(self.region, other_coords)
        if not intersection:
            return 0
        intersected_volume = volume(intersection)
        for shape in self.exclusion:
            intersected_volume -= shape.intersected_volume(intersection)
        return intersected_volume


def intersected_region(r0, r1):
    (min_x0, min_y0, min_z0), (max_x0, max_y0, max_z0) = r0
    (min_x1, min_y1, min_z1), (max_x1, max_y1, max_z1) = r1
    min_x, max_x = max(min_x0, min_x1), min(max_x0, max_x1)
    min_y, max_y = max(min_y0, min_y1), min(max_y0, max_y1)
    min_z, max_z = max(min_z0, min_z1), min(max_z0, max_z1)
    if max_x <= min_x or max_y <= min_y or max_z <= min_z:
        return None
    return (min_x, min_y, min_z), (max_x, max_y, max_z)


def volume(r):
    (min_x, min_y, min_z), (max_x, max_y, max_z) = r
    return (max_x - min_x) * (max_y - min_y) * (max_z - min_z)


shapes = []
for line in lines:
    on_off, *nums = re.match(r"^(on|off) x=([-0-9]+)\.\.([-0-9]+),y=([-0-9]+)\.\.([-0-9]+),z=([-0-9]+)\.\.([-0-9]+)$",
                             line).groups()
    min_x, max_x, min_y, max_y, min_z, max_z = (int(n) for n in nums)
    shape = Shape(on=(on_off == "on"),
                  region=((min_x, min_y, min_z), (max_x + 1, max_y + 1, max_z + 1)),
                  exclusion=list())
    for previous_shape in shapes:
        previous_shape.add_exclusion(shape)
    shapes.append(shape)

print(sum(shape.volume() for shape in shapes if shape.on))

