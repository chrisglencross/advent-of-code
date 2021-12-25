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
            # never assigned so we know it is zero
            return 0
        else:
            return f"{var}_{suffix}"
    else:
        return int(var)

def write_renamed(var):
    var_assignments[var] += 1
    return read_renamed(var)

# Register renaming
instructions = []
for line in lines:
    words = line.split(" ")
    match words:
        case ["inp", arg1]:
            out = write_renamed(arg1)
            instructions.append((out, "inp", write_renamed("inp")))
        case [op, arg1, arg2]:
            in1 = read_renamed(arg1)
            in2 = read_renamed(arg2)
            out = write_renamed(arg1)
            instructions.append((out, op, in1, in2))
        case _:
            raise ValueError(f"Bad command ${line}")

def build_expressions(instructions, register_expressions):

    def get_register_value(var):
        if isinstance(var, int):
            return var
        else:
            return register_expressions.get(var, var)

    for instruction in instructions:
        out, op, *args = instruction
        if op == "inp":
            register_expressions[out] = args[0]
            continue

        arg0 = args[0]
        arg1 = args[1]
        val0 = get_register_value(arg0)
        val1 = get_register_value(arg1)

        p0 = val0 if isinstance(val0, int) else arg0
        p1 = val1 if isinstance(val1, int) else arg1
        register_expressions[out] = op, p0, p1

        # Create a synthetic not-equal instruction
        if op == "eql" and p1 == 0 and (val0, tuple) and val0[0] == "eql":
            register_expressions[out] = "neq", val0[1], val0[2]


def count_register_usage(expressions, reference_count):
    for expression in expressions:
        if isinstance(expression, str):
            reference_count[expression] += 1
        if isinstance(expression, tuple):
            count_register_usage(expression[1:], reference_count)

def simplify(expression, expressions):
    if isinstance(expression, str) and isinstance(expressions.get(expression), int):
        return expressions.get(expression)
    if isinstance(expression, tuple):
        op, *args = expression
        for i, arg in enumerate(args):
            args[i] = simplify(arg, expressions)
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
        return op, *args
    else:
        return expression


def inline_expressions(expressions: dict):

    # Remove common subexpressions
    common_subexpressions = dict()
    for target, expression in expressions.items():
        if expression not in common_subexpressions.keys():
            common_subexpressions[expression] = target

    for target, expression in list(expressions.items()):
        if isinstance(expression, tuple):
            op, *args = expression
            for i, arg in enumerate(args):
                if not isinstance(arg, int):
                    arg_value = expressions.get(arg, arg)
                    common_subexpression = common_subexpressions.get(arg_value)
                    if common_subexpression:
                        args[i] = common_subexpression
            expressions[target] = (op, *args)

    # Inline expressions which contain simple values
    for target, expression in list(expressions.items()):
        if isinstance(expression, str):
            expressions[target] = expressions.get(expression, expression)
        if isinstance(expression, tuple):
            op, *args = expression
            for i, arg in enumerate(args):
                if not isinstance(arg, int):
                    arg_value = expressions.get(arg, arg)
                    if not isinstance(arg_value, tuple):
                        args[i] = arg_value
            expressions[target] = (op, *args)


    # Simplify
    for target, expression in list(expressions.items()):
        simplified_expression = simplify(expression, expressions)
        if simplified_expression != expression:
            expressions[target] = simplified_expression

    # Count how many times each register is used
    reference_count = defaultdict(lambda: 0)
    reference_count[read_renamed("z")] = 1
    count_register_usage(expressions.values(), reference_count)

    # Inline complex expressions which are used only once
    for target, expression in list(expressions.items()):
        if isinstance(expression, tuple):
            op, *args = expression
            for i, arg in enumerate(args):
                if isinstance(arg, str) and reference_count[arg] == 1:
                    arg_value = expressions.get(arg, arg)
                    args[i] = arg_value
            expressions[target] = (op, *args)

    # Count how many times each register is used
    reference_count = defaultdict(lambda: 0)
    reference_count[read_renamed("z")] = 1
    count_register_usage(expressions.values(), reference_count)

    # If register is not used, remove it
    for target, expression in list(expressions.items()):
        if reference_count[target] == 0:
            expressions.pop(target)


register_expressions = {}
build_expressions(instructions, register_expressions)

# These were set by manual inspection
register_expressions.update({
    'x_5': 1,
    'x_11': 1,
    'x_17': 1
})
inline_expressions(register_expressions)
inline_expressions(register_expressions)
inline_expressions(register_expressions)

def print_expression(expression):
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
            return "(" + print_expression(args[0]) + " " + infix_operators[op] + " " + print_expression(args[1]) + ")"
        else:
            return str(op)
    else:
        return str(expression)

for target, expression in register_expressions.items():
    print(f"{target} = {print_expression(expression)}")

