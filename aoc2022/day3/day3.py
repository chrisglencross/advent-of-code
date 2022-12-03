#!/usr/bin/python3
# Advent of code 2022 day 3
# See https://adventofcode.com/2022/day/3

def score(s: set[str]):
    c = s.pop()
    return ord(c) - ord('a') + 1 if c.islower() else ord(c) - ord('A') + 27


with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

print(sum(score(set(line[0:len(line)//2]) & set(line[len(line)//2:])) for line in lines))
print(sum(score(set(lines[i]) & set(lines[i+1]) & set(lines[i+2])) for i in range(0, len(lines), 3)))
