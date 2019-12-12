from aoc2019.modules import intcode


def run_program(noun, verb):
    program = intcode.load_file("input.txt", debug=False)
    program.memory[1] = noun
    program.memory[2] = verb
    program.next_output()
    return program.memory[0]


# Part 1
print(run_program(12, 2))

# Part 2
for noun in range(0, 100):
    for verb in range(0, 100):
        if run_program(noun, verb) == 19690720:
            print(100 * noun + verb)
