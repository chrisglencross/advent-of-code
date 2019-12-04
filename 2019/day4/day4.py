#!/usr/bin/python3
# Advent of code 2019 day 4

import itertools

count = 0
for i in range(123257, 647016):
    password = str(i)

    is_sorted = "".join(sorted(password)) == password

    contains_pair = False
    for c, consecutive_chars in itertools.groupby(password):
        if len(list(consecutive_chars)) == 2:  # >=2 for part 1
            contains_pair = True

    if is_sorted and contains_pair:
        count = count + 1

print(count)
