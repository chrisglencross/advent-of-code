#!/usr/bin/python3
# Advent of code 2015 day 7
# See https://adventofcode.com/2015/day/7

with open("input.txt") as f:
    lines = f.readlines()

exprs = {}
for line in lines:
    line = line.strip()
    left, var = line.split("->", 2)
    expr = left.strip().split(" ")
    exprs[var.strip()] = expr

print(exprs)


def get_value(var, values, exprs):
    if var.isnumeric():
        return int(var)

    if var in values:
        return values[var]
    expr = exprs[var]

    value = None
    if len(expr) == 1:
        value = get_value(expr[0], values, exprs)
    elif len(expr) == 2:
        op = expr[0]
        if op == "NOT":
            value = ~get_value(expr[1], values, exprs)
    elif len(expr) == 3:
        op = expr[1]
        if op == "AND":
            value = get_value(expr[0], values, exprs) & get_value(expr[2], values, exprs)
        elif op == "OR":
            value = get_value(expr[0], values, exprs) | get_value(expr[2], values, exprs)
        elif op == "RSHIFT":
            value = get_value(expr[0], values, exprs) >> int(expr[2])
        elif op == "LSHIFT":
            value = get_value(expr[0], values, exprs) << int(expr[2])

    if value is None:
        raise Exception(f"Unknown operation {expr}")

    value = value % 65536
    values[var] = value

    return value


values = {}
print(get_value("a", values, exprs))

values = {"b": 3176}
print(get_value("a", values, exprs))
