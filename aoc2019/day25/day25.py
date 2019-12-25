#!/usr/bin/python3
# Advent of code 2019 day 25
import itertools

from aoc2019.modules import intcode

route = "ssseewwnnewnesnnnsswnnswneen"
do_not_collect = ["lava", "magnet", "escape", "photons", "loop"]


def collect(item):
    return not any([item.find(n) >= 0 for n in do_not_collect])


def get_output(program, silent=False):
    message = program.next_ascii_output()
    if message and not silent:
        print(message)
    return message


def read_list(message, header):
    item_pos = message.find(header)
    result = []
    if item_pos >= 0:
        items = message[item_pos:].split("\n")
        for line in items:
            if line.strip() == "":
                break
            if line.startswith("- "):
                result.append(line[2:])
    return result


def run_command(program, command, silent=False):
    if not silent:
        print(">> " + command)
    program.append_ascii_input(command)
    message = get_output(program, silent)
    return message


def play(program):
    get_output(program)
    while not program.is_terminated():
        command = input("> ")
        run_command(program, command)


def follow(program, route):
    message = get_output(program)

    while not program.is_terminated():

        # Take any item in the room
        items = read_list(message, "Items here:")
        for item in items:
            if collect(item):
                run_command(program, "take " + item)

        if not route:
            break

        command = {"n": "north", "e": "east", "s": "south", "w": "west"}[route.pop(0)]
        message = run_command(program, command)


def try_combination(program, items):
    for item in items:
        run_command(program, "take " + item, silent=True)

    message = run_command(program, "west", silent=True)

    if message.find("Alert! Droids on this ship are heavier than the detected value!") >= 0:
        state = "too_light"
    elif message.find("Alert! Droids on this ship are lighter than the detected value!") >= 0:
        state = "too_heavy"
    else:
        state = "success"
        print(message)

    if state != "success":
        for item in items:
            run_command(program, "drop " + item, silent=True)
    return state


def find_security_combination(program, all_items):
    too_heavy_sets = set()
    for i in range(1, len(all_items)):
        for c in itertools.combinations(all_items, i):
            if any([set(c).issuperset(s) for s in too_heavy_sets]):
                print(f"Combination {c} is known to be too heavy")
                continue
            state = try_combination(program, c)
            print(state, c)
            if state == "success":
                return c
            elif state == "too_heavy":
                too_heavy_sets.add(c)


def security_checkpoint(program: intcode.Program):
    get_output(program)

    # Drop all
    message = run_command(program, "inv")
    all_items = read_list(message, "Items in your inventory")
    for item in all_items:
        run_command(program, "drop " + item)

    find_security_combination(program, all_items)


program = intcode.load_file("input.txt")
follow(program, list(route))
security_checkpoint(program)
play(program)
