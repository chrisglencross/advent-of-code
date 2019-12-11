#!/usr/bin/python3
# Advent of code 2017 day 21
# See https://adventofcode.com/2017/day/21

import re
from math import sqrt


def rotate2(i):
    return "".join(i[2] + i[0] + i[3] + i[1])


def flip2(i):
    return "".join(i[1] + i[0] + i[3] + i[2])


def rotate3(i):
    return "".join(i[6] + i[3] + i[0] + i[7] + i[4] + i[1] + i[8] + i[5] + i[2])


def flip3(i):
    return "".join(i[2] + i[1] + i[0] + i[5] + i[4] + i[3] + i[8] + i[7] + i[6])


def rotate(i):
    if len(i) == 4:
        return rotate2(i)
    elif len(i) == 9:
        return rotate3(i)
    else:
        raise Exception("Bad chunk size")


def flip(i):
    if len(i) == 4:
        return flip2(i)
    elif len(i) == 9:
        return flip3(i)
    else:
        raise Exception("Bad chunk size")


assert rotate2("ABCD") == "CADB"
assert rotate3("ABCDEFGHI") == "GDAHEBIFC"
assert flip2("ABCD") == "BADC"
assert flip3("ABCDEFGHI") == "CBAFEDIHG"


def get_row_size(grid_len):
    return int(sqrt(grid_len))


def get_chunk_size(row_size):
    if row_size % 2 == 0:
        return 2
    elif row_size % 3 == 0:
        return 3
    else:
        raise Exception(f"Unsupported grid size {row_size}")


def get_grid_index(grid_len, chunk_size, chunk_x, chunk_y, x, y):
    row_size = get_row_size(grid_len)
    cy = chunk_y * chunk_size
    cx = chunk_x * chunk_size
    return (cy + y) * row_size + (cx + x)


def chunk(grid):
    row_size = get_row_size(len(grid))
    chunk_size = get_chunk_size(row_size)
    chunks = []
    for chunk_y in range(0, row_size // chunk_size):
        for chunk_x in range(0, row_size // chunk_size):
            chunk = []
            for y in range(0, chunk_size):
                for x in range(0, chunk_size):
                    chunk.append(grid[get_grid_index(len(grid), chunk_size, chunk_x, chunk_y, x, y)])
            chunks.append("".join(chunk))
    return chunks


def replace_chunk(chunk, rules):
    for r in range(0, 4):
        replacement = rules.get(chunk)
        if replacement is not None:
            return replacement
        flipped = flip(chunk)
        # print(f"Flipped {chunk} to {flipped}")
        replacement = rules.get(flipped)
        if replacement is not None:
            return replacement

        # Flip on h axis by rotating, flipping then rotating back again (270 degrees)
        flipped = rotate(rotate(rotate(flip(rotate(chunk)))))
        replacement = rules.get(flipped)
        if replacement is not None:
            return replacement

        rotated = rotate(chunk)
        # print(f"Rotated {chunk} to {rotated}")
        chunk = rotated

    raise Exception("No replacement rule found for chunk " + chunk)


assert chunk("ABCDEFGHIJKLMNOP") == ["ABEF", "CDGH", "IJMN", "KLOP"]


def build_grid(chunks):
    grid_len = sum([len(chunk) for chunk in chunks])
    row_size = get_row_size(grid_len)
    chunk_size = int(sqrt(len(chunks[0])))
    chunk_row_count = row_size // chunk_size

    grid = [None] * grid_len
    for chunk_y in range(0, row_size // chunk_size):
        for chunk_x in range(0, row_size // chunk_size):
            for y in range(0, chunk_size):
                for x in range(0, chunk_size):
                    grid_index = get_grid_index(len(grid), chunk_size, chunk_x, chunk_y, x, y)
                    grid[grid_index] = chunks[chunk_row_count * chunk_y + chunk_x][y * chunk_size + x]

    return "".join(grid)


assert build_grid(["ABEF", "CDGH", "IJMN", "KLOP"]) == "ABCDEFGHIJKLMNOP"

with open("input.txt") as f:
    lines = f.readlines()

rules = {}
for line in lines:
    line = line.replace("/", "")
    # .#/..#/##. => ..../..#./####/..##
    match = re.search("^(.*) => (.*)$", line.strip())
    if not match:
        raise Exception("Cannot parse " + line)
    rules[match.group(1)] = match.group(2)

grid = ".#...####"
for i in range(0, 18):
    chunks = chunk(grid)
    new_chunks = []
    for c in chunks:
        new_chunk = replace_chunk(c, rules)
        new_chunks.append(new_chunk)
    grid = build_grid(new_chunks)

print(sum([1 for c in grid if c == "#"]))
