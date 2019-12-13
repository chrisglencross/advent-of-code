#!/usr/bin/python3
# Advent of code 2019 day 5

from aoc2019.modules import intcode

intcode.load_file("input.txt").print_disassembly()

# Part 1
program = intcode.load_file("input.txt", input=[1], debug=True)
print(program.run())

# Part 2
program = intcode.load_file("input.txt", input=[5], debug=False)
print(program.run())
