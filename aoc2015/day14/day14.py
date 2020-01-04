#!/usr/bin/python3
# Advent of code 2015 day 14
# See https://adventofcode.com/2015/day/14

import re
from dataclasses import dataclass


@dataclass
class Reindeer:
    name: str
    speed: int
    active_time: int
    rest_time: int


def distance_after(reindeer, time):
    cycle_time = reindeer.active_time + reindeer.rest_time
    completed_cycles = time // cycle_time
    remaining_active_time = min(time % cycle_time, reindeer.active_time)
    movement_time = completed_cycles * reindeer.active_time + remaining_active_time
    return reindeer.speed * movement_time


with open("input.txt") as f:
    lines = f.readlines()

reindeer = []
for line in lines:
    # Dancer can fly 7 km/s for 20 seconds, but then must rest for 119 seconds.
    match = re.search("^(.*) can fly (.*) km/s for (.*) seconds, but then must rest for (.*) seconds.$", line.strip())
    if match:
        reindeer.append(Reindeer(name=match.group(1),
                                 speed=int(match.group(2)),
                                 active_time=int(match.group(3)),
                                 rest_time=int(match.group(4))))

# Part 1
print(max([distance_after(r, 2503) for r in reindeer]))

# Part 2
scores = dict()
for tick in range(1, 2504):
    max_distance = max([distance_after(r, tick) for r in reindeer])
    for max_reindeer in [r.name for r in reindeer if distance_after(r, tick) == max_distance]:
        scores[max_reindeer] = scores.get(max_reindeer, 0) + 1
print(max(scores.values()))
