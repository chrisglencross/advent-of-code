#!/usr/bin/python3
# Advent of code 2023 day 1
# See https://adventofcode.com/2023/day/1

NUMERIC_DIGIT_VALUES = {str(x): x for x in range(0, 10)}
WORD_DIGIT_VALUES = NUMERIC_DIGIT_VALUES | {
    "zero":  0,
    "one":   1,
    "two":   2,
    "three": 3,
    "four":  4,
    "five":  5,
    "six":   6,
    "seven": 7,
    "eight": 8,
    "nine":  9,
}


def find_value(line, first, values):
    find_function = line.find if first else line.rfind
    return sorted([(index, value)
                   for index, value in [(find_function(token), value) for token, value in values.items()]
                   if index >= 0], reverse=not first)[0][1]


def line_value(line, values):
    return 10*find_value(line, True, values) + find_value(line, False, values)


with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]
    print(sum(line_value(line, NUMERIC_DIGIT_VALUES) for line in lines))
    print(sum(line_value(line, WORD_DIGIT_VALUES) for line in lines))
