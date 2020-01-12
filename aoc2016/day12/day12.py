#!/usr/bin/python3
# Advent of code 2016 day 12
# See https://adventofcode.com/2016/day/12
from aoc2016.modules import assembunny

program = assembunny.load_program("input.txt")
program.run()
print("Part 1:", program.registers["a"])

program = assembunny.load_program("input.txt", registers={"c": 1})
program.run()
print("Part 2:", program.registers["a"])
