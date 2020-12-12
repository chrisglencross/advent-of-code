#!/usr/bin/python3
# Advent of code 2020 day 9
# See https://adventofcode.com/2020/day/9

preamble = 25
with open("input.txt") as f:
    values = [int(line) for line in f.readlines()]

for i in range(preamble, len(values)):
    v = values[i]
    previous = values[i-preamble:i]
    if len([p for p in previous if (v - p) in previous]) < 2:
        print(f"{i}: {v} not in {previous}")
        break

for j in range(0, i):
    for c in range(2, i-j):
        r = values[j:j+c]
        t = sum(r)
        if t == v:
            print(min(r) + max(r))
        elif t > v:
            break
