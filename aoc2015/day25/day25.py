#!/usr/bin/python3
# Advent of code 2015 day 25
# See https://adventofcode.com/2015/day/25


def get_cell_number(row, col):
    # Get the triangular number at the top right corner of the triangle containing this cell,
    # then subtract (row number - 1). Note: nth triangular number is n*(n+1)/2
    triangle_size = row + col - 1
    return triangle_size * (triangle_size + 1) // 2 - (row - 1)


def calc_nth_value(n):
    # Calculate 20151125 * 252533 * 252533 * 252533 * ... with modular arithmetic, modulus 33554393
    return 20151125 * pow(252533, n - 1, 33554393) % 33554393


cell_number = get_cell_number(2947, 3029)
value = calc_nth_value(cell_number)
print(value)
