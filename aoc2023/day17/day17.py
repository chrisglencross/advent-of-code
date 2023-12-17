#!/usr/bin/python3
# Advent of code 2023 day 17
# See https://adventofcode.com/2023/day/17

from aoc2023.modules import grid as g
from aoc2023.modules.directions import COMPASS_DIRECTIONS

grid = g.load_grid("input.txt")


def solve(min_moves, max_moves):
    start_state = ((0, 0), None, 0)  # state is (coordinates, previous direction, number of moves in that direction)
    lowest_costs = {start_state: 0}
    lowest_end_cost = None

    grid_coords = grid.keys()
    end_coords = (grid.get_width()-1, grid.get_height()-1)

    old_states = [start_state]
    while old_states:
        new_states = []
        for old_state in old_states:
            old_coords, old_dir_name, old_dir_count = old_state
            old_cost = lowest_costs[old_state]
            for new_dir in COMPASS_DIRECTIONS.values():
                new_coords = new_dir.move(old_coords)
                if new_coords not in grid_coords:
                    continue
                if new_dir.reverse_name == old_dir_name:
                    continue
                new_dir_name = new_dir.name
                if old_dir_name and new_dir_name != old_dir_name and old_dir_count < min_moves:
                    continue
                if new_dir_name == old_dir_name and old_dir_count == max_moves:
                    continue
                new_cost = old_cost + int(grid[new_coords])
                if lowest_end_cost is not None and new_cost >= lowest_end_cost:
                    continue
                new_dir_count = old_dir_count+1 if new_dir_name == old_dir_name else 1
                new_state = (new_coords, new_dir_name, new_dir_count)
                existing_cost = lowest_costs.get(new_state)
                if existing_cost and existing_cost <= new_cost:
                    continue
                lowest_costs[new_state] = new_cost
                if new_coords == end_coords and new_dir_count >= min_moves and \
                        (lowest_end_cost is None or new_cost < lowest_end_cost):
                    lowest_end_cost = new_cost

                new_states.append(new_state)
        old_states = new_states
    return lowest_end_cost


print(solve(0, 3))
print(solve(4, 10))
