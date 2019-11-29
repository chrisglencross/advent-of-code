#!/usr/bin/python3
# Advent of code <YEAR> day <DAY>
# See https://adventofcode.com/<YEAR>/day/<DAY>

import re
from dataclasses import dataclass


@dataclass
class MyClass:
    name: str
    size: int
    properties: dict


if __name__ == "__main__":

    with open("input.txt") as f:
        lines = f.readlines()

    for line in lines:
        match = re.search("^([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)$", line.strip())
        if match:
            field1 = match.group(1)
