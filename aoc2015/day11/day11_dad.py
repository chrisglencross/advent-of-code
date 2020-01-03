#!/usr/bin/python3
# Advent of code 2015 day 11
# See https://adventofcode.com/2015/day/11

import re


def increment(password):
    password = list(password)
    for i in range(len(password) - 1, -1, -1):
        if password[i] != 'z':
            n = chr(1 + ord(password[i]))
            password[i] = n
            break
        password[i] = 'a'
    return "".join(password)


def is_valid(password):
    has_sequence = False
    for i in range(0, len(password) - 2):
        if ord(password[i]) + 1 == ord(password[i + 1]) and ord(password[i]) + 2 == ord(password[i + 2]):
            has_sequence = True
            break
    if not has_sequence:
        return False

    if not {'i', 'o', 'l'}.isdisjoint(password):
        return False

    pairs = set()
    m = re.findall("(.)\\1", password)
    pairs.update(m)
    if len(pairs) < 2:
        return False
    return True


def next_valid(password):
    while True:
        password = increment(password)
        if is_valid(password):
            return password


password = "hxbxwxba"
password = next_valid(password)
print(password)
password = next_valid(password)
print(password)
