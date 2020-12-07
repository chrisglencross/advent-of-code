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
        if match.group(2) == "no other bags":
            result[outer] = []
        else:
            result[outer] = [
                (m.group(2), int(m.group(1)))
                for m in [re.fullmatch(r"(\d+) (.*) bags?", s) for s in match.group(2).split(", ")]
            ]
    return result


@lru_cache
def can_contain(outer, target):
    inner_colours = {pair[0] for pair in rules.get(outer)}
    return target in inner_colours or any([can_contain(inner, target) for inner in inner_colours])


@lru_cache
def count_bags(outer):
    return 1+sum([count_bags(inner) * qty for inner, qty in rules.get(outer)])


rules = load_rules()
print(len([outer_bag for outer_bag in rules.keys() if can_contain(outer_bag, "shiny gold")]))
print(count_bags("shiny gold") - 1)
