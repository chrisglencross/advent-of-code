#!/usr/bin/python3
# Advent of code 2021 day 22
# See https://adventofcode.com/2021/day/22
import functools
import itertools
import operator
import re
from dataclasses import dataclass, field
from typing import Tuple, List

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

# Part 1
grid = set()
for line in lines:
    on_off, *nums = re.match(r"^(on|off) x=([-0-9]+)\.\.([-0-9]+),y=([-0-9]+)\.\.([-0-9]+),z=([-0-9]+)\.\.([-0-9]+)$", line).groups()
    min_x, min_y, min_z = (max(int(n), -50) for n in (nums[0], nums[2], nums[4]))
    max_x, max_y, max_z = (min(int(n), +50) for n in (nums[1], nums[3], nums[5]))
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
    exclusion: List["Shape"] = field(default_factory=list)

    def volume(self):
        self_volume = volume(self.region)
        for shape in self.exclusion:
            self_volume -= shape.intersected_volume(self.region)
        return self_volume

    def add_exclusion(self, other: "Shape"):
        if intersected_region(self.region, other.region):
            self.exclusion.append(other)

    def intersected_volume(self, other_region):
        intersection = intersected_region(self.region, other_region)
        if not intersection:
            return 0
        intersected_volume = volume(intersection)
        for shape in self.exclusion:
            intersected_volume -= shape.intersected_volume(intersection)
        return intersected_volume


def intersected_region(region0, region1):
    intersection = (tuple(max(min_d0, min_d1) for min_d0, min_d1 in zip(region0[0], region1[0])),
                    tuple(min(max_d0, max_d1) for max_d0, max_d1 in zip(region0[1], region1[1])))
    if any(max_d <= min_d for min_d, max_d in zip(*intersection)):
        return None
    return intersection


def volume(region):
    return functools.reduce(operator.mul, (d1 - d0 for d0, d1 in zip(region[0], region[1])))


shapes = []
for line in lines:
    on_off, *nums = re.match(r"^(on|off) x=([-0-9]+)\.\.([-0-9]+),y=([-0-9]+)\.\.([-0-9]+),z=([-0-9]+)\.\.([-0-9]+)$", line).groups()
    min_x, max_x, min_y, max_y, min_z, max_z = (int(n) for n in nums)
    shape = Shape(on=(on_off == "on"), region=((min_x, min_y, min_z), (max_x + 1, max_y + 1, max_z + 1)))
    for previous_shape in shapes:
        previous_shape.add_exclusion(shape)
    shapes.append(shape)

print(sum(shape.volume() for shape in shapes if shape.on))
