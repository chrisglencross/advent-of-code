#!/usr/bin/python3
# Advent of code 2016 day 23
# See https://adventofcode.com/2016/day/23

from aoc2016.modules import assembunny

program = assembunny.load_program("input.txt", registers={"a": 7})
program.run()
print("Part 1", program.registers["a"])


# Part 2 contains nested loops between pc=3 and pc=10 which perform a multiplication
# Optimize these loops with a Python implementation and skip to pc=3
def optimized_multiplication(program: assembunny.Program):
    program.registers["a"] = program.registers["a"] * program.registers["b"]
    program.registers["d"] = 0
    program.pc = 10


program = assembunny.load_program("input.txt", registers={"a": 12}, optimizations={3: optimized_multiplication})
program.run()
print("Part 2", program.registers["a"])
