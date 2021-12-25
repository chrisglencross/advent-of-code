#!/usr/bin/python3
# Advent of code 2021 day 24
# See https://adventofcode.com/2021/day/24

from collections import defaultdict

# This is a decompiler of the input.txt assembly language to convert
# the code to Python, which I can then read and run through a debugger

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

var_assignments = {"w": -1, "x": -1, "y": -1, "z": -1, "inp": -1}


def read_renamed(var):
    if var in var_assignments.keys():
        suffix = var_assignments[var]
        if suffix < 0:
            # never assigned so we know it is literal zero
            return 0
        else:
            return f"{var}_{suffix}"
    else:
        return int(var)


def write_renamed(var):
    var_assignments[var] += 1
    return read_renamed(var)


def load_simple_expressions(lines):
    # Load instructions with register renaming for clarity
    expressions = {}
    for line in lines:
        words = line.split(" ")
        match words:
            case ["inp", arg1]:
                out = write_renamed(arg1)
                expressions[out] = write_renamed("inp")
            case [op, arg1, arg2]:
                in1 = read_renamed(arg1)
                in2 = read_renamed(arg2)
                out = write_renamed(arg1)
                expressions[out] = op, in1, in2
            case _:
                raise ValueError(f"Bad command ${line}")
    return expressions


def count_register_usage(expressions, reference_count=None):
    if reference_count is None:
        reference_count = defaultdict(lambda: 0)
        reference_count[read_renamed("z")] = 1  # the output register is used
    for expression in expressions:
        if isinstance(expression, str):
            reference_count[expression] += 1
        if isinstance(expression, tuple):
            count_register_usage(expression[1:], reference_count)
    return reference_count


def simplify_expression(expression, expressions):

    # Inline atomic values
    if isinstance(expression, str) and expression in expressions and not isinstance(expressions.get(expression), tuple):
        return expressions[expression]

    # Simplify expressions involving constants
    if isinstance(expression, tuple):
        op, *args = expression
        for i, arg in enumerate(args):
            args[i] = simplify_expression(arg, expressions)
        if all(isinstance(arg, int) for arg in args):
            if op == 'mul':
                return args[0] * args[1]
            if op == 'add':
                return args[0] + args[1]
            if op == 'mod':
                return args[0] % args[1]
        if op in ["mul", "div", "mod"] and args[0] == 0:
            return 0
        if op == "mul" and args[1] == 0:
            return 0
        if op == "mul" and args[1] == 1:
            return args[0]
        if op == "div" and args[1] == 1:
            return args[0]
        if op == "add" and args[0] == 0:
            return args[1]
        if op == "add" and args[1] == 0:
            return args[0]
        if op == "eql" and args[1] == 0 and isinstance(args[0], tuple) and args[0][0] == 'eql':
            return 'neq', args[0][1], args[0][2]
        return op, *args
    else:
        return expression


def simplify_expressions(expressions: dict):

    # Simplify each expression individually
    for target, expression in list(expressions.items()):
        simplified_expression = simplify_expression(expression, expressions)
        if simplified_expression != expression:
            expressions[target] = simplified_expression

    # Inline complex expressions which are used only once
    reference_count = count_register_usage(expressions.values())
    for target, expression in list(expressions.items()):
        if isinstance(expression, tuple):
            op, *args = expression
            for i, arg in enumerate(args):
                if isinstance(arg, str) and reference_count[arg] == 1:
                    arg_value = expressions.get(arg, arg)
                    args[i] = arg_value
            expressions[target] = (op, *args)

    # If register is no longer used because it has been inlined, remove it
    reference_count = count_register_usage(expressions.values())
    for target, expression in list(expressions.items()):
        if reference_count[target] == 0:
            expressions.pop(target)


def print_expression_as_python(expression):
    if isinstance(expression, tuple):
        op, *args = expression
        infix_operators = {
            "eql": "==",
            "neq": "!=",
            "mul": "*",
            "add": "+",
            "div": "//",
            "mod": "%"
        }
        if op in infix_operators.keys():
            return "(" + print_expression_as_python(args[0]) + " " + infix_operators[op] + " " + print_expression_as_python(args[1]) + ")"
        else:
            return str(op)
    else:
        return str(expression)


# Load simple expressions and turn into a small number of expression trees
expressions = load_simple_expressions(lines)
while True:
    expression_count = len(expressions)
    simplify_expressions(expressions)
    if len(expressions) == expression_count:
        break

for target, expression in expressions.items():
    print(f"{target} = {print_expression_as_python(expression)}")

