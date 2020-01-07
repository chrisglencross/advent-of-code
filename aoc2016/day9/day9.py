#!/usr/bin/python3
# Advent of code 2016 day 9
# See https://adventofcode.com/2016/day/9

import re


def get_expanded_length(line, v2=False):
    output_length = 0

    pos = 0
    while match := re.search(r"\((\d+)x(\d+)\)", line[pos:]):

        output_length += match.start()
        match_end = pos + match.end()

        block_len = int(match.group(1))
        repeat_count = int(match.group(2))

        compressed_block = line[match_end:match_end + block_len]
        if v2:
            expanded_block_length = get_expanded_length(compressed_block)
        else:
            # Part 1 has no recursive expansion
            expanded_block_length = len(compressed_block)

        output_length += expanded_block_length * repeat_count
        pos = match_end + block_len

    output_length += len(line) - pos
    return output_length


with open("input.txt") as f:
    line = f.read().strip()

print("Part 1:", get_expanded_length(line, False))
print("Part 2:", get_expanded_length(line, True))
