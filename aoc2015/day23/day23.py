#!/usr/bin/python3
# Advent of code 2015 day 23
# See https://adventofcode.com/2015/day/23


with open("input.txt") as f:
    lines = f.readlines()

program = []
for line in lines:
    line = line.strip()
    op, arg_str = line.split(" ", maxsplit=1)
    args = arg_str.split(", ")
    program.append((op, args))

# Part 1
# registers = {"a": 0, "b": 0}

# Part 2
registers = {"a": 1, "b": 0}

pc = 0
while 0 <= pc < len(program):
    op, args = program[pc]
    if op == "hlf":
        registers[args[0]] //= 2
        pc += 1
    elif op == "tpl":
        registers[args[0]] *= 3
        pc += 1
    elif op == "inc":
        registers[args[0]] += 1
        pc += 1
    elif op == "jmp":
        pc += int(args[0])
    elif op == "jie":
        if registers[args[0]] % 2 == 0:
            pc += int(args[1])
        else:
            pc += 1
    elif op == "jio":
        if pc == 38:
            print(registers)
        if registers[args[0]] == 1:
            pc += int(args[1])
        else:
            pc += 1
    else:
        raise Exception(f"Unknown op {op}")

print(registers["b"])
