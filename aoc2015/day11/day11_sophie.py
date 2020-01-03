#!/usr/bin/python3
# Advent of code 2015 day 11
# See https://adventofcode.com/2015/day/11

def increment(password):
    while True:
        last = ord(password[-1])
        if last != 122:
            last += 1
            last = chr(last)
            password[-1] = last
            return password
        else:
            password[-1] = "a"


password = ["h", "x", "b", "x", "w", "x", "b", "a"]
valid = False

while not valid:
    password = increment(password)
    for pos, char in enumerate(password):
        pass  # FIXME - not finished yet
