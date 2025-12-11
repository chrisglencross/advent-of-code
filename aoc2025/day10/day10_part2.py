#!/usr/bin/python3
# Advent of code 2025 day 10
# See https://adventofcode.com/2025/day/10

import re

import aoc2025.modules as aoc

aoc.download_input("2025", "10")

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

def get_equations(buttons, target_joltages):
    return [
        ({button for button in buttons if joltage_no in button}, target_joltage)
        for joltage_no, target_joltage in enumerate(target_joltages)
    ]

def set_button_presses(equations, button, presses):
    updated_equations = []
    for eq_buttons, eq_presses in equations:
        remaining_buttons = {b for b in eq_buttons if b != button}
        remaining_presses = eq_presses - presses if button in eq_buttons else eq_presses
        updated_equations.append((remaining_buttons, remaining_presses))
    updated_equations.append(({button}, presses))
    return partially_solve(updated_equations)

def is_fully_solved(equations):
    return all(len(eq[0]) == 1 for eq in equations)

def partially_solve(equations):
    simplified = True
    while simplified:
        simplified = False
        for i0, (b0, j0) in enumerate(equations):
            for i1, (b1, j1) in enumerate(equations):
                if i0 != i1 and b1 and b1.issubset(b0):
                    equations[i0] = (b0 - b1, j0 - j1)
                    simplified = True
        equations = [eq for eq in equations if eq[0]]
    return equations

def is_valid_solution(equations, target_joltage):
    joltage = [0] * len(target_joltage)
    for buttons, presses in equations:
        for button in buttons:
            for counter in button:
                joltage[counter] += presses
    return joltage == target_joltage

def get_button_press_range(button, equations):
    result = None
    for eq_buttons, total_presses in equations:
        if button in eq_buttons:
            if len(eq_buttons) == 1:
                return total_presses, total_presses  # Solved the exact value already
            if result is None or result[1] > total_presses:
               result = 0, total_presses
    return result

def find_best_solution(buttons, equations, target_joltage):

    if any(eq[1] < 0 for eq in equations):
        return None  # A value we guessed at caused another value to be calculated as negative

    if is_fully_solved(equations):
        return equations if is_valid_solution(equations, target_joltage) else None

    button, *rest = buttons
    press_range = get_button_press_range(button, equations)
    if press_range:
        possible_solutions = [solution
                              for solution in [find_best_solution(rest, set_button_presses(equations, button, presses), target_joltage)
                                               for presses in range(press_range[1], press_range[0]-1, -1)]
                              if solution]
        if possible_solutions:
            return min(possible_solutions, key=lambda solution: sum(eq[1] for eq in solution))

    return None

def part2():
    result = 0
    for line in lines:
        print(line)
        lights, buttons_str, joltage_str = re.match("^\[(.+)] (\(.+\) )+\{(.+)}$", line).groups()

        buttons = [tuple([int(i) for i in toggle_set_str.split(",")]) for toggle_set_str in buttons_str.strip().replace("(", "").replace(")", "").split(" ")]
        target_joltage = [int(j) for j in joltage_str.split(",")]

        # Equations are ({buttons}, total) where total is the sum of how many times the buttons in that set need to be pressed
        equations = get_equations(buttons, target_joltage)
        equations = partially_solve(equations)

        # Performance: Sort buttons so we'll iterate through unknowns with the lowest target joltage first
        buttons.sort(key=lambda b: min(eq[1] for eq in equations if b in eq[0]))
        solution = find_best_solution(buttons, equations, target_joltage)
        result += sum(eq[1] for eq in solution)

    return result

print(part2())
