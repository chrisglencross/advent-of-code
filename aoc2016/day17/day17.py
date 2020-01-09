#!/usr/bin/python3
# Advent of code 2016 day 17
# See https://adventofcode.com/2016/day/17
import binascii
import hashlib

PASSCODE = "qljzarfv"
DIRECTIONS = [
    ("U", 0, -1),
    ("D", 0, 1),
    ("L", -1, 0),
    ("R", 1, 0)
]


def make_md5(data):
    data = data.encode()
    m = hashlib.md5()
    m.update(data)
    data = binascii.hexlify(m.digest())
    return data.decode()


def get_next_paths(x, y, route):
    next_paths = []
    for dir_no, door_state in enumerate(make_md5(PASSCODE + route)[:4]):
        if door_state in "bcdef":
            c, dx, dy = DIRECTIONS[dir_no]
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x <= 3 and 0 <= new_y <= 3:
                next_paths.append(((x + dx, y + dy), route + c))
    return next_paths


def find_paths():
    result = []
    paths = [((0, 0), "")]
    while paths:
        next_paths = []
        for (x, y), route in paths:
            if (x, y) == (3, 3):
                result.append(route)
            else:
                next_paths.extend(get_next_paths(x, y, route))
        paths = next_paths
    return result


paths = find_paths()
print("Part 1:", paths[0])
print("Part 2:", len(paths[-1]))
