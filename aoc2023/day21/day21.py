#!/usr/bin/python3
# Advent of code 2023 day 21
# See https://adventofcode.com/2023/day/21
from collections import defaultdict
from itertools import groupby, zip_longest

from aoc2023.modules import grid as g
from aoc2023.modules.directions import COMPASS_DIRECTIONS

grid = g.load_grid("input.txt")
start = grid.find_cell("S")
width, height = grid.get_size()

# Part 1
def find_one_step_from(grid, locations):
    new_locations = set()
    for location in locations:
        for direction in COMPASS_DIRECTIONS.values():
            new_location = direction.move(location)
            cell = grid.get(new_location)
            if cell and cell != "#":
                new_locations.add(new_location)
    return new_locations

def part1():
    locations = {start}
    for i in range(0, 64):
        locations = find_one_step_from(grid, locations)
    print(len(locations))

part1()


# Part 2 -- this code is not at all generic. It is specific to my test input, where there is a periodic cycle of
# 130 or 131 steps before repeating a sequence of steps in a neighbouring grids (depending whether grids are on an
# axis or diagonal. Thos constants were discovered through experimentation and hard-coded, as is the
# 65 steps it takes to reach a diagonal corner from the centre of the starting square. Yuck.

# This is really horrible and took ages to implement. There will be better algorithms!

# Basically we do 400 steps, measure the various periodicities of the repeating cycles and what the grids look like at
# step, then extrapolate from this to a large number of steps.

def find_one_step_from_multi_grids(grid, locations):
    new_locations = {}
    for grid_coords, grid_locations in locations.items():
        for location in grid_locations:
            for direction in COMPASS_DIRECTIONS.values():
                new_x, new_y = direction.move(location)
                grid_x, grid_y = grid_coords
                if new_x < 0:
                    new_x = width - 1
                    grid_x -= 1
                elif new_x >= width:
                    new_x = 0
                    grid_x += 1
                if new_y < 0:
                    new_y = height - 1
                    grid_y -= 1
                elif new_y >= height:
                    new_y = 0
                    grid_y += 1
                new_location = (new_x, new_y)
                cell = grid.get(new_location)
                if cell and cell != "#":
                    new_grid_locations = new_locations.get((grid_x, grid_y))
                    if new_grid_locations is not None:
                        new_grid_locations.add(new_location)
                    else:
                        new_locations[(grid_x, grid_y)] = {new_location}
    return {k: tuple(sorted(v)) for k, v in new_locations.items()}


def get_grid_type(grid_x, grid_y):
    return 1 if grid_x > 0 else -1 if grid_x < 0 else 0, 1 if grid_y > 0 else -1 if grid_y < 0 else 0


def get_start_repeat(grid_type):
    return 130 if grid_type in {(0, 1), (1, 0), (0, -1), (-1, 0)} else 131


# Returns a much smaller age of a grid which is equivalent to the actual age, in terms of the contents of the grid.
# This takes advantage of the repeating cycles.
def get_effective_age(grid_repeat_after_by_type, grid_type, grid_age):
    grid_repeat_after = grid_repeat_after_by_type[grid_type]
    if grid_age < grid_repeat_after + 2:
        return grid_age
    effective_grid_age = (grid_age - grid_repeat_after) % 2 + grid_repeat_after
    return effective_grid_age


def part2():

    locations = {(0, 0): tuple({start})}

    grid_creation_times = {(0, 0): 0}
    grid_states_by_type_and_age = {}
    grid_ages_by_type_and_state = {}
    grid_repeat_after_by_type = {}

    grid_ages_by_type_and_state[((0, 0), tuple({start}))] = 0
    grid_states_by_type_and_age[((0, 0), 0)] = tuple({start})

    for i in range(1, 401):

        grids_created_by_type = defaultdict(lambda: 0)

        new_locations = find_one_step_from_multi_grids(grid, locations)
        for grid_coords, grid_locations in new_locations.items():
            grid_type = get_grid_type(*grid_coords)
            old_grid_locations = locations.get(grid_coords)

            if old_grid_locations is None:
                # This is a new grid
                grids_created_by_type[grid_type] += 1
                grid_creation_times[grid_coords] = i
                grid_states_by_type_and_age[(grid_type, 0)] = grid_locations
                grid_ages_by_type_and_state[(grid_type, grid_locations)] = 0
            else:
                # Check if this grid is repeating itself, and if so record the periodicity of this type of grid
                grid_age = i - grid_creation_times[grid_coords]
                grid_repeat_after = grid_repeat_after_by_type.get(grid_type)
                if grid_repeat_after is None:
                    previous_grid_age = grid_ages_by_type_and_state.get((grid_type, grid_locations))
                    if previous_grid_age is None:
                        grid_ages_by_type_and_state[(grid_type, grid_locations)] = grid_age
                    elif previous_grid_age < grid_age:
                        grid_repeat_after = previous_grid_age
                        grid_repeat_after_by_type[grid_type] = grid_repeat_after
                        print(f"Grid type {grid_type} repeats after {grid_repeat_after} steps (at step number {i})")

                grid_states_by_type_and_age[(grid_type, grid_age)] = grid_locations

        # Log frequency of grid creations. These constants (66, 129, 131) are hard-coded elsewhere.
        if grids_created_by_type:
            print(f"At step {i} the following grid types were created: ", dict(grids_created_by_type))

        locations = new_locations

    STEPS = 26501365
    total = 0
    for grid_type in [(0, 0), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
        for count, age in get_grid_ages_at_iteration(grid_type, STEPS, grid_repeat_after_by_type):
            grid_state = grid_states_by_type_and_age[(grid_type, age)]
            total += (len(grid_state) * count)
    print()
    print(total)


def count_grid_of_type_at_iteration(grid_type, iteration):
    x, y = grid_type
    if x == 0 and y == 0:
        # There's only ever one grid at the origin
        return 1
    elif x == 0 or y == 0:
        # Items along the axis first created at 66, then 1 created every 131
        # 0 at 65, 1 at 66, 1 at 196, 2 at 197
        return 1 + (iteration - 66) // 131
    else:
        # Other items created at 131, then (iteration//131) created every 131
        # 0 at 131, 1 at 132, 1 at 262, 3 at 263
        return (iteration-1) // 131 * (((iteration-1) // 131) + 1) // 2


def get_iterations_since_last_creation(grid_type, iteration):
    """Returns the age of the youngest grids of this type at the iteration"""
    x, y = grid_type
    if x == 0 and y == 0:
        last_creation = 0
        return iteration - last_creation
    elif x == 0 or y == 0:
        last_creation = ((iteration - 66) // 131) * 131 + 66
        if last_creation > iteration:
            last_creation -= 131
        return iteration - last_creation
    else:
        last_creation = ((iteration - 1) // 131) * 131 + 1
        if last_creation > iteration:
            last_creation -= 131
        return iteration - last_creation


def get_grid_ages_at_iteration(grid_type, iteration, grid_repeat_after_by_type):
    generations = []
    for g in range(0, iteration // 131 + 1):
        generation_iteration = iteration - (g * 131)
        if generation_iteration >= 0:
            count = count_grid_of_type_at_iteration(grid_type, generation_iteration)
            if count > 0:
                age = get_iterations_since_last_creation(grid_type, generation_iteration) + (g * 131)
                effective_age = get_effective_age(grid_repeat_after_by_type, grid_type, age)
                generations.append((count, effective_age))
    result = []
    for g1, g2 in zip_longest(generations, generations[1:]):
        if g2 is None:
            result.append(g1)
        else:
            diff = (g1[0] - g2[0])
            if diff > 0:
                result.append((diff, g1[1]))
    return result

part2()