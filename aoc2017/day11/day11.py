#!/usr/bin/python3
# Advent of code 2017 day 11
# See https://adventofcode.com/2017/day/11

# Hex grid can be represented as a square grid where you move n/s two squares at a time
# or diagonally one square at a time.
dirs = {
    "n": (0, -2),
    "ne": (1, -1),
    "se": (1, 1),
    "s": (0, 2),
    "sw": (-1, 1),
    "nw": (-1, -1)
}


def distance(x, y):
    """Distance from origin."""
    if abs(x) >= abs(y):
        return abs(x)  # Diagonal moves allow us to get to the correct y coordinate with no n/s steps
    else:
        return abs(x) + (abs(y) - abs(x)) / 2  # Diagonal move to the correct x coordinate, then 2 at a time n/s


if __name__ == "__main__":

    with open("input.txt") as f:
        lines = f.readlines()

    max_distance = 0
    for line in lines:
        coords = (0, 0)
        for dir in line.strip().split(","):
            move = dirs[dir]
            coords = (coords[0] + move[0], coords[1] + move[1])
            max_distance = max(max_distance, distance(*coords))
        print(distance(*coords))
        print(max_distance)
