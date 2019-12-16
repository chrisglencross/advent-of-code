#!/usr/bin/python3
# Advent of code 2019 day 16

pattern = [0, 1, 0, -1]


def get_multiplication_factor(output_digit_pos, input_digit_pos):
    """Returns +1, 0, or -1 as the multiplication factor to be applied to a specific input digit, when producing an
    output digit as a sum of factors of input digits. This is effectively looking up a cell from the transformation
    matrix, without actually materializing the matrix into a data structure."""
    index = (input_digit_pos + 1) // (output_digit_pos + 1)
    index = index % len(pattern)
    return pattern[index]


def get_output_digit(input_digits, output_digit_pos):
    output_digit = 0
    for input_digit_pos, input_digit in enumerate(input_digits):
        output_digit += input_digit * get_multiplication_factor(output_digit_pos, input_digit_pos)
    output_digit = abs(output_digit) % 10
    return output_digit


with open("input.txt") as f:
    line = f.readline()

# Part 1, unoptimised
digits = [int(value) for value in line]
for phase in range(100):
    digits = [get_output_digit(digits, digit_pos) for digit_pos in range(len(digits))]
print("".join([str(digit) for digit in digits[0:8]]))

# Part 2 - uses a non-obvious optimisation.
#
# This relies on a pattern from the transformation rules (i.e. multiplier matrix) that:
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
input_digits = [int(value) for value in line] * 10000

for phase in range(100):
    output_digit = 0
    output_digits = [None] * len(input_digits)
    for digit_pos in range(len(output_digits) - 1, offset - 1, -1):
        output_digit += input_digits[digit_pos]  # Multiplication factor for these cells is always 1
        output_digit %= 10
        output_digits[digit_pos] = output_digit
    input_digits = output_digits
print("".join(str(digit) for digit in output_digits[offset:offset + 8]))
