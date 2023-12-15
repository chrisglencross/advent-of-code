#!/usr/bin/python3
# Advent of code 2023 day 15
# See https://adventofcode.com/2023/day/15

import functools


def label_hash(value):
    return functools.reduce(lambda v, c: (v+ord(c)) * 17 % 256, value, 0)


with open("input.txt") as f:
    steps = f.read().strip().split(",")

print(sum(label_hash(step) for step in steps))

# Requires Python >=3.7 to guarantee dict insertion order (3.6 should work)
boxes = [dict() for i in range(0, 256)]
for step in steps:
    if "-" in step:
        label = step.split("-")[0]
        box = label_hash(label)
        boxes[box].pop(label, None)
    if "=" in step:
        label, lens = step.split("=")
        box = label_hash(label)
        boxes[box][label] = int(lens)

print(sum((box_no+1) * (slot_no+1) * lens
          for box_no, lenses in enumerate(boxes)
          for slot_no, lens in enumerate(lenses.values())))

