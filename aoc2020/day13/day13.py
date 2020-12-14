#!/usr/bin/python3
# Advent of code 2020 day 13
# See https://adventofcode.com/2020/day/13
import functools
import numpy

with open("input.txt") as f:
    lines = f.readlines()

arrive = int(lines[0])
buses = lines[1].strip().split(",")


def part1():
    times = [int(bus) for bus in buses if bus != "x"]
    n = sorted([(m, m - (arrive % m)) for m in times], key=lambda p: p[1])
    print(n[0][0] * n[0][1])


def reduce_buses(bus1, bus2):
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
    # n1 = (offset2-offset1) * f1_inverse (mod f2)

    # Calculate f1_inverse (Python 3.8+)
    f1_inverse = pow(f1, -1, f2)

    # Solve:
    n1 = ((offset2 - offset1) * f1_inverse) % f2
    t = n1 * f1 + offset1

    # Both buses leave every f minutes after t
    f = numpy.lcm(f1, f2, dtype=numpy.object_)

    return t, f


def part2():
    # Rather than having buses first depart simultaneously at t=0 and check when they arrive i minutes apart, we'll
    # have the buses first depart at t=-i minutes and find a solution when they arrive simultaneously.
    # Amounts to the same thing.
    times = [(-i, int(t)) for i, t in enumerate(buses) if t != 'x']
    print(functools.reduce(reduce_buses, times)[0])


part1()
part2()
