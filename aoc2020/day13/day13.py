#!/usr/bin/python3
# Advent of code 2020 day 13
# See https://adventofcode.com/2020/day/13
import functools
import numpy

with open("input.txt") as f:
    lines = f.readlines()

arrive = int(lines[0])
busses = lines[1].strip().split(",")


def part1():
    times = [int(bus) for bus in busses if bus != "x"]
    n = sorted([(m, m - (arrive % m)) for m in times], key=lambda p: p[1])
    print(n[0][0] * n[0][1])


def reduce_busses(bus1, bus2):
    """Given two buss definitions (time of first departure, aka offset, and frequency) return a pair containing time
    when both simultaneously depart, and the frequency of when this happens.

    The result can be treated as a synthetic bus in further reduce operations."""

    f1 = bus1[1]
    f2 = bus2[1]
    offset1 = bus1[0] % f1
    offset2 = bus2[0] % f2

    # THE MATHS BIT (comment is bigger than the code):

    # Find t such that:
    # (t % f1) = offset1, and
    # (t % f2) = offset2

    # Rewrite using integer constants n1 and n2:
    # t = n1*f1 + offset1
    # t = n2*f2 + offset2

    # Rearrange:
    # n1*f1 + offset1 = n2*f2 + offset2
    # n1*f1 - n2*f2   = offset2 - offset1

    # Solve using approach at
    # https://trans4mind.com/personal_development/mathematics/numberTheory/indeterminateEquations.htm

    # Using invariant n2*f2 = 0 (mod f2),
    # n1*f1 = offset2-offset1 (mod f2)
    # n1 = (offset2 -offset1) * f1_inverse (mod f2)

    # Calculate f1_inverse (Python 3.8+)
    f1_inverse = pow(f1, -1, f2)

    # Solve:
    n1 = (f1_inverse * (offset2 - offset1)) % f2
    t = n1 * f1 + offset1

    return t, numpy.lcm(f1, f2, dtype=numpy.object_)


def part2():
    times = [(int(t) - i, int(t)) for i, t in enumerate(busses) if t != 'x']
    print(functools.reduce(reduce_busses, times)[0])


part1()
part2()
