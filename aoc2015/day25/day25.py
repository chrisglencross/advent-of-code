#!/usr/bin/python3
# Advent of code 2015 day 25
# See https://adventofcode.com/2015/day/25


def get_cell_number(row, col):
    # Get the triangular number at the top right corner (row 1) of the diagonal containing this cell,
    # then subtract (row number - 1) to move towards the bottom left. Note: nth triangular number is n*(n+1)/2
    # e.g. row=4 col=3 has 21 at the top right of its diagonal (row=1 col=6). This diagonal has 18 at row 4.
    #    | 1   2   3   4   5   6
    # ---+---+---+---+---+---+---+
    #  1 |  1   3   6  10  15 (21)
    #  2 |  2   5   9  14  20
    #  3 |  4   8  13  19
    #  4 |  7  12 [18]
    #  5 | 11  17
    #  6 | 16
    triangle_size = row + col - 1
    return triangle_size * (triangle_size + 1) // 2 - (row - 1)


def calc_nth_value(n):
    # Calculate 20151125 * 252533 * 252533 * 252533 * ... with modular arithmetic, modulus 33554393
    return 20151125 * pow(252533, n - 1, 33554393) % 33554393


cell_number = get_cell_number(2947, 3029)
value = calc_nth_value(cell_number)
print(value)
