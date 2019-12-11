#!/usr/bin/python3
# Advent of code 2019 day 11

from aoc2019.modules import intcode

DIRECTIONS = {
    "up": ((0, -1), "left", "right"),
    "left": ((-1, 0), "down", "up"),
    "down": ((0, 1), "right", "left"),
    "right": ((1, 0), "up", "down")
}


def paint(initial_colour):
    program = intcode.load_file("input.txt", debug=False)

    cells = {}
    cells_painted_once = set()
    current_location = (0, 0)
    direction = "up"

    # Part 1 starts on black, part 2 starts on white
    cells[current_location] = initial_colour

    while True:
        program.input.append(cells.get(current_location, 0))
        new_colour = program.next_output()
        if new_colour is None:
            break
        cells[current_location] = new_colour
        if new_colour == 1:
            cells_painted_once.add(current_location)
        turn = program.next_output()
        if turn == 0:
            direction = DIRECTIONS[direction][1]
        elif turn == 1:
            direction = DIRECTIONS[direction][2]
        else:
            raise Exception(f"Unexpected turn {turn}")
        move = DIRECTIONS[direction][0]
        current_location = (current_location[0] + move[0], current_location[1] + move[1])

    return cells_painted_once, cells


def print_cells(cells):
    xs = [c[0] for c in cells.keys()]
    ys = [c[1] for c in cells.keys()]
    for y in range(min(ys) - 1, max(ys) + 2):
        row = []
        for x in range(min(xs) - 1, max(xs) + 2):
            if cells.get((x, y), 0) == 1:
                row.append("*")
            else:
                row.append(" ")
        print("".join(row))


def part1():
    cells_painted_once, cells = paint(initial_colour=0)
    print(len(cells_painted_once))


def part2():
    cells_painted_once, cells = paint(initial_colour=1)
    print_cells(cells)


if __name__ == "__main__":
    part1()
    part2()
