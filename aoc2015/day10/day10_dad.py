#!/usr/bin/python3
# Advent of code 2015 day 10
# See https://adventofcode.com/2015/day/10


def next_sequence(value):
    in_seq = list(reversed(value))
    out_seq = list()
    while in_seq:
        char = in_seq.pop()
        count = 1
        while in_seq and in_seq[-1] == char:
            in_seq.pop()
            count += 1
        out_seq.extend([str(count), char])
    return "".join(out_seq)


assert next_sequence("1") == "11"
assert next_sequence("11") == "21"
assert next_sequence("21") == "1211"
assert next_sequence("1211") == "111221"
assert next_sequence("111221") == "312211"

value = "1321131112"
for i in range(0, 40):
    value = next_sequence(value)
print(len(value))

value = "1321131112"
for i in range(0, 50):
    value = next_sequence(value)
print(len(value))
