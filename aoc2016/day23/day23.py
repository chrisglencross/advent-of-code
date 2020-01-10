#!/usr/bin/python3
# Advent of code 2016 day 23
# See https://adventofcode.com/2016/day/23

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
        addr = int(match.group(2))
        program.append(("jnz", value, addr))
    elif match := re.fullmatch(r"jnz ([a-d]) (-?\d+)", line):
        reg = match.group(1)
        addr = int(match.group(2))
        program.append(("jnz", reg, addr))
    elif match := re.fullmatch(r"jnz ([-?\d]+) ([a-d]+)", line):
        reg = int(match.group(1))
        addr = match.group(2)
        program.append(("jnz", reg, addr))
    elif match := re.fullmatch(r"tgl (-?\d+)", line):
        addr = int(match.group(1))
        program.append(("tgl", addr))
    elif match := re.fullmatch(r"tgl ([a-z]+)", line):
        addr = match.group(1)
        program.append(("tgl", addr))
    else:
        raise Exception(f"Unknown command '{line}'")


def arg_value(registers, value):
    if type(value) is int:
        return value
    else:
        return registers[value]


# registers = {"a": 7, "b": 0, "c": 0, "d": 0}  # Part 1
registers = {"a": 12, "b": 0, "c": 0, "d": 0}  # Part 2

pc = 0
optimize = True  # Optional for part 1, required for part 2
while 0 <= pc < len(program):
    # print(f"{pc}: {program[pc]}")
    op, *args = program[pc]

    # Part 2 - we need to optimize this multiplication loop
    if pc == 3:
        print(f"Registers before mult = {registers}")
        if optimize:
            registers["a"] = registers["a"] * registers["b"]
            registers["d"] = 0
            pc = 10
            continue
    if pc == 10:
        print(f"Registers after mult = {registers}")

    if op == "cpy":
        if type(args[1]) != int:
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
            pc += arg_value(registers, args[1])
        else:
            pc += 1
    elif op == "tgl":
        addr = pc + arg_value(registers, args[0])
        if 0 <= addr < len(program):
            other_op, *other_args = program[addr]

            if other_op == "inc":
                replace_op = "dec"
            elif len(other_args) == 1:
                replace_op = "inc"
            elif other_op == "jnz":
                replace_op = "cpy"
            elif len(other_args) == 2:
                replace_op = "jnz"
            print(f"  => TOGGLING {addr}: op={other_op} {other_args} with {replace_op}")
            program[addr] = tuple([replace_op, *other_args])
        pc += 1
    else:
        raise Exception(f"Unknown op {op}")
    # print(f"  => pc={pc} reg={registers}")

print(registers)
