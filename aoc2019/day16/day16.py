#!/usr/bin/python3
# Advent of code 2019 day 16

pattern = [0, 1, 0, -1]


def pattern_element(digit_pos, term_num):
    """Returns +1, 0, or -1 as the multiplication factor from the pattern, for the 'term_num'-th term
    of the 'digit_pos'-th digit"""
    index = (term_num + 1) // (digit_pos + 1)
    index = index % len(pattern)
    return pattern[index]


def get_output_digit(values, digit_pos):
    result = 0
    for term, value in enumerate(values):
        result += value * pattern_element(digit_pos, term)
    result = abs(result) % 10
    return result


with open("input.txt") as f:
    line = f.readline()

# Part 1, unoptimised
values = [int(value) for value in line]
for phase in range(100):
    values = [get_output_digit(values, digit_pos) for digit_pos in range(len(values))]
print("".join([str(value) for value in values[0:8]]))

# Part 2 - uses a non-obvious optimisation.
#
# This relies on pattern from the transformation rules that:
#   a) the final digit value of the output is the same as the final digit of the input.
#   b) the preceding digit of the output is the digit just calculated (i.e for the next digit), plus the digit of the
#      input in the corresponding position, *for all digits in the second half of the output only*. (It's more
#      complicated for the first half of the digits.)
#  That is, to calculate the Nth digit of output, you do not need to look at any digits prior to the Nth
#  digit of input. Also, fortunately:
#   c) the digits that we are interested in, specified by our offset (5977341-5977348), are in the second half of the
#      input. This may not be true for everyone's unique input.
#
# This probably clear if you look at the examples from Part 1 of the problem description. For the last 4 digits of
# output the multiplication matrix factors are: ((1, 1, 1, 1), (0, 1, 1, 1), (0, 0, 1, 1), (0, 0, 0, 1)).

offset = int(line[0:7])
values = [int(value) for value in line] * 10000

for phase in range(100):
    digit_value = 0
    new_values = [None] * len(values)
    for digit_pos in range(len(values) - 1, offset - 1, -1):
        digit_value += (values[digit_pos]) % 10
        digit_value %= 10
        new_values[digit_pos] = digit_value
    values = new_values
print("".join(str(value) for value in values[offset:(offset + 8)]))
