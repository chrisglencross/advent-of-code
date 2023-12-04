#!/usr/bin/python3
# Advent of code 2023 day 3
# See https://adventofcode.com/2023/day/3
import itertools
from aoc2023.modules import grid as g
from aoc2023.modules import directions as d

grid = g.load_grid("input.txt")

# For each digit create index of digit coordinate -> number start coordinate and number value
digits = grid.index_repeating_cells("0123456789")
digit_locations = {l for ls in digits.values() for l in ls}
number_start_locations = {(x, y) for x, y in digit_locations if (x - 1, y) not in digit_locations}
number_locations = {}
for number_start_location in number_start_locations:
    number = 0
    number_digit_locations = []
    location = number_start_location
    while location in digit_locations:
        number_digit_locations.append(location)
        number = 10 * number + int(grid[location])
        location = (location[0]+1, location[1])
    for c in number_digit_locations:
        number_locations[c] = (number_start_location, number)

# Part 1
symbols = grid.index_repeating_cells(not_symbols="0123456789.")
symbol_locations = {l for ls in symbols.values() for l in ls}
symbol_adjacent_locations = {direction.move(symbol)
                             for symbol in symbol_locations
                             for direction in d.COMPASS_DIRECTIONS_8.values()}
symbol_adjacent_numbers = {number_locations[l]
                           for l in symbol_adjacent_locations
                           if l in number_locations}
print(sum([number for location, number in symbol_adjacent_numbers]))

# Part 2
star_locations = grid.find_cells("*")
star_adjacent_locations = [(star, direction.move(star))
                           for star in star_locations
                           for direction in d.COMPASS_DIRECTIONS_8.values()]
star_adjacent_numbers = {(star, number_locations[l])
                         for star, l in star_adjacent_locations
                         if l in number_locations}
numbers_grouped_by_adjacent_star = [[number for star, (location, number) in numbers]
                                    for star, numbers in
                                    itertools.groupby(sorted(star_adjacent_numbers), lambda n: n[0])]
number_pairs = [numbers for numbers in numbers_grouped_by_adjacent_star if len(numbers) == 2]
print(sum(n1 * n2 for n1, n2 in number_pairs))
