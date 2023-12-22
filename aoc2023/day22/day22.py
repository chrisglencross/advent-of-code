#!/usr/bin/python3
# Advent of code 2023 day 22
# See https://adventofcode.com/2023/day/22

import re
from collections import defaultdict

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

blocks = []
for line in lines:
    x0, y0, z0, x1, y1, z1 = [int(i)
                              for i in
                              re.match("^([0-9]+),([0-9]+),([0-9]+)~([0-9]+),([0-9]+),([0-9]+)$", line).groups()]
    block = ((x0, y0, z0), (x1, y1, z1))
    blocks.append(block)


# Returns true if this block overlaps with some other blocks in a given dimension
def overlap(block, other_blocks, dimension):
    y0, y1 = block[0][dimension], block[1][dimension]
    result = []
    for other in other_blocks:
        oy0 = other[0][dimension]
        oy1 = other[1][dimension]
        if oy0 <= y0 <= oy1 or oy0 <= y1 <= oy1 or y0 <= oy0 <= y1 or y0 <= oy1 <= y1:
            result.append(other)
    return result


# Returns the top-most blocks from a stack of blocks, and the height
def top_blocks(blocks_below):
    if not blocks_below:
        return 0, []
    max_z_below = max(z for _, (_, _, z) in blocks_below)
    return max_z_below, [other for other in blocks_below if other[1][2] == max_z_below]


# Drops a single block onto a surface below
def drop_block(block, max_z_below):
    (x0, y0, z0), (x1, y1, z1) = block
    new_bottom = max_z_below + 1
    distance_to_fall = z0 - new_bottom
    return (x0, y0, z0 - distance_to_fall), (x1, y1, z1 - distance_to_fall)


def drop_stack(blocks):

    fallen_block_count = 0
    fallen_blocks = []
    blocks_by_support = defaultdict(lambda: set())
    supports_by_block = defaultdict(lambda: set())

    for block in sorted(blocks, key=lambda b: b[0][2]):
        blocks_beneath = fallen_blocks
        blocks_beneath_overlapping_x = overlap(block, blocks_beneath, 0)
        blocks_beneath_overlapping_x_and_y = overlap(block, blocks_beneath_overlapping_x, 1)
        max_z_below, blocks_to_support_this = top_blocks(blocks_beneath_overlapping_x_and_y)
        fallen_block = drop_block(block, max_z_below)
        if fallen_block != block:
            fallen_block_count += 1
        fallen_blocks.append(fallen_block)
        for support in blocks_to_support_this:
            blocks_by_support[support].add(fallen_block)
            supports_by_block[fallen_block].add(support)
    return fallen_blocks, fallen_block_count, blocks_by_support, supports_by_block


# Part 1
def blocks_to_drop(disintegrated_block, blocks_by_support, supports_by_block):
    return sum(1
               for supported in blocks_by_support[disintegrated_block]
               if not (supports_by_block[supported] - {disintegrated_block}))


fallen_blocks, _, blocks_by_support, supports_by_block = drop_stack(blocks)
print(sum(1 for block in fallen_blocks if blocks_to_drop(block, blocks_by_support, supports_by_block) == 0))


# Part 2
# Can be made much faster reusing the supporting/supported indexes we already built, but this
# runs more quickly than I could write that (a couple of minutes) and yesterday took hours to get working
# so I'm not feeling embarrassed about taking the easy option today.
total = 0
for block in fallen_blocks:
    remaining = [other for other in fallen_blocks if other != block]
    _, fallen_block_count, _, _ = drop_stack(remaining)
    total += fallen_block_count
print(total)
