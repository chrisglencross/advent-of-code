#!/usr/bin/python3
# Advent of code 2015 day 9
# See https://adventofcode.com/2015/day/9

import itertools
import re

with open("input.txt") as f:
    lines = f.readlines()

places = set()
distances = {}
for line in lines:
    match = re.search("^(.*) to (.*) = (.*)$", line.strip())
    if match:
        place1 = match.group(1)
        place2 = match.group(2)
        distance = int(match.group(3))
        distances[(place1, place2)] = distance
        distances[(place2, place1)] = distance
        places.add(place1)
        places.add(place2)


def get_distance(order):
    total_distance = 0
    for i in range(1, len(order)):
        place1 = order[i - 1]
        place2 = order[i]
        distance = distances[(place1, place2)]
        total_distance += distance
    return total_distance


orders = list(itertools.permutations(places))

best_order = min(orders, key=get_distance)
print(best_order)
print(get_distance(best_order, distances))

best_order = max(orders, key=get_distance)
print(best_order)
print(get_distance(best_order, distances))
