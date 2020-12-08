#!/usr/bin/python3
# Advent of code 2020 day 8
# See https://adventofcode.com/2020/day/8

import re

with open("input.txt") as f:
    lines = f.readlines()

program = []
for line in lines:
    match = re.fullmatch(r"^([a-z]+) ([+-]\d+)$", line.strip())
    program.append((match.group(1), int(match.group(2))))


def run(program):
    pc = 0
    acc = 0
    pcs = set()
    while pc not in pcs and pc < len(program):
        pcs.add(pc)
        i, arg = program[pc]
        if i == "acc":
            acc += arg
        if i == "jmp":
            pc += arg
        else:
            pc += 1
    return pc == len(program), acc


def part1():
    print(run(program)[1])


def part2():
    for i in range(0, len(program)):
        modify = {"jmp": "nop", "nop": "jmp"}.get(program[i][0])
        if modify:
            copy = list(program)
            copy[i] = (modify, copy[i][1])
            end, acc = run(copy)
            if end:
                print(acc)


part1()
part2()

