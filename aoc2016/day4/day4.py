#!/usr/bin/python3
# Advent of code 2016 day 4
# See https://adventofcode.com/2016/day/4
import itertools
import re

with open("input.txt") as f:
    lines = f.readlines()


def decode(c, shift):
    if c == "-":
        return " "
    else:
        return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))


real_rooms = {}
for line in lines:
    match = re.search(r"^([-a-z]+)-([0-9]+)\[([a-z]*)\]$", line.strip())
    if match:
        name, sector, expected_checksum = match.groups()
        sector = int(sector)
        counted_letters = []
        for letter, values in itertools.groupby(sorted(name.replace("-", ""))):
            counted_letters.append((letter, len(list(values))))
        counted_letters.sort(key=lambda pair: pair[1], reverse=True)
        actual_checksum = "".join([pair[0] for pair in counted_letters[:5]])
        if actual_checksum == expected_checksum:
            real_rooms[name] = sector
print(sum(real_rooms.values()))

for name, sector in real_rooms.items():
    decoded_name = "".join([decode(c, sector) for c in name])
    prefix = "\t"
    if decoded_name.find("northpole") >= 0:
        prefix = "==>\t"
    print(prefix, decoded_name, sector)
