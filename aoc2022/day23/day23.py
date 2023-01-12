#!/usr/bin/python3
# Advent of code 2022 day 23
# See https://adventofcode.com/2022/day/23
import itertools

import aoc2022.modules.grid as g
import aoc2022.modules.directions as d

grid = g.load_grid("input.txt")
elves = set(grid.find_cells("#"))

direction_checks = {
    "N": {"NE", "N", "NW"},
    "E": {"NE", "E", "SE"},
    "S": {"SE", "S", "SW"},
    "W": {"SW", "W", "NW"},
}
order = ["N", "S", "W", "E"]

for i in itertools.count(0):

    if i == 10:
        grid = g.Grid({elf: "#" for elf in elves})
        print("Part 1:", grid.get_width() * grid.get_height() - len(grid.find_cells("#")))

    elf_targets = {}
    for elf in elves:
        elf_targets[elf] = elf
        neighbours = {dir.name for dir in d.COMPASS_DIRECTIONS_8.values() if dir.move(elf) in elves}
        if neighbours:
            move_dir = [dir
                        for dir in [order[dir_no % 4] for dir_no in range(i, i+4)]
                        if not any(neighbour_check in neighbours for neighbour_check in direction_checks[dir])]
            if move_dir:
                target = d.COMPASS_DIRECTIONS_8[move_dir[0]].move(elf)
                elf_targets[elf] = target

    targets_list = list(elf_targets.values())
    dupe_targets = {target for target in targets_list if targets_list.count(target) > 1}
    new_elves = {elf_targets[elf] if elf_targets[elf] not in dupe_targets else elf for elf in elves}

    if elves == new_elves:
        print("Part 2:", i+1)
        break

    elves = new_elves
