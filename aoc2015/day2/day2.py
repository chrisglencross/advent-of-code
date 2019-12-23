#!/usr/bin/python3
# Advent of code aoc2015 day 2
# See https://adventofcode.com/aoc2015/day/2

def get_paper_area(l, w, h):
    lw = l * w
    lh = l * h
    wh = w * h
    return min([lw, lh, wh]) + (lw + lh + wh) * 2


def get_ribbon_length(l, w, h):
    lw = 2 * (l + w)
    lh = 2 * (l + h)
    wh = 2 * (w + h)
    return min([lw, lh, wh]) + l * w * h


with open("input.txt") as f:
    lines = f.readlines()

paper_total = 0
ribbon_total = 0
for line in lines:
    line = line.strip()
    fields = line.split("x")
    l = int(fields[0])
    w = int(fields[1])
    h = int(fields[2])
    paper_total += get_paper_area(l, w, h)
    ribbon_total += get_ribbon_length(l, w, h)
print(paper_total)
print(ribbon_total)
