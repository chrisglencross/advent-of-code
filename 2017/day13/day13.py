#!/usr/bin/python3
# Advent of code 2017 day 13
# See https://adventofcode.com/2017/day/13

import re
from dataclasses import dataclass


@dataclass
class Scanner:
    depth: int
    range: int

    def position_at(self, time):
        time_to_loop = 2 * self.range - 2
        if time_to_loop == 0:
            return 0
        position = time % time_to_loop
        if position >= self.range:
            position = 2 * self.range - position - 2
        return position

    def severity(self):
        return self.depth * self.range


if __name__ == "__main__":

    with open("input.txt") as f:
        lines = f.readlines()

    scanners = []
    for line in lines:
        # depth: range
        match = re.search("^([0-9]+): ([0-9]+)$", line.strip())
        if match:
            scanners.append(Scanner(int(match.group(1)), int(match.group(2))))
        else:
            raise Exception("Cannot parse: " + line)

    # Part 1
    total_severity = 0
    for scanner in scanners:
        if scanner.position_at(scanner.depth) == 0:
            total_severity = total_severity + scanner.severity()
    print(total_severity)

    # Part 2
    for delay in range(1, 100000000):
        failed = False
        for scanner in scanners:
            if scanner.position_at(scanner.depth + delay) == 0:
                failed = True
                break
        if not failed:
            print("Succeeded with delay", delay)
            break
