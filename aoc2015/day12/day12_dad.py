#!/usr/bin/python3
# Advent of code 2015 day 12
# See https://adventofcode.com/2015/day/12

import json


def get_total(data):
    if type(data) is int:
        return data
    elif type(data) is dict:
        if "red" in data.values():  # Part 2 only
            return 0
        return get_total(list(data.values()))
    elif type(data) is list:
        return sum([get_total(item) for item in data])
    elif type(data) is str:
        return 0
    else:
        raise Exception(f"Unsupported type {type(data)}: {data}")


with open("input.txt") as f:
    data = json.load(f)

print(get_total(data))
