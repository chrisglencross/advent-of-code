#!/usr/bin/python3
# Advent of code 2025 day 10
# See https://adventofcode.com/2025/day/10

import re

import aoc2025.modules as aoc

aoc.download_input("2025", "10")

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

def simplify_equations(equations):
    result = list(equations)
    more = True
    while more:
        more = False
        for i0, (c0, r0) in enumerate(list(result)):
            for i1, (c1, r1) in enumerate(result):
                if i0 != i1 and c1 and c1.issubset(c0):
                    cs = c0 - c1
                    rs = r0 - r1
                    result[i0] = (cs, rs)
                    more = True
    return [(c, r) for c, r in result if c]

def substitute_equations(equations, known_button_presses):
    substituted = []
    for eq_buttons, total_presses in equations:
        unknown_buttons = {b for b in eq_buttons if b not in known_button_presses.keys()}
        known_presses = sum(kv for kb, kv in known_button_presses.items() if kb in eq_buttons)
        remaining_presses = total_presses - known_presses
        if unknown_buttons:
            substituted.append((unknown_buttons, remaining_presses))
    for button, presses in known_button_presses.items():
        substituted.append(({button}, presses))
    return simplify_equations(substituted)

def get_possible_presses(button, equations):
    min_result = None
    for eq_buttons, total_presses in equations:
        if button in eq_buttons:
            if len(eq_buttons) == 1:
                return total_presses, total_presses
            if min_result is None or min_result > total_presses:
                min_result = total_presses
    return min_result, 1

def is_fully_substituted(equations):
    return all(len(eq[0]) == 1 for eq in equations)

def is_correct_solution(equations, target_joltage):
    joltage = [0] * len(target_joltage)
    for buttons, presses in equations:
        for button in buttons:
            for counter in button:
                joltage[counter] += presses
    return joltage == target_joltage

def solve(buttons, equations, depth, target_joltage):

    if any(eq[1] < 0 for eq in equations):
        return None

    if is_fully_substituted(equations):
        if is_correct_solution(equations, target_joltage):
            return equations
        else:
            return None

    button = buttons[0]
    rest = buttons[1:]
    max_presses, min_presses = get_possible_presses(button, equations)
    if max_presses is not None:
        best_solution_equation = None
        best_solution_presses = None
        for presses in range(max_presses, min_presses-1, -1):
            next_equations = substitute_equations(equations, {button: presses})
            solution_equation = solve(rest, next_equations, depth+1, target_joltage)
            if solution_equation is not None:
                solution_presses = sum(eq[1] for eq in solution_equation)
                if best_solution_presses is None or solution_presses < best_solution_presses:
                    best_solution_presses = solution_presses
                    best_solution_equation = solution_equation
        return best_solution_equation

    return None


def get_equations(buttons, target_joltages):
    result = []
    for i, target_joltage in enumerate(target_joltages):
        one_coefficients = set()
        for button_no, button in enumerate(buttons):
            if i in button:
                one_coefficients.add(button_no)
        result.append((one_coefficients, target_joltage))
    return [({buttons[button_id] for button_id in c}, r) for c, r in result if c]


part2 = 0
for line in lines:
    lights, buttons_str, joltage_str = re.match("^\[(.+)] (\(.+\) )+\{(.+)}$", line).groups()

    buttons = [tuple([int(i) for i in toggle_set_str.split(",")]) for toggle_set_str in buttons_str.strip().replace("(", "").replace(")", "").split(" ")]
    target_joltage = [int(j) for j in joltage_str.split(",")]

    # Equations are (c0 + c1 + cN) = total where cN is the number of button pushes of button index N
    # Simplify simultaneous equations to find some known values of cN
    equations = get_equations(buttons, target_joltage)
    equations = simplify_equations(equations)

    buttons.sort(key=lambda b: min((eq[1], 0-len(b)) for eq in equations if b in eq[0]))
    solution = solve(buttons, equations, 0, target_joltage)
    presses = sum(eq[1] for eq in solution)
    print(f"  => Solution is {presses} presses: {solution}")
    part2 += presses

print(part2)
