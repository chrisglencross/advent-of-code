#!/usr/bin/python3
# Advent of code 2021 day 16
# See https://adventofcode.com/2021/day/16
import functools


with open("input.txt") as f:
    binary = list('{0:b}'.format(int(f.readline().strip(), 16)))
    while not len(binary) % 4 == 0:
        binary.insert(0, '0')


def read_int(binary: list, bits):
    # Not the most efficient way of modelling as a stream, but okay for this
    number = int("".join(binary[0:bits]), 2)
    binary[0:bits] = []
    return number


def read_literal(binary: list):
    result = 0
    more = True
    while more:
        more = read_int(binary, 1) == 1
        result = result * 16 + read_int(binary, 4)
    return result


def read_operator(binary: list):
    values = []
    length_type = read_int(binary, 1)
    if length_type == 0:
        subpackets_len = read_int(binary, 15)
        subpacket_binary = binary[0:subpackets_len]
        binary[0:subpackets_len] = []
        while subpacket_binary:
            values.append(read_packet(subpacket_binary))
    else:
        subpacket_count = read_int(binary, 11)
        for i in range(subpacket_count):
            values.append(read_packet(binary))
    return values


def evaluate(packet_type, values):
    match packet_type:
        case 0:
            return sum(values)
        case 1:
            return functools.reduce(lambda acc, v: acc*v, values, 1)
        case 2:
            return min(values)
        case 3:
            return max(values)
        case 5:
            return 1 if values[0] > values[1] else 0
        case 6:
            return 1 if values[0] < values[1] else 0
        case 7:
            return 1 if values[0] == values[1] else 0
        case _:
            raise ValueError(f"Bad type {type}")


def read_packet(binary: list):
    global total_version
    total_version += read_int(binary, 3)
    packet_type = read_int(binary, 3)
    if packet_type == 4:
        return read_literal(binary)
    else:
        return evaluate(packet_type, read_operator(binary))


total_version = 0
answer = read_packet(binary)

print("Part 1:", total_version)
print("Part 2:", answer)


