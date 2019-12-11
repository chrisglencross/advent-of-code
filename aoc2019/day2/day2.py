#!/usr/bin/python3
# Advent of code 2019 day 2


with open("input.txt") as f:
    lines = f.readlines()

program = [int(value) for value in lines[0].split(",")]


def run_program(program, noun, verb):
    # replace position 1 with the value 12 and replace position 2 with the value 2.
    program[1] = noun
    program[2] = verb

    pc = 0
    while program[pc] != 99:
        opcode = program[pc]
        if opcode == 1:
            val1 = program[program[pc + 1]]
            val2 = program[program[pc + 2]]
            program[program[pc + 3]] = val1 + val2
            pc = pc + 4
        elif opcode == 2:
            val1 = program[program[pc + 1]]
            val2 = program[program[pc + 2]]
            program[program[pc + 3]] = val1 * val2
            pc = pc + 4
        else:
            raise Exception(f"Unknown opcode {opcode}")

    return program[0]


# Part 1
print(run_program(list(program), 12, 2))

# Part 2
for noun in range(0, 100):
    for verb in range(0, 100):
        if run_program(list(program), noun, verb) == 19690720:
            print(100 * noun + verb)
