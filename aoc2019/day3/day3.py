#!/usr/bin/python3
# Advent of code 2019 day 3

with open("input.txt") as f:
    lines = f.readlines()

wire1 = [(line[0], int(line[1:])) for line in lines[0].split(",")]
wire2 = [(line[0], int(line[1:])) for line in lines[1].split(",")]

directions = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1)
}


def get_path(wire):
    """Returns a dictionary of coordinates where the wire has passed.
    The dictionary key is the coord tuple (x, y); the value is the distance
    along the wire from the start.
    """
    result = dict()
    coords = (0, 0)
    count = 0
    for step in wire:
        direction = directions[step[0]]
        for i in range(0, step[1]):
            coords = (coords[0] + direction[0], coords[1] + direction[1])
            count = count + 1
            result[coords] = count
    return result


# Part 1
w1 = get_path(wire1)
w2 = get_path(wire2)
cross_at = set(w1.keys()).intersection(w2.keys())
min_cross_distance = min([abs(c[0]) + abs(c[1]) for c in cross_at])
print(min_cross_distance)

# Part 2
sums = [w1[coords] + w2[coords] for coords in cross_at]
print(min(sums))
