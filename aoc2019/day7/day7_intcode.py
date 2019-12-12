import itertools

from aoc2019.modules import intcode

with open("input.txt") as f:
    program_data = f.readline()

# Part 1
max_output = 0
for sequence in itertools.permutations(range(0, 5)):
    previous_output = 0
    for i, s in enumerate(sequence):
        output = intcode.load_program(program_data, input=[s, previous_output]).next_output()
        previous_output = output
    max_output = max(max_output, previous_output)
print(max_output)

# Part 2
max_output = 0
for sequence in itertools.permutations(range(5, 10)):
    amps = [intcode.load_program(program_data, name="amp-" + str(i)) for i in range(0, 5)]
    for i, s in enumerate(sequence):
        amps[i].input.append(s)
    previous_output = 0
    for i in itertools.count():
        amp = amps[i % len(amps)]
        amp.input.append(previous_output)
        output = amp.next_output()
        if output is None:
            break
        previous_output = output

    max_output = max(max_output, previous_output)

print(max_output)
