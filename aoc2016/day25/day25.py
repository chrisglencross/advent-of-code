#!/usr/bin/python3
# Advent of code 2016 day 23
# See https://adventofcode.com/2016/day/23

from aoc2016.modules import assembunny


# I actually did this by reverse engineering the program to work out what it was doing
# (see annotated_input.tx and converted_input.txt) but here's the easier way...

def get_first_outputs(program):
    outputs = []
    while len(outputs) < 20:
        outputs.append(program.next_output())
    return outputs


for a in range(0, 1000):
    program = assembunny.load_program("input.txt", registers={"a": a})
    if [0, 1] * 10 == get_first_outputs(program):
        print("Answer:", a)
        break
