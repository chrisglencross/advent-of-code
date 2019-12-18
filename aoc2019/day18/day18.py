#!/usr/bin/python3
# Advent of code 2019 day 18
from dataclasses import dataclass
from typing import List, Dict, Tuple

from aoc2019.modules.textgridprinter import TextGridPrinter

DIRECTIONS = {
    "north": (0, -1),
    "east": (1, 0),
    "south": (0, 1),
    "west": (-1, 0),
}

with open("testinput.txt") as f:
    lines = f.readlines()

grid = {}
location = None
target_locations = {}
for y, line in enumerate(lines):
    for x, cell in enumerate(line.strip()):
        grid[(x, y)] = cell
        if cell == "@":
            location = (x, y)
        elif cell.isalpha():
            target_locations[cell] = (x, y)

grid_printer = TextGridPrinter()

# Remove grid contents
grid[location] = "."


def move_location(location, direction_name):
    move = DIRECTIONS[direction_name]
    return location[0] + move[0], location[1] + move[1]


ROUTE_LENGTH_CACHE = dict()


def find_route_lengths(grid, target_locations, start_location):
    cache_key = (tuple(sorted(target_locations.keys())), start_location)
    cached_result = ROUTE_LENGTH_CACHE.get(cache_key)
    if cached_result is not None:
        return cached_result

    # Populate empty grid
    grid = dict(grid)
    for target, target_location in target_locations.items():
        grid[target_location] = target

    route_lengths = {}
    check_neighbours = set()

    route_lengths[start_location] = 0
    check_neighbours.add(start_location)
    while check_neighbours:
        next_check_neighbours = set()
        for location in list(check_neighbours):
            location_distance = route_lengths[location]
            for neighbour in get_neighbours(location[0], location[1]):
                if neighbour in route_lengths.keys():
                    continue
                if grid[neighbour] != ".":
                    continue
                route_lengths[neighbour] = location_distance + 1
                next_check_neighbours.add(neighbour)
        check_neighbours = next_check_neighbours

    ROUTE_LENGTH_CACHE[cache_key] = route_lengths

    return route_lengths


def get_neighbours(x, y):
    result = set()
    for move in DIRECTIONS.values():
        result.add((x + move[0], y + move[1]))
    return result


def get_route_len(target_location, reachable_route_lengths):
    if target_location is None:
        return None
    routes = []
    for neighbour_location in get_neighbours(target_location[0], target_location[1]):
        route_len = reachable_route_lengths.get(neighbour_location)
        if route_len is not None:
            routes.append(route_len + 1)
    if not routes:
        return None
    return min(routes)


@dataclass
class RouteState:
    location: Tuple[int, int]
    route_length: int
    collected_list: List[str]
    target_locations: Dict[str, Tuple[int, int]]

    def get_state_key(self):
        return self.location, tuple(sorted(self.collected_list))


def get_next_route_states(grid, route_state):
    result = []

    reachable_route_lengths = find_route_lengths(grid, route_state.target_locations, route_state.location)

    # Try navigating to all available keys and doors (in alphabetical order just because that's what the AoC samples do)
    for target in sorted(route_state.target_locations.keys()):
        if target.isupper() and target.lower() not in route_state.collected_list:
            # Door for which we do not have the key
            continue
        target_location = route_state.target_locations[target]
        route_len = get_route_len(target_location, reachable_route_lengths)
        if route_len is not None:
            new_target_locations = dict(route_state.target_locations)
            del new_target_locations[target]
            result.append(RouteState(location=target_location,
                                     route_length=route_state.route_length + route_len,
                                     collected_list=route_state.collected_list + [target],
                                     target_locations=new_target_locations))

    return result


def find_all_routes(grid, location, target_locations):
    initial_state = RouteState(location=location, route_length=0, target_locations=target_locations, collected_list=[])
    all_keys = set([target for target in target_locations.keys() if target.islower()])

    best_routes_by_state = {}
    best_routes_by_state[initial_state.get_state_key()] = initial_state

    route_states_to_check = []
    route_states_to_check.append(initial_state)

    best_complete_route_length = None

    iterations = 0
    while route_states_to_check:
        prune_count = 0
        print(f"Iteration {iterations} has {len(route_states_to_check)} active states:")
        route_states_to_check.sort(key=lambda r: r.route_length)
        # for x in route_states_to_check:
        #     print(x.get_state_key(), x.route_length)
        # print()
        iterations += 1
        new_route_states_to_check = []
        for route_state in route_states_to_check:
            next_route_states = get_next_route_states(grid, route_state)
            for next_route_state in next_route_states:
                if best_complete_route_length and next_route_state.route_length >= best_complete_route_length:
                    prune_count += 1
                    continue
                state_key = next_route_state.get_state_key()
                already_found = best_routes_by_state.get(state_key)
                if already_found and already_found.route_length <= next_route_state.route_length:
                    prune_count += 1
                    continue
                best_routes_by_state[state_key] = next_route_state
                new_route_states_to_check.append(next_route_state)

                if all_keys.issubset(next_route_state.collected_list):
                    best_complete_route_length = next_route_state.route_length

        print(f"Pruned {prune_count} next states")
        route_states_to_check = new_route_states_to_check

    complete_routes = []
    for best_route in best_routes_by_state.values():
        if all_keys.issubset(best_route.collected_list):
            complete_routes.append(best_route)
    return complete_routes


empty_grid = dict(grid)
for target_location in target_locations.values():
    empty_grid[target_location] = '.'

results = find_all_routes(empty_grid, location, target_locations)

for result in results:
    print(result.route_length, "".join(result.collected_list))

# 'c', 'e', 'b', 'f', 'a', 'E', 'k', 'd', 'F', 'l', 'h', 'C', 'm', 'g', 'B', 'n', 'G', 'i', 'H', 'p', 'A', 'j', 'D', 'o'
# a, f, b, j, g, n, h, d, l, o, e, p, c, i, k, m
