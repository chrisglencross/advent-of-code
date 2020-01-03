#!/usr/bin/python3
# Advent of code 2019 day 25

from aoc2019.modules import intcode


def print_output(program):
    message = program.next_ascii_output()
    print(message)


def play(program):
    print_output(program)
    while not program.is_terminated():
        command = input("> ")
        if command == "debug":
            program.print_disassembly()
        else:
            program.append_ascii_input(command)
            print_output(program)
    print("Gnoame Over")


program = intcode.load_file("input.txt", debug=True)
play(program)
# program.print_disassembly()
