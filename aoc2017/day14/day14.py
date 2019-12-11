#!/usr/bin/python3
# Advent of code 2017 day 14
# See https://adventofcode.com/2017/day/14


def index(loop, i):
    return (i + len(loop)) % len(loop)


def reverse_range(loop, current, length):
    start = index(loop, current)
    end = index(loop, current + length - 1)
    for i in range(0, length // 2):
        t = loop[index(loop, start)]
        loop[index(loop, start)] = loop[index(loop, end)]
        loop[index(loop, end)] = t
        end = index(loop, end - 1)
        start = index(loop, start + 1)
    return loop


def knot_hash(data):
    lengths = [ord(c) for c in data]
    lengths.extend([17, 31, 73, 47, 23])

    length = 256
    loop = list(range(0, length))
    current = 0
    skip_size = 0
    for i in range(0, 64):
        for length in lengths:
            reverse_range(loop, current, length)
            current = current + length + skip_size
            skip_size = skip_size + 1
    dense_hash = []
    for block in range(0, 16):
        a = 0
        for b in range(0, 16):
            a = a ^ loop[block * 16 + b]
        dense_hash.append(a)

    out = ""
    for b in dense_hash:
        out = out + f"{b:02x}"
    return out


hex_to_binary = dict()
for n in range(0, 16):
    hex_to_binary[f"{n:01x}"] = f"{n:04b}"


def print_binary(hex):
    line = []
    for c in hex:
        line.append(hex_to_binary[c])
    return "".join(line)


def flood_fill(lines, groups, y, x, group_id):
    if y > 0 and lines[y - 1][x] == "1" and groups[y - 1][x] is None:
        groups[y - 1][x] = group_id
        flood_fill(lines, groups, y - 1, x, group_id)
    if y < len(lines) - 1 and lines[y + 1][x] == "1" and groups[y + 1][x] is None:
        groups[y + 1][x] = group_id
        flood_fill(lines, groups, y + 1, x, group_id)
    if x > 0 and lines[y][x - 1] == "1" and groups[y][x - 1] is None:
        groups[y][x - 1] = group_id
        flood_fill(lines, groups, y, x - 1, group_id)
    if x < len(lines[0]) - 1 and lines[y][x + 1] == "1" and groups[y][x + 1] is None:
        groups[y][x + 1] = group_id
        flood_fill(lines, groups, y, x + 1, group_id)


if __name__ == "__main__":

    # input = "flqrgnkx"  # test input
    input = "amgozmfv"
    total_used = 0
    lines = []
    for row in range(0, 128):
        hash_value = knot_hash(f"{input}-{row}")
        line = print_binary(hash_value)
        lines.append(line)
        total_used = total_used + sum([1 for block in line if block == "1"])
    print(total_used)

    # Part 2

    # Create empty grid
    groups = []
    for line in lines:
        group = []
        for block in line:
            group.append(None)
        groups.append(group)

    # Flood fill each used block to count groups
    group_id = 0
    for y, line in enumerate(lines):
        for x, block in enumerate(line):
            if block == "1" and groups[y][x] is None:
                flood_fill(lines, groups, y, x, group_id)
                group_id = group_id + 1
    print(group_id)
