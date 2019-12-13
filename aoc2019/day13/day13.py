#!/usr/bin/python3
# Advent of code 2019 day 13

from aoc2019.modules import intcode
from aoc2019.modules.imagegridprinter import ImageGridPrinter
from aoc2019.modules.textgridprinter import TextGridPrinter

GENERATE_ANIMATED_GIF = True

if GENERATE_ANIMATED_GIF:
    grid_printer = ImageGridPrinter(filename="game.gif", sample=10, max_height=256, max_width=256,
                                    colour_map={0: (0, 0, 0), 1: (255, 255, 255), 2: (128, 128, 128), 3: (0, 255, 255),
                                                4: (255, 0, 0)})
else:
    grid_printer = TextGridPrinter(symbol_map={0: " ", 1: "#", 2: ".", 3: "_", 4: "o"})


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
    grid_printer.print(cells)


def get_coords(cells: dict, symbol):
    coords = [item[0] for item in cells.items() if item[1] == symbol]
    if len(coords) == 0:
        return None, None
    return coords[0]


def signum(x):
    return (x > 0) - (x < 0)


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

        print_grid(cells)

        if program.is_terminated() or count_blocks(cells) == 0:
            print("Game Over")
            break

        # Move the bat left or right to follow the ball
        ball_x, ball_y = get_coords(cells, 4)
        bat_x, bat_y = get_coords(cells, 3)
        program.input.append(signum(ball_x - bat_x))

    print(f"Final Score: {score}")
    grid_printer.close()


if __name__ == "__main__":
    part1()
    part2()
