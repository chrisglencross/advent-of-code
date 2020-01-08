#!/usr/bin/python3
# Advent of code 2016 day 12
# See https://adventofcode.com/2016/day/12
import re

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

program = []
for line in lines:
    if match := re.fullmatch(r"cpy (-?\d+) ([a-d])", line):
        value = int(match.group(1))
        target = match.group(2)
        program.append(("cpy", value, target))
    elif match := re.fullmatch(r"cpy ([a-d]) ([a-d])", line):
        source = match.group(1)
        target = match.group(2)
        program.append(("cpy", source, target))
    elif match := re.fullmatch(r"inc ([a-d])", line):
        program.append(("inc", match.group(1)))
    elif match := re.fullmatch(r"dec ([a-d])", line):
        program.append(("dec", match.group(1)))
    elif match := re.fullmatch(r"jnz (-?\d+) (-?\d+)", line):
        value = int(match.group(1))
        offset = int(match.group(2))
        program.append(("jnz", value, offset))
    elif match := re.fullmatch(r"jnz ([a-d]) (-?\d+)", line):
        reg = match.group(1)
        offset = int(match.group(2))
        program.append(("jnz", reg, offset))
    else:
        raise Exception(f"Unknown command '{line}'")


def arg_value(registers, value):
    if type(value) is int:
        return value
    else:
        return registers[value]


pc = 0
registers = {"a": 0, "b": 0, "c": 1, "d": 0}
while 0 <= pc < len(program):
    op, *args = program[pc]
    if op == "cpy":
        registers[args[1]] = arg_value(registers, args[0])
        pc += 1
    elif op == "inc":
        registers[args[0]] += 1
        pc += 1
    elif op == "dec":
        registers[args[0]] -= 1
        pc += 1
    elif op == "jnz":
        if arg_value(registers, args[0]) != 0:
            pc += args[1]
        else:
            pc += 1
    else:
        raise Exception(f"Unknown op {op}")

print(registers)
