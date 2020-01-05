#!/usr/bin/python3
# Advent of code 2015 day 24
# See https://adventofcode.com/2015/day/24
import functools
import itertools


def quantum_entanglement(packages):
    return functools.reduce(lambda x, y: x * y, packages)


def get_passenger_compartment_quantum_entanglement(packages, compartments):
    total_weight = sum(packages)
    compartment_weight = total_weight // compartments

    candidates = []
    for i in range(0, len(packages)):
        if candidates:
            break
        for group in itertools.combinations(packages, i):
            if sum(group) == compartment_weight:
                candidates.append(group)

    passenger_compartment_packages = min(candidates, key=quantum_entanglement)
    return quantum_entanglement(passenger_compartment_packages)


with open("input.txt") as f:
    all_packages = [int(line) for line in f.readlines()]

print("Part 1:", get_passenger_compartment_quantum_entanglement(all_packages, 3))
print("Part 2:", get_passenger_compartment_quantum_entanglement(all_packages, 4))
