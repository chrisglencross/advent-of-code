#!/usr/bin/python3
# Advent of code 2019 day 23

from aoc2019.modules import intcode


def part1():
    programs = [intcode.load_file("input.txt", input=[address]) for address in range(0, 50)]
    while True:
        for i, program in enumerate(programs):
            address = program.next_output()
            if program.is_terminated():
                raise Exception(f"Program {i} terminated")
            if address is None:
                # Waiting for input; do not block
                program.input.append(-1)
            else:
                x = program.next_output()
                y = program.next_output()
                if address == 255:
                    return y
                programs[address].input.extend([x, y])


def part2():
    programs = [intcode.load_file("input.txt", input=[address]) for address in range(0, 50)]
    idle_counts = [0] * 50
    nat_value = None
    last_nat_value = None

    while True:
        for i, program in enumerate(programs):
            address = program.next_output()
            if program.is_terminated():
                raise Exception(f"Program {i} terminated")
            if address is None:
                # Waiting for input; do not block
                idle_counts[i] += 1
                program.input.append(-1)
            else:
                idle_counts[i] = 0
                x = program.next_output()
                y = program.next_output()
                if address == 255:
                    nat_value = [x, y]
                else:
                    programs[address].input.extend([x, y])

        if all([idle_count > 2 for idle_count in idle_counts]):
            if last_nat_value and last_nat_value[1] == nat_value[1]:
                return last_nat_value[1]
            last_nat_value = nat_value
            programs[0].input.extend(nat_value)


print("Part 1", part1())
print("Part 2", part2())
