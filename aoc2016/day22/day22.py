#!/usr/bin/python3
# Advent of code 2016 day 22
# See https://adventofcode.com/2016/day/22

import re
from dataclasses import dataclass
from typing import Tuple, Dict

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

fs_size = {}
fs_used = {}
for line in lines[2:]:
    if match := re.fullmatch(r"/dev/grid/node-x(\d+)-y(\d+) +(\d+)T +(\d+)T +(\d+)T +(\d+)%", line):
        x, y, size, used, avail, percent = match.groups()
        fs_size[(int(x), int(y))] = int(size)
        fs_used[(int(x), int(y))] = int(used)

pairs = [(source_key, target_key)
         for source_key, source_used in fs_used.items()
         for target_key, target_size in fs_size.items()
         if source_key != target_key and 0 < source_used < target_size - fs_used[target_key]]
print("Part 1:", len(pairs))


@dataclass
class State:
    data_addr: Tuple[int, int]
    fs_used: Dict[Tuple[int, int], int]
    free_addr: Tuple[int, int]
    steps: int

    def next_state(self, source_addr, target_addr):
        assert self.fs_used[target_addr] == 0
        if self.fs_used[source_addr] > fs_size[target_addr]:
            return None
        if source_addr == self.data_addr:
            new_data_coords = target_addr
        else:
            new_data_coords = self.data_addr
        new_fs_used = dict(self.fs_used)
        new_fs_used[target_addr] = self.fs_used[source_addr]
        new_fs_used[source_addr] = 0
        return State(new_data_coords, new_fs_used, source_addr, self.steps + 1)

    def print_compact(self):
        max_x = max([x for x, y in self.fs_used.keys()])
        max_y = max([y for x, y in self.fs_used.keys()])
        for y in range(0, max_y + 1):
            line = []
            for x in range(0, max_x + 1):
                brackets = "  "
                if (0, 0) == (x, y):
                    brackets = "()"
                symbol = "."
                if self.data_addr == (x, y):
                    symbol = "G"
                if self.free_addr == (x, y):
                    symbol = "_"
                if self.fs_used[(x, y)] > 400:
                    symbol = "#"
                line.append(f"{brackets[0]}{symbol}{brackets[1]}")
            print("".join(line))
        print()


max_x = max([x for x, y in fs_used.keys() if y == 0])
gaps = [(x, y) for (x, y), used in fs_used.items() if used == 0]
assert len(gaps) == 1
initial_state = State((max_x, 0), dict(fs_used), gaps[0], 0)
initial_state.print_compact()

# The algorithm attempts to move the free space to the cell left of the data we need, then
# swapping to move the data left. To return the free space to the left of the data, move it down, left x 2 and then up.
# Note that this is not a general solution: it is specific to our initial state (see print_compact output) where the
# free space can move almost anywhere except a large horizontal row of immovable blocks, which the space must move left
# to avoid (hence the rule to move left if the space cannot move up)

# First of all attempted this with an exhaustive depth first and breadth-first searches, but too many states to search.
# We quickly run out of memory.

state = initial_state
while state.data_addr != (0, 0):

    left = (state.free_addr[0] - 1, state.free_addr[1])
    right = (state.free_addr[0] + 1, state.free_addr[1])
    up = (state.free_addr[0], state.free_addr[1] - 1)
    down = (state.free_addr[0], state.free_addr[1] + 1)

    if state.free_addr[1] == state.data_addr[1]:
        # Free space is on the same row as the data
        if state.free_addr[0] < state.data_addr[0]:
            # Space is left of the data: move space right towards the data, or swap with it
            next_state = state.next_state(right, state.free_addr)
        else:
            # Space is right of the data: move it down so we can move it to the left of the data and back up
            next_state = state.next_state(down, state.free_addr)

    elif state.free_addr[1] > state.data_addr[1]:
        # Free space is below the data
        if state.free_addr[0] < state.data_addr[0]:
            # Space is below and to the left of the data: move it up
            next_state = state.next_state(up, state.free_addr)
            if next_state is None:
                # The blockage is above the space: move the space left to navigate around it
                next_state = state.next_state(left, state.free_addr)
        else:
            # Space is below and to the right of the data: move it left
            next_state = state.next_state(left, state.free_addr)

    else:
        raise Exception("Unexpected state: free space is above data")

    if next_state is None:
        state.print_compact()
        raise Exception("Algorithm failure: unexpected blockage. Check the map.")

    state = next_state

state.print_compact()
print("Part 2:", state.steps)
