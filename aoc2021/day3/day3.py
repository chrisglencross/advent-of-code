#!/usr/bin/python3
# Advent of code 2021 day 3
# See https://adventofcode.com/2021/day/3

# With hindsight this might have been more readable with string manipulation
# rather than bitwise Boolean operators.

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

BIT_COUNT = len(lines[0])
VALUES = [int(line, 2) for line in lines]


def bit_value(bit):
    return 2 ** (BIT_COUNT - bit - 1)


def count_bits(values, bit):
    return sum([1 for value in values if bit_value(bit) & value != 0])


def max_bits(values, find_most_frequent):
    bit_counts = [count_bits(values, i) for i in range(BIT_COUNT)]
    return sum([bit_value(i)
                for i, c in enumerate(bit_counts)
                if (find_most_frequent and c >= len(values) // 2) or (not find_most_frequent and c < len(values) // 2)])


# Part 1
gamma = max_bits(VALUES, True)
epsilon = max_bits(VALUES, False)
print(gamma * epsilon)


def filter_values(values, find_most_frequent):
    i = 0
    while len(values) > 1:
        mask = bit_value(i)
        pattern = max_bits(values, find_most_frequent)
        values = [v for v in values if v & mask == pattern & mask]
        i += 1
    return values[0]


# Part 2
o2_generator = filter_values(VALUES, True)
co2_scrubber = filter_values(VALUES, False)
print(o2_generator * co2_scrubber)
