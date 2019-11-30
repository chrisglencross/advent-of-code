#!/usr/bin/python3
# Advent of code 2017 day 22
# See https://adventofcode.com/2017/day/22

from dataclasses import dataclass

directions = {
    "up": ((0, -1), "left", "right"),
    "down": ((0, 1), "right", "left"),
    "left": ((-1, 0), "down", "up"),
    "right": ((1, 0), "up", "down")
}


@dataclass
class Virus:
    x: int = 0
    y: int = 0
    direction: str = "up"
    count: int = 0

    def turn_left(self):
        self.direction = directions[self.direction][1]

    def turn_right(self):
        self.direction = directions[self.direction][2]

    def forward(self):
        move = directions[self.direction][0]
        self.x = self.x + move[0]
        self.y = self.y + move[1]

    def is_infected(self, infections):
        return infections.get((self.x, self.y)) == "#"

    def is_weakened(self, infections):
        return infections.get((self.x, self.y)) == "W"

    def is_flagged(self, infections):
        return infections.get((self.x, self.y)) == "F"

    def infect(self, infections):
        infections[(self.x, self.y)] = "#"
        self.count = self.count + 1

    def is_clean(self, infections):
        return infections.get((self.x, self.y)) is None

    def weaken(self, infections):
        infections[(self.x, self.y)] = "W"

    def flag(self, infections):
        infections[(self.x, self.y)] = "F"

    def clean(self, infections):
        del infections[(self.x, self.y)]

    def burst(self, infections):
        # Part 1
        # if self.is_infected(infections):
        #     self.turn_right()
        #     self.clean(infections)
        # else:
        #     self.turn_left()
        #     self.infect(infections)
        # self.forward()
        # Part 2
        if self.is_clean(infections):
            self.turn_left()
            self.weaken(infections)
        elif self.is_weakened(infections):
            self.infect(infections)
        elif self.is_infected(infections):
            self.turn_right()
            self.flag(infections)
        elif self.is_flagged(infections):
            self.turn_right()
            self.turn_right()
            self.clean(infections)
        self.forward()


def print_infections(virus, infections):
    xs = [infection[0] for infection in infections]
    ys = [infection[1] for infection in infections]
    for y in range(min(ys) - 1, max(ys) + 2):
        line = []
        for x in range(min(xs) - 1, max(xs) + 2):
            if x == virus.x and y == virus.y:
                line.append("[")
            else:
                line.append(" ")
            if (x, y) in infections:
                line.append("#")
            else:
                line.append(".")
            if x == virus.x and y == virus.y:
                line.append("]")
            else:
                line.append(" ")
        print("".join(line))
    print("")


if __name__ == "__main__":

    with open("input.txt") as f:
        lines = f.readlines()

    map_x = (len(lines[0]) - 1) // 2
    map_y = (len(lines) - 1) // 2

    infections = dict()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                infections[(x - map_x, y - map_y)] = '#'

    virus = Virus()

    for i in range(0, 10000000):
        # print("Iteration", i)
        # print(virus)
        # print_infections(virus, infections)
        virus.burst(infections)
        if i % 100000 == 0:
            print(f"Progress {int(100 * i / 10000000)}%")

    print("Final")
    print(virus)
    print_infections(virus, infections)
    print(len(infections))
    print(virus.count)
