#!/usr/bin/python3
# Advent of code 2021 day 23
# See https://adventofcode.com/2021/day/23
import bisect

from aoc2021.modules import grid as g

hallway_y = 1
room_xs = {'A': 3, 'B': 5, 'C': 7, 'D': 9}
energies = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


def get_state(grid: g.Grid):
    return tuple(sorted([(cell, tuple(sorted(locations))) for cell, locations in grid.index_repeating_cells().items()]))


def get_navigable_targets(grid, start, targets):
    locations = [start]
    result = []
    visited = set()
    while locations:
        location = locations.pop()
        visited.add(location)
        if location in targets:
            result.append(location)
        for direction in grid.directions:
            new_location = direction.move(location)
            if grid.get(new_location) == '.' and new_location not in visited:
                locations.append(new_location)
    return result


def get_move_energy(source, target, pod_type):
    # Simple because each turn only ever moves once sideways and once vertically
    distance = abs(target[0] - source[0]) + abs(target[1] - source[1])
    return distance * energies[pod_type]


def get_pod_targets(grid, pod, location, hallway_targets, room_targets):

    wrong_pod_in_my_room = any(grid[target] not in [pod, '.'] for target in room_targets)
    if location not in hallway_targets and (location not in room_targets or wrong_pod_in_my_room):
        # can move into hallway if in the wrong room or in our own room blocking an incorrect pod
        targets = get_navigable_targets(grid, location, hallway_targets)
    elif location in hallway_targets and not wrong_pod_in_my_room:
        # can move from hallway to bottom of our own room
        targets = get_navigable_targets(grid, location, room_targets)
        if targets:
            targets = [targets[-1]]
    else:
        targets = []

    return targets


def search(grid: g.Grid, finished_grid: g.Grid):

    # Find coords the pods can walk to
    spaces = [coord for coords in grid.index_repeating_cells('.ABCD').values() for coord in coords]
    hallway_targets = [(x, y) for x, y in spaces if y == hallway_y and x not in room_xs.values()]
    room_targets = dict((pod, [(x, y) for x, y in spaces if y > hallway_y and x == room_xs[pod]]) for pod in 'ABCD')

    finished_state = get_state(finished_grid)

    grids = [(0, grid)]
    visited_states = {}
    while grids:
        total_energy, grid = grids.pop()
        state = get_state(grid)
        if state == finished_state:
            return total_energy
        if state in visited_states and visited_states[state] <= total_energy:
            continue
        visited_states[state] = total_energy

        for pod, locations in grid.index_repeating_cells().items():
            for location in locations:
                for target in get_pod_targets(grid, pod, location, hallway_targets, room_targets[pod]):
                    new_grid = g.Grid(dict(grid.grid))
                    new_grid[location] = '.'
                    new_grid[target] = pod
                    new_energy = total_energy + get_move_energy(location, target, pod)
                    bisect.insort_right(grids, (new_energy, new_grid), key=lambda v: -v[0])


# Part 1
grid = g.load_grid("input.txt")
finished_grid = g.parse_grid("""
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
""".strip())
print(search(grid, finished_grid))

# Part 2
with open("input.txt") as f:
    lines = [line.replace('\n', '') for line in f.readlines()]
    lines.insert(3, "  #D#C#B#A#  ")
    lines.insert(4, "  #D#B#A#C#  ")
grid = g.parse_grid("\n".join(lines))
finished_grid = g.parse_grid("""
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
""".strip())
print(search(grid, finished_grid))
