#!/usr/bin/python3
# Advent of code 2017 day 25
# See https://adventofcode.com/2017/day/25

blueprint = {
    "A": {
        0: (1, "right", "B"),
        1: (0, "left", "C")
    },
    "B": {
        0: (1, "left", "A"),
        1: (1, "left", "D")
    },
    "C": {
        0: (1, "right", "D"),
        1: (0, "right", "C")
    },
    "D": {
        0: (0, "left", "B"),
        1: (0, "right", "E")
    },
    "E": {
        0: (1, "right", "C"),
        1: (1, "left", "F")
    },
    "F": {
        0: (1, "left", "E"),
        1: (1, "right", "A")
    }
}

tape = dict()
cursor = 0
state = "A"
for step in range(0, 12172063):
    value = tape.get(cursor, 0)
    new_value, move, next_state = blueprint[state][value]
    tape[cursor] = new_value
    if move == "left":
        cursor = cursor - 1
    elif move == "right":
        cursor = cursor + 1
    else:
        raise Exception("Bad move")
    state = next_state
    if step % 100000 == 0:
        print(f"Progress... {100 * step // 12172063}%")

print(sum(tape.values()))
