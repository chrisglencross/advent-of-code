#!/usr/bin/python3
# Advent of code 2019 day 4

import itertools

count = 0
for i in range(123257, 647016):
    password = str(i)

    previous_char = None
    increase = True
    for char in password:
        if previous_char is not None:
            if ord(previous_char) > ord(char):
                increase = False
                break
        previous_char = char

    contains_pair = False
    for c, consecutive_chars in itertools.groupby(password):
        if len(list(consecutive_chars)) == 2:  # >=2 for part 1
            contains_pair = True

    if increase and contains_pair:
        count = count + 1

print(count)
