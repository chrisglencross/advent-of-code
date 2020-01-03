#!/usr/bin/python3
# Advent of code 2015 day 10
# See https://adventofcode.com/2015/day/10


value = [1, 3, 2, 1, 1, 3, 1, 1, 1, 2]

for i in range(50):
    new_value = []
    pos = 0
    while pos < len(value):
        c = value[pos]
        if len(value) == pos + 1 or c != value[pos + 1]:
            new_value.append(1)
            new_value.append(c)
            pos += 1
        elif len(value) == pos + 2 or c == value[pos + 1] and c != value[pos + 2]:
            new_value.append(2)
            new_value.append(c)
            pos += 2
        elif c == value[pos + 1] and c == value[pos + 2]:
            new_value.append(3)
            new_value.append(c)
            pos += 3
        else:
            raise Exception("Boom!")
    value = new_value

print(value)
print(len(value))
