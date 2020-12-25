#!/usr/bin/python3
# Advent of code 2020 day 25
# See https://adventofcode.com/2020/day/25
import itertools


def transform(subject_no, loop_size):
    return pow(subject_no, loop_size, 20201227)


def find_loop_size(pubkey):
    value = 1
    for loop_size in itertools.count():
        if value == pubkey:
            return loop_size
        value = (value * 7) % 20201227


with open("input.txt") as f:
    pubkey1, pubkey2 = [int(line) for line in f.readlines()]

print(transform(pubkey1, find_loop_size(pubkey2)))
print(transform(pubkey2, find_loop_size(pubkey1)))
