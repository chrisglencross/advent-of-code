#!/usr/bin/python3
# Advent of code 2020 day 14
# See https://adventofcode.com/2020/day/14
import re

with open("input.txt") as f:
    lines = f.readlines()


def load_mask(mask):
    mask_or = 0
    mask_and = pow(2, 36)-1
    for i, c in enumerate(reversed(mask)):
        bit = pow(2, i)
        if c == '0':
            mask_and -= bit
        elif c == '1':
            mask_or += bit
    return mask_or, mask_and


def part1():
    mask = load_mask('X' * 36)
    memory = {}
    for line in lines:
        match1 = re.fullmatch(r"mask = (.*)", line.strip())
        match2 = re.fullmatch(r"mem\[(\d+)] = (\d+)", line.strip())
        if match1:
            mask = load_mask(match1.group(1))
        elif match2:
            addr, val = match2.groups()
            masked_val = (int(val) | mask[0]) & mask[1]
            memory[addr] = masked_val

    print(sum(memory.values()))


def list_values(value, mask):
    results = []
    result_count = pow(2, len([c for c in mask if c == 'X']))
    for i in range(0, result_count):
        x_bit = 0
        result = []
        for bit in range(0, len(value)):
            digit = '0'
            if mask[bit] == 'X':
                if i & pow(2, x_bit):
                    digit = '1'
                x_bit += 1
            elif value[bit] == '1' or mask[bit] == '1':
                digit = '1'
            result.append(digit)
        results.append("".join(result))

    return results


def part2():
    mask = 'X' * 36
    memory = {}
    for line in lines:
        match1 = re.fullmatch(r"mask = (.*)", line.strip())
        match2 = re.fullmatch(r"mem\[(\d+)] = (\d+)", line.strip())
        if match1:
            mask = match1.group(1)
        elif match2:
            addr, val = match2.groups()
            binary_addr = format(int(addr), "036b")
            masked_addrs = list_values(binary_addr, mask)
            for masked_addr in masked_addrs:
                memory[masked_addr] = int(val)

    print(sum(memory.values()))


part1()
part2()
