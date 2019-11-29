#!/usr/bin/python3
# Advent of code 2017 day 15
# See https://adventofcode.com/2017/day/15

from dataclasses import dataclass


@dataclass
class Generator:
    factor: int
    value: int
    modulo: int = 1

    def next(self):
        while True:
            self.value = (self.factor * self.value) % 2147483647
            if self.value % self.modulo == 0:
                return self.value


if __name__ == "__main__":

    # Part 1
    G1 = Generator(factor=16807, value=883)
    G2 = Generator(factor=48271, value=879)
    count = 0
    for i in range(0, 40000000):
        if G1.next() & 0xffff == G2.next() & 0xffff:
            count = count + 1
        if i % 1000000 == 0:
            print(f"Progress: {i} -> {count}")
    print(count)

    # Part 2
    G1 = Generator(factor=16807, value=883, modulo=4)
    G2 = Generator(factor=48271, value=879, modulo=8)
    count = 0
    for i in range(0, 5000000):
        if G1.next() & 0xffff == G2.next() & 0xffff:
            count = count + 1
        if i % 100000 == 0:
            print(f"Progress: {i} -> {count}")
    print(count)
