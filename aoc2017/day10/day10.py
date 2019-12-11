#!/usr/bin/python3
# Advent of code 2017 day 10
# See https://adventofcode.com/2017/day/10


def index(loop, i):
    return (i + len(loop)) % len(loop)


def reverse_range(loop, current, length):
    start = index(loop, current)
    end = index(loop, current + length - 1)
    for i in range(0, length // 2):
        t = loop[index(loop, start)]
        loop[index(loop, start)] = loop[index(loop, end)]
        loop[index(loop, end)] = t
        end = index(loop, end - 1)
        start = index(loop, start + 1)
    return loop


def part1():
    # Part 1
    length = 256
    loop = list(range(0, length))
    current = 0
    skip_size = 0
    with open("input.txt") as f:
        lengths = [int(length.strip()) for length in f.readlines()[0].split(",")]
    for length in lengths:
        reverse_range(loop, current, length)
        current = current + length + skip_size
        skip_size = skip_size + 1
    print(loop[0] * loop[1])


def part2():
    # Part 1

    with open("input.txt") as f:
        lengths = [ord(c) for c in f.read().strip()]
    lengths.extend([17, 31, 73, 47, 23])

    dense_hash = knot_hash(lengths)

    out = ""
    for b in dense_hash:
        out = out + f"{b:02x}"
    print(out)


def knot_hash(lengths):
    length = 256
    loop = list(range(0, length))
    current = 0
    skip_size = 0
    for i in range(0, 64):
        for length in lengths:
            reverse_range(loop, current, length)
            current = current + length + skip_size
            skip_size = skip_size + 1
    dense_hash = []
    for block in range(0, 16):
        a = 0
        for b in range(0, 16):
            a = a ^ loop[block * 16 + b]
        dense_hash.append(a)
    return dense_hash


if __name__ == "__main__":
    part1()
    part2()
