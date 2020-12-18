#!/usr/bin/python3
# Advent of code 2020 day 18
# See https://adventofcode.com/2020/day/18

import re

with open("input.txt") as f:
    lines = f.readlines()


def tokenize(expr):
    return [int(token) if token.isdigit() else token
            for token in re.split(r'([\b ]|[()](?=[\d])|(?=[)]))', expr)
            if token.strip()]


def read_value(tokens, is_part2):
    token = tokens.pop(0)
    if token == "(":
        return tuple([read_expr(tokens, is_part2)])
    elif type(token) is int:
        return token
    else:
        raise Exception(f"Unexpected start of value: {token}")


def read_expr(tokens, is_part2):
    expr = read_value(tokens, is_part2)
    while tokens:
        op = tokens.pop(0)
        if op == ")":
            return expr
        if tokens[0] == "(":
            tokens.pop(0)
            rhs = tuple([read_expr(tokens, is_part2)])
        else:
            rhs = read_value(tokens, is_part2)

        if is_part2 and op == "+" and type(expr) is tuple and len(expr) == 3 and expr[1] == "*":
            # Rearrange: plus has higher precedence than times
            lhs_lhs, lhs_op, lhs_rhs = expr
            expr = lhs_lhs, lhs_op, (lhs_rhs, op, rhs)
        else:
            expr = expr, op, rhs

    return expr


def evaluate(expr):
    if type(expr) is int:
        return expr

    if type(expr) is tuple and len(expr) == 1:
        return evaluate(expr[0])

    lhs, op, rhs = expr
    if op == "+":
        return evaluate(lhs) + evaluate(rhs)
    if op == "*":
        return evaluate(lhs) * evaluate(rhs)

    raise Exception(f"Cannot evaluate {expr}")


def calc(line, is_part2=False):
    expr = read_expr(tokenize(line), is_part2)
    return evaluate(expr)


print(sum([calc(line.strip(), False) for line in lines]))
print(sum([calc(line.strip(), True) for line in lines]))
