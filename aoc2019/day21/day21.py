#!/usr/bin/python3
# Advent of code 2019 day 21

from aoc2019.modules import intcode


def part1():
    program = intcode.load_file("input.txt")
    program.append_ascii_input_lines([
        "NOT A J",
        "NOT B T",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "WALK"
    ])
    message = program.next_ascii_output()
    print(message)
    print(program.next_output())


def part2():
    program = intcode.load_file("input.txt")
    program.append_ascii_input_lines([
        "NOT A J",
        "NOT B T",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "NOT E T",
        "NOT T T",
        "OR H T",
        "AND T J",
        "RUN"
    ])
    message = program.next_ascii_output()
    print(message)
    print(program.next_output())


if __name__ == "__main__":
    part1()
    part2()
