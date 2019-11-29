#!/usr/bin/python3
# Advent of code 2017 day 19
# See https://adventofcode.com/2017/day/19
import itertools

directions = {
    "right": (1, 0),
    "left": (-1, 0),
    "down": (0, 1),
    "up": (0, -1)
}

turn_directions = {
    "right": {"up", "down"},
    "left": {"up", "down"},
    "up": {"left", "right"},
    "down": {"left", "right"}
}


class Packet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current_dir = "down"
        self.destinations = []

    def try_move(self, rows, dir):
        move = directions[dir]
        next_x = self.x + move[0]
        next_y = self.y + move[1]
        if 0 <= next_y < len(rows) and 0 <= next_x < len(rows[next_y]) and rows[next_y][next_x] not in {' ', '.'}:
            print(f"Moving {dir} to {next_x}, {next_y}")
            return next_x, next_y
        else:
            return None

    def move(self, rows):
        for dir in itertools.chain.from_iterable(([self.current_dir], turn_directions[self.current_dir])):
            next_coords = self.try_move(rows, dir)
            if next_coords is not None:
                self.x = next_coords[0]
                self.y = next_coords[1]
                self.current_dir = dir
                cell = rows[self.y][self.x]
                if cell.isalnum():
                    print(f"Reached {cell}")
                    self.destinations.append(cell)
                return True

        print("Cannot move")
        return False

    def __str__(self):
        return f"{self.x},{self.y} facing {self.current_dir}"


with open("input.txt") as f:
    rows = f.readlines()

start_x = rows[0].find("|")
p = Packet(start_x, 0)
steps = 0
while True:
    steps = steps + 1
    if not p.move(rows):
        break
print("".join(p.destinations))
print(steps)
