#!/usr/bin/python3
# Advent of code 2021 day 10
# See https://adventofcode.com/2021/day/10
import functools

def scan(line):
    pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
    stack = []
    for c in line:
        if c in pairs.keys():
            stack.append(pairs[c])
        elif c != stack.pop():
            return c, reversed(stack)
    return None, reversed(stack)


with open("input.txt") as f:
    scan_results = [scan(line.strip()) for line in f.readlines()]

# Part 1
part1_scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
print(sum(part1_scores.get(c, 0) for c, _ in scan_results))

# Part 2
part2_scores = {")": 1, "]": 2, "}": 3, ">": 4}
scores = sorted([
    functools.reduce(lambda acc, c: acc * 5 + part2_scores[c], completion, 0)
    for error, completion in scan_results
    if not error])
print(scores[len(scores) // 2])
