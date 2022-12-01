#!/usr/bin/python3
# Advent of code 2022 day 1
# See https://adventofcode.com/2022/day/1

with open("input.txt") as f:
    blocks = f.read().split("\n\n")

elf_calories = sorted([
    sum([int(line) for line in block.split("\n")])
    for block in blocks], reverse=True)

print(elf_calories[0])
print(sum(elf_calories[0:3]))
