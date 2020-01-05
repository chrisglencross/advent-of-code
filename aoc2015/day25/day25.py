#!/usr/bin/python3
# Advent of code 2015 day 25
# See https://adventofcode.com/2015/day/25


def calc_nth_value(n):
    return 20151125 * pow(252533, n - 1, 33554393) % 33554393


def get_n(row, col):
    return (col + row - 1) * (col + row) // 2 - (row - 1)


n = get_n(2947, 3029)
value = calc_nth_value(n)
print(value)
