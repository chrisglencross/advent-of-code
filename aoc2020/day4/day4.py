#!/usr/bin/python3
# Advent of code 2020 day 4
# See https://adventofcode.com/2020/day/4

import re


def in_range(value, lo, hi):
    try:
        return lo <= int(value) <= hi
    except ValueError:
        return False


def is_valid(passport, strict):
    if not set(passport.keys()).issuperset(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]):
        return False

    if strict:
        if not in_range(passport["byr"], 1920, 2002) or \
                not in_range(passport["iyr"], 2010, 2020) or \
                not in_range(passport["eyr"], 2020, 2030) or \
                not re.fullmatch("#[0-9a-f]{6}", passport["hcl"]) or \
                not re.fullmatch("(amb|blu|brn|gry|grn|hzl|oth)", passport["ecl"]) or \
                not re.fullmatch("[0-9]{9}", passport["pid"]):
            return False

        match = re.fullmatch("([0-9]+)(cm|in)", passport["hgt"])
        if not match or \
                (match.group(2) == "cm" and not in_range(match.group(1), 150, 193)) or \
                (match.group(2) == "in" and not in_range(match.group(1), 59, 76)):
            return False

    return True


def read_passport(block):
    return dict([field.split(":", 2) for line in block.split("\n") for field in line.split(" ")])


def count_valid(strict):
    passports = [read_passport(block) for block in blocks]
    return len([passports for passport in passports if is_valid(passport, strict)])


with open("input.txt") as f:
    blocks = f.read().replace("\r", "").split("\n\n")

print(count_valid(False))
print(count_valid(True))
