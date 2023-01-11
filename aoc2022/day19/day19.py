#!/usr/bin/python3
# Advent of code 2022 day 19
# See https://adventofcode.com/2022/day/19

import re

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

MATERIALS = {
    "ore": ORE,
    "clay": CLAY,
    "obsidian": OBSIDIAN,
    "geode": GEODE
}

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


def can_build_robot(items, item_costs):
    return all(qty >= item_costs[item] for item, qty in enumerate(items))


def build_robot(items, item_costs):
    return (qty - item_costs[item] for item, qty in enumerate(items))


def get_options(robots, items, robot_costs):
    # Build nothing
    next_states = set()
    next_states.add((robots, items))

    # Try building one of each robot that we can afford
    for robot_to_buy, item_costs in enumerate(robot_costs):
        if can_build_robot(items, item_costs):
            next_robots = list(robots)
            next_robots[robot_to_buy] += 1
            next_robots = tuple(next_robots)
            next_state = (
                next_robots,
                build_robot(items, item_costs)
            )
            next_states.add(next_state)

    return next_states


def get_next_states(robot_costs, states):
    next_states = set()
    for robots, items in states:
        next_options = get_options(robots, items, robot_costs)

        # Increment items by the number of robots (but not the ones we just built)
        for next_robots, next_items in next_options:
            next_items = list(next_items)
            for robot_type, robot_qty in enumerate(robots):
                next_items[robot_type] += robot_qty
            next_states.add((
                next_robots,
                tuple(next_items)
            ))

    return next_states


def set_limits(items, item_limits):
    return tuple(min(value, item_limits[item]) for item, value in enumerate(items))

def worse_than_any(items, existing_items):
    for existing_item in existing_items:
        if all(items[i] <= existing_item[i] for i in range(0, 4)):
            return True
    return False

def get_best_costs(robot_costs, minutes):
    states = [((1, 0, 0, 0), (0, 0, 0, 0))]
    for minute in range(0, minutes):
        states = get_next_states(robot_costs, states)

        # Optimisation: discard any states with fewer geodes than the max
        max_geodes = max(items[GEODE] for robots, items in states)
        # states = {(robots, items) for robots, items in states if items[GEODE] == max_geodes}

        # Optimisation: if there are more items of a type than we can possibly use in the remaining time, set to the max
        # This helps deduplicate the number of states
        minutes_remaining = minutes - minute
        item_limits = [0, 0, 0, 10000000]
        for item_costs in robot_costs:
            for item, qty in enumerate(item_costs):
                item_limits[item] = max(item_limits[item], qty * minutes_remaining)
        states = {(robots, set_limits(items, item_limits)) for robots, items in states}

        # Optimisation: If two states have the same robots but all item counts are lower, then it is strictly worse
        # This optimisation does a good job of pruning states, but is slow: O(N^2)
        items_by_robots = {}
        for robots, items in sorted(states, reverse=True):
            existing_robot_items = items_by_robots.get(robots)
            if existing_robot_items is None:
                existing_robot_items = []
                items_by_robots[robots] = existing_robot_items
            if not worse_than_any(items, existing_robot_items):
                existing_robot_items.append(items)
        states = set()
        for robots, all_items in items_by_robots.items():
            for items in all_items:
                states.add((robots, items))

        print(f"After minute {minute}: {max_geodes} geodes opened with {len(states)} states to progress")

    return max_geodes


def parse_blueprint(line):
    blueprint, rest = line.strip('.').split(": ", 2)
    blueprint_no = int(blueprint.split(" ")[1])
    robot_costs = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for cost in rest.split(". "):
        robot, items = re.match("Each (.*) robot costs (.*)", cost).groups()
        for qty, item in [item_qty.split(" ") for item_qty in items.split(" and ")]:
            robot_costs[MATERIALS[robot]][MATERIALS[item]] = int(qty)
    return blueprint_no, robot_costs


# Part 1
answer = 0
for line in lines:
    blueprint_no, robot_costs = parse_blueprint(line)
    print(f"Blueprint {blueprint_no}: {robot_costs}")
    best_cost = get_best_costs(robot_costs, 24)
    print(f"Best cost with blueprint {blueprint_no}: {best_cost}\n")
    answer += best_cost * blueprint_no
print(f"Part 1: {answer}")

# Part 2
answer = 1
for line in lines[0:3]:
    blueprint_no, robot_costs = parse_blueprint(line)
    print(f"Blueprint {blueprint_no}: {robot_costs}")
    best_cost = get_best_costs(robot_costs, 32)
    print(f"Best cost with {blueprint_no}: {best_cost}\n")
    answer *= best_cost
print(f"Part 2: {answer}")
