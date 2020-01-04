#!/usr/bin/python3
# Advent of code 2015 day 20
# See https://adventofcode.com/2015/day/20
import itertools
import math


def factors(n):
    result = set()
    for i in range(1, math.isqrt(n) + 1):
        if n % i == 0:
            result.add(i)
            result.add(n // i)
    return result


def factors_limited(n, limit):
    return [f for f in factors(n) if n // f <= limit]


def part1():
    for house in itertools.count(1):
        presents = 10 * sum(factors(house))
        if presents >= 34000000:
            return house


def part2():
    for house in itertools.count(1):
        presents = 11 * sum(factors_limited(house, 50))
        if presents >= 34000000:
            return house


print("Part 1:", part1())
print("Part 2:", part2())
