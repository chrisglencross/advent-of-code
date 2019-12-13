#!/usr/bin/python3
# Advent of code 2019 day 13

from dataclasses import dataclass

from aoc2019.modules import intcode


@dataclass
class MyClass:
    name: str
    size: int
    properties: dict


def get_outputs(program):
    x = program.next_output()
    if x is None:
        return None, None, None
    y = program.next_output()
    tile = program.next_output()
    return x, y, tile


def part1():
    program = intcode.load_file("input.txt", input=[1], debug=False)
    cells = dict()
    while True:
        x, y, tile = get_outputs(program)
        if x is None:
            break
        cells[(x, y)] = tile
    print(count_blocks(cells))
    print_grid(cells)


def count_blocks(cells):
    return len([cell for cell in cells.values() if cell == 2])


def print_grid(cells):
    xs = set([c[0] for c in cells.keys() if c[0] >= 0])
    ys = set([c[0] for c in cells.keys() if c[0] >= 0])
    for y in range(min(ys), max(ys) + 1):
        row = []
        for x in range(min(xs), max(xs) + 1):
            cell = cells.get((x, y), 0)
            if cell == 0:
                cell = " "
            elif cell == 1:
                cell = "#"
            elif cell == 2:
                cell = "."
            elif cell == 3:
                cell = "_"
            elif cell == 4:
                cell = "o"
            else:
                cell = str(cell)
            row.append(cell)
        print("".join(row))


def get_coords(cells: dict, symbol):
    coords = [item[0] for item in cells.items() if item[1] == symbol]
    if len(coords) == 0:
        return None, None
    return coords[0]


def part2():
    program = intcode.load_file("input.txt", input=[1], debug=False)
    program.memory[0] = 2
    cells = {}
    score = 0
    while True:

        # Update Display
        while True:
            x, y, tile = get_outputs(program)
            if program.is_terminated() or program.is_blocked():
                break
            elif x == -1 and y == 0:
                score = tile
            else:
                cells[(x, y)] = tile

        # print_grid(cells)
        # print(f"Score: {score}")

        if program.is_terminated() or count_blocks(cells) == 0:
            print("Game Over")
            break

        # Play the game
        ball_x, ball_y = get_coords(cells, 4)
        bat_x, bat_y = get_coords(cells, 3)
        if bat_x < ball_x:
            program.input.append(1)
        elif bat_x > ball_x:
            program.input.append(-1)
        else:
            program.input.append(0)

    # Summarize the game
    print_grid(cells)
    print(f"Final Score: {score}")


if __name__ == "__main__":
    # part1()
    part2()
