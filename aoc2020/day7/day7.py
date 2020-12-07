#!/usr/bin/python3
# Advent of code 2020 day 7
# See https://adventofcode.com/2020/day/7

import re
from functools import lru_cache


def load_rules():
    with open("input.txt") as f:
        lines = f.readlines()
    result = {}
    for line in lines:
        match = re.fullmatch(r"(.*) bags contain (.+)\.", line.strip())
        outer = match.group(1)
        inners = []
        if match.group(2) != "no other bags":
            for s in match.group(2).split(", "):
                contained_match = re.search(r"^(\d+) (.*) bags?$", s)
                inners.append((contained_match.group(2), int(contained_match.group(1))))
        result[outer] = inners
    return result


@lru_cache
def can_contain(outer, target):
    inners = {pair[0] for pair in rules.get(outer)}
    if target in inners:
        return True
    for inner in inners:
        if can_contain(inner, target):
            return True
    return False


@lru_cache
def count_bags(outer):
    return 1+sum([count_bags(pair[0]) * pair[1] for pair in rules.get(outer)])


rules = load_rules()
print(len([outer_bag for outer_bag in rules.keys() if can_contain(outer_bag, "shiny gold")]))
print(count_bags("shiny gold") - 1)
