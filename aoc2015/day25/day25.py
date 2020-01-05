#!/usr/bin/python3
# Advent of code 2015 day 25
# See https://adventofcode.com/2015/day/25
from itertools import count


def calc_next(value):
    return (value * 252533) % 33554393


def calc_nth_value(n):
    # Almost certainly a better way to calculate this with powers of modular arithmetic
    # ...but this only takes a couple of seconds
    value = 20151125
    for i in range(0, n - 1):
        value = calc_next(value)
    return value


def get_n(row, col):
    # Almost certainly a better way to calculate this with some arithmetic and properties of triangular numbers
    # ...but this only takes a couple of seconds.
    x = 1
    y = 1
    for n in count(1):
        if row == y and col == x:
            return n
        if y == 1:
            y = x + 1
            x = 1
        else:
            y -= 1
            x += 1


n = get_n(2947, 3029)
print(n)
value = calc_nth_value(n)
print(value)
