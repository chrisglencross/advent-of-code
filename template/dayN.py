#!/usr/bin/python3
# Advent of code <YEAR> day <DAY>
# See https://adventofcode.com/<YEAR>/day/<DAY>

import re
from dataclasses import dataclass

with open("testinput.txt") as f:
    lines = [line.strip() for line in f.readlines()]

for line in lines:
    f1, f2 = re.match("^([0-9]+) @ ([0-9]+)$", line)

