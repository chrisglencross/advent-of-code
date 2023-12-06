#!/usr/bin/python3
# Advent of code 2023 day 6
# See https://adventofcode.com/2023/day/6
import functools
import operator
import math

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


# Number of integer values t where t^2 - Tt + D < 0
# T is race time, D is race distance, t is time holding button
def get_t_range(T, D):
    s = math.sqrt(T*T-4*D)
    t0 = (T-s)/2
    t1 = (T+s)/2
    t0 = math.ceil(t0) if t0 < math.ceil(t0) else math.ceil(t0)+1
    t1 = math.floor(t1) if t1 > math.floor(t1) else math.floor(t1)-1
    return t1 - t0 + 1


times = [int(t) for t in lines[0].split(":")[1].split()]
distances = [int(d) for d in lines[1].split(":")[1].split()]
print(functools.reduce(operator.mul, (get_t_range(T, D) for T, D in zip(times, distances))))

T = int(lines[0].split(":")[1].replace(' ', ''))
D = int(lines[1].split(":")[1].replace(' ', ''))
print(get_t_range(T, D))
