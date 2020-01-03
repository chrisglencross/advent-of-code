#!/usr/bin/python3
# Advent of code 2015 day 13
# See https://adventofcode.com/2015/day/13

import itertools
import re

with open("input.txt") as f:
    lines = f.readlines()

pairs = {}
people = set()
for line in lines:
    match = re.search("^(.*) would (.*) (.*) happiness units by sitting next to (.*).$", line.strip())
    if match:
        name1 = match.group(1)
        lose_gain = match.group(2)
        amount = int(match.group(3))
        if lose_gain == "lose":
            amount = -amount
        name2 = match.group(4)
        pairs[(name1, name2)] = amount
        people.add(name1)
        people.add(name2)


def get_happiness(order, pairs):
    happiness = 0
    prev_person = order[-1]
    for person in order:
        happiness += get_pair_happiness(pairs, person, prev_person)
        happiness += get_pair_happiness(pairs, prev_person, person)
        prev_person = person
    return happiness


def get_pair_happiness(pairs, p1, p2):
    result = pairs.get((p1, p2), 0)
    # print(f"{p1} gains {result} happiness sitting next to {p2}")
    return result


# people.add("*Me*") - part 2
orders = itertools.permutations(people)
best_order = max(orders, key=lambda order: get_happiness(order, pairs))
print(best_order)
print(get_happiness(best_order, pairs))
