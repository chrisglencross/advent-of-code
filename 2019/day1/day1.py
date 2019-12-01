#!/usr/bin/python3
# Advent of code 2019 day 1

with open("input.txt") as f:
    lines = f.readlines()


def get_fuel(mass):
    fuel = mass // 3 - 2
    return max(fuel, 0)


assert get_fuel(100756) == 33583

# Part 1
masses = [int(line) for line in lines]
total_fuel = sum([get_fuel(mass) for mass in masses])
print(total_fuel)


def get_total_fuel(mass):
    total_fuel = 0
    extra_mass = mass
    while extra_mass > 0:
        extra_mass = get_fuel(extra_mass)
        total_fuel = total_fuel + extra_mass
    return total_fuel


assert get_total_fuel(100756) == 50346

# Part 2
total_fuel = sum([get_total_fuel(get_fuel(mass)) for mass in masses])
print(total_fuel)
