#!/usr/bin/python3
# Advent of code 2015 day 7
# See https://adventofcode.com/2015/day/7


with open("input.txt") as f:
    lines = f.readlines()


def get_value(wires, name):
    if name.isnumeric():
        return int(name)
    else:
        return wires.get(name)


wires = {}
wires["b"] = 3176  # Part 2 only

while "a" not in wires:
    for line in lines:
        line = line.strip()
        value = line.split(" -> ")[0]
        assign = line.split(" -> ")[1]
        value = value.split(" ")
        calculated = None
        if len(value) == 1:
            calculated = get_value(wires, value[0])
        elif value[1] == "AND" and get_value(wires, value[0]) is not None and get_value(wires, value[2]) is not None:
            calculated = get_value(wires, value[0]) & get_value(wires, value[2])
        elif value[1] == "OR" and get_value(wires, value[0]) is not None and get_value(wires, value[2]) is not None:
            calculated = get_value(wires, value[0]) | get_value(wires, value[2])
        elif value[1] == "LSHIFT" and get_value(wires, value[0]) is not None:
            calculated = get_value(wires, value[0]) << int(value[2])
        elif value[1] == "RSHIFT" and get_value(wires, value[0]) is not None:
            calculated = get_value(wires, value[0]) >> int(value[2])
        elif value[0] == "NOT" and get_value(wires, value[1]) is not None:
            calculated = ~get_value(wires, value[1])
        if calculated is not None and assign not in wires:
            wires[assign] = calculated

print(wires["a"])
