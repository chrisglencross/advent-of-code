#!/usr/bin/python3
# Advent of code 2021 day 8
# See https://adventofcode.com/2021/day/8
import functools

with open("input.txt") as f:
    lines = f.readlines()

entries = {}
for line in lines:
    left, right = line.strip().split("|")
    input_symbols = tuple(frozenset(symbol) for symbol in left.strip().split(" "))
    output_symbols = tuple(frozenset(symbol) for symbol in right.strip().split(" "))
    entries[input_symbols] = output_symbols

# Part 1
print(len([1
           for output_symbols in entries.values()
           for symbol in output_symbols
           if len(symbol) in [2, 3, 4, 7]]))


# Part 2
def find(values, condition):
    return next(value for value in values if condition(value))


answer = 0
for input_symbols, output_symbols in entries.items():
    s1 = find(input_symbols, lambda symbol: len(symbol) == 2)
    s4 = find(input_symbols, lambda symbol: len(symbol) == 4)
    s7 = find(input_symbols, lambda symbol: len(symbol) == 3)
    s8 = find(input_symbols, lambda symbol: len(symbol) == 7)
    s3 = find(input_symbols, lambda symbol: len(symbol) == 5 and len(s1 & symbol) == 2)
    s5 = find(input_symbols, lambda symbol: len(symbol) == 5 and symbol != s3 and len(s4 & symbol) == 3)
    s2 = find(input_symbols, lambda symbol: len(symbol) == 5 and len(s4 & symbol) == 2)
    s9 = find(input_symbols, lambda symbol: len(symbol) == 6 and len(s3 & symbol) == 5)
    s0 = find(input_symbols, lambda symbol: len(symbol) == 6 and symbol != s9 and len(s1 & symbol) == 2)
    s6 = find(input_symbols, lambda symbol: len(symbol) == 6 and symbol != s9 and symbol != s0)
    symbol_values = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9]
    answer += functools.reduce(lambda x, s: 10 * x + symbol_values.index(s), output_symbols, 0)
print(answer)
