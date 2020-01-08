#!/usr/bin/python3
# Advent of code 2016 day 11
# See https://adventofcode.com/2016/day/11
import itertools
import re

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

numbers = {
    "first": 0,
    "second": 1,
    "third": 2,
    "fourth": 3
}

floors = [set() for i in range(0, 4)]
floors[0].add(("lift", "lift"))

for line in lines:
    if match := re.fullmatch(r"The (.*) floor contains (.*)\.", line):
        if match.group(2) == "nothing relevant":
            continue
        floor_no = numbers[match.group(1)]
        for item in re.split(r"(,|\band\b)", match.group(2)):
            item = re.sub("^an? ", "", item.strip()).replace("-compatible", "")
            if item not in ("", ",", "and"):
                floors[floor_no].add(tuple(item.split(" ")))


def move(state, move_to_floor, moves_items):
    result = []
    for floor_no, items in enumerate(state):
        new_floor = set()
        for item in items:
            if item not in moves_items:
                new_floor.add(item)
        for move_item in moves_items:
            if move_to_floor == floor_no:
                new_floor.add(move_item)
        result.append(tuple(sorted(new_floor)))
    return tuple(result)


def is_valid_combination(floor):
    for chem, type in floor:
        if type == "microchip":
            # Microchips cannot be with a generator unless its own generator is included
            generators = [c2 for c2, t2 in floor if t2 == "generator"]
            if generators and chem not in generators:
                return False
    return True


def is_valid(state):
    for floor in state:
        if not is_valid_combination(floor):
            return False
    return True


def get_next_states(state, visited_states):
    next_states = set()

    for i, floor in enumerate(state):
        if ("lift", "lift") in floor:
            floor_no = i

    items = [item for item in state[floor_no] if item != ("lift", "lift")]
    for items_to_move in itertools.chain(itertools.combinations(items, 1), itertools.combinations(items, 2)):

        if not is_valid_combination(items_to_move):
            # Cannot move these two items together
            continue

        for destination_floor in [floor_no - 1, floor_no + 1]:
            if 0 <= destination_floor < len(state):
                next_state = move(state, destination_floor, items_to_move + tuple([("lift", "lift")]))
                if next_state not in visited_states and is_valid(next_state):
                    next_states.add(next_state)
                    visited_states.add(next_state)

    return next_states


def is_finished(states):
    for floors in states:
        if not (floors[0] or floors[1] or floors[2]):
            return True
    return False


# Part 2 only
floors[0].update({
    ("elerium", "generator"),
    ("elerium", "microchip"),
    ("dilithium", "generator"),
    ("dilithium", "microchip")})

count = 0
states = {move(floors, None, [])}
visited_states = set()
while not is_finished(states):
    count += 1
    next_states = set()
    for state in states:
        next_states.update(get_next_states(state, visited_states))
    states = next_states
    print(count, len(states), len(visited_states))
print(count)
