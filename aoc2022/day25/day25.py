#!/usr/bin/python3
# Advent of code 2022 day 25
# See https://adventofcode.com/2022/day/25

def snafu_to_decimal(value):
    digit_value = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}[value[-1]]
    remaining_digits = value[0:-1]
    if not remaining_digits:
        return digit_value
    else:
        return digit_value + 5*snafu_to_decimal(remaining_digits)


with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]
total = sum(snafu_to_decimal(line) for line in lines)
print(total)

# Discovered manually by calling snafu_to_decimal with some big numbers with the format n==============
# until we find a number just smaller than the target, then incrementing the most significant digits while
# staying just below the target.
print(snafu_to_decimal("2=0=02-0----2-=02-10"))