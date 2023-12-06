#!/usr/bin/python3
# Advent of code 2023 day 6
# See https://adventofcode.com/2023/day/6
import functools
import operator
import math

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


# Number of integer values t where t^2 - Tt + D < 0
def get_t_range(T, D):
    s = math.sqrt(T*T-4*D)
    t0 = (T-s)/2
    t1 = (T+s)/2
    t0 = math.ceil(t0) if t0 < math.ceil(t0) else math.ceil(t0)+1
    t1 = math.floor(t1) if t1 > math.floor(t1) else math.floor(t1)-1
    return t1 - t0 + 1


times = [int(t) for t in lines[0].split(":")[1].split()]
distances = [int(d) for d in lines[1].split(":")[1].split()]
print(functools.reduce(operator.mul, (get_t_range(t, d) for t, d in zip(times, distances))))

t = int(lines[0].split(":")[1].replace(' ', ''))
d = int(lines[1].split(":")[1].replace(' ', ''))
print(get_t_range(t, d))
