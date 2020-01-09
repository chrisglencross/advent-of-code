#!/usr/bin/python3
# Advent of code 2016 day 16
# See https://adventofcode.com/2016/day/16


def parse(s):
    return [int(c) for c in s]


def format(a):
    return "".join([str(c) for c in a])


def next_data(a):
    return a + [0] + [1 - c for c in reversed(a)]


def checksum(a):
    while True:
        b = []
        for i in range(0, len(a), 2):
            b.append(1) if a[i] == a[i + 1] else b.append(0)
        if len(b) % 2 == 1:
            return b
        a = b


data = parse("10010000000110000")
# disk = 272     # Part 1
disk = 35651584  # Part 2

while len(data) < disk:
    data = next_data(data)

print("Answer:", format(checksum(data[:disk])))
