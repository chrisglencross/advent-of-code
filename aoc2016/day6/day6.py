#!/usr/bin/python3
# Advent of code 2016 day 6
# See https://adventofcode.com/2016/day/6
import itertools

with open("input.txt") as f:
    lines = f.readlines()


def decode(lines, most_frequent):
    message = []
    for char_no in range(0, len(lines[0]) - 1):
        chars = [line[char_no] for line in lines]
        letter_frequencies = [(len(list(g)), k) for k, g in itertools.groupby(sorted(chars))]
        frequency, letter = sorted(letter_frequencies, reverse=most_frequent)[0]
        message.append(letter)
    return "".join(message)


print("Part 1:", decode(lines, True))
print("Part 2:", decode(lines, False))
