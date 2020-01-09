#!/usr/bin/python3
# Advent of code 2016 day 19
# See https://adventofcode.com/2016/day/19


def find_last_elf(elf_count, part1):
    sorted_elves = []
    for elf in range(1, elf_count + 1):
        sorted_elves.append(elf)
    elf_index = 0
    removed_elves = set()
    while True:

        if elf_index >= len(sorted_elves) // 3 - 1:
            # Compact the list of elves, moving the the current elf to the start
            # Ensures that the elf we will steal from is always after the current elf
            sorted_elves = ([elf for elf in sorted_elves[elf_index:] if elf not in removed_elves] +
                            [elf for elf in sorted_elves[:elf_index] if elf not in removed_elves])
            elf_index = 0
            removed_elves.clear()

        if len(sorted_elves) == 1:
            break

        # Find the next non-removed elf
        while True:
            elf_no = sorted_elves[elf_index]
            if elf_no not in removed_elves:
                break
            elf_index += 1

        if part1:
            target = sorted_elves[elf_index + 1]
        else:
            remaining_elves = len(sorted_elves) - len(removed_elves)
            # Invariant: because of how we do compaction, elf_index is always in the first half of sorted_elves
            # and, for part 2, removed_elves are always in the second half.
            # The index of the next target we remove is after the elves already removed.
            target = sorted_elves[elf_index + remaining_elves // 2 + len(removed_elves)]

        removed_elves.add(target)
        elf_index += 1

    return sorted_elves[0]


print("Part 1:", find_last_elf(3014603, True))
print("Part 2:", find_last_elf(3014603, False))
