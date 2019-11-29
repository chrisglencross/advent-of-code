#!/usr/bin/python3
# Advent of code 2017 day 16
# See https://adventofcode.com/2017/day/16


def spin(programs: list, count):
    for i in range(0, count):
        programs.insert(0, programs.pop())


def swap_pos(programs: list, a, b):
    t = programs[a]
    programs[a] = programs[b]
    programs[b] = t


def swap(programs: list, a, b):
    swap_pos(programs, programs.index(a), programs.index(b))


def dance(commands, dancers):
    for command in commands:
        if command[0] == 's':
            spin(dancers, int(command[1:]))
        elif command[0] == 'x':
            positions = [int(pos) for pos in command[1:].split("/")]
            swap_pos(dancers, *positions)
        elif command[0] == 'p':
            positions = [pos for pos in command[1:].split("/")]
            swap(dancers, *positions)
        else:
            raise Exception("Unknown command: " + command)


if __name__ == "__main__":

    with open("input.txt") as f:
        commands = f.readlines()[0].split(",")

    base_dancers = [chr(c) for c in range(ord('a'), ord('q'))]

    # Part 1
    dancers = list(base_dancers)
    print("".join(dancers))
    dance(commands, dancers)
    print("".join(dancers))

    # Part 2
    seen = {}
    dancers = list(base_dancers)
    repetition_start = None
    interval = None
    for i in range(0, 1000000000):
        d = tuple(dancers)
        if d in seen.keys():
            print(f"Sequence seen at {seen[d]} seen again at {i}")
            repetition_start = seen[d]
            interval = i - repetition_start
            break
        seen[d] = i
        dance(commands, dancers)

    if interval is not None:
        dancers = list(base_dancers)
        for i in range(0, repetition_start):
            dance(commands, dancers)
        for i in range(0, 1000000000 % interval):
            dance(commands, dancers)

    print("".join(dancers))
