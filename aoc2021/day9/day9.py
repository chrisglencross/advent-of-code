#!/usr/bin/python3
# Advent of code 2021 day 9
# See https://adventofcode.com/2021/day/9

from aoc2021.modules import grid as g

grid = g.load_grid("input.txt")

# Part 1
risk_value = 0
for coords, value in grid.items():
    neighbour_values = [grid.get(direction.move(coords)) for direction in grid.directions]
    is_lowest = all(neighbour_value > value for neighbour_value in neighbour_values if neighbour_value is not None)
    if is_lowest:
        risk_value += int(value) + 1
print(risk_value)


# Part 2
def flood_fill(grid, coords, points_in_basin: set):
    if coords in points_in_basin:
        return
    points_in_basin.add(coords)
    for direction in grid.directions:
        neighbour_coords = direction.move(coords)
        neighbour_value = grid.get(neighbour_coords)
        if neighbour_value is not None and neighbour_value != '9':
            flood_fill(grid, neighbour_coords, points_in_basin)


all_basins = []
remaining_coords = {coords for coords, value in grid.items() if value != '9'}
while remaining_coords:
    new_basin = set()
    flood_fill(grid, remaining_coords.pop(), new_basin)
    remaining_coords -= new_basin
    all_basins.append(new_basin)

basin_sizes = sorted([len(basin) for basin in all_basins], reverse=True)
print(basin_sizes[0] * basin_sizes[1] * basin_sizes[2])
