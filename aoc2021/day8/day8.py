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
def find_symbol(symbols, condition):
    return [symbol for symbol in symbols if condition(symbol)][0]


answer = 0
for input_symbols, output_symbols in entries.items():
    s1 = find_symbol(input_symbols, lambda symbol: len(symbol) == 2)
    s4 = find_symbol(input_symbols, lambda symbol: len(symbol) == 4)
    s7 = find_symbol(input_symbols, lambda symbol: len(symbol) == 3)
    s8 = find_symbol(input_symbols, lambda symbol: len(symbol) == 7)
    s3 = find_symbol(input_symbols, lambda symbol: len(symbol) == 5 and len(s1 & symbol) == 2)
    s5 = find_symbol(input_symbols, lambda symbol: len(symbol) == 5 and symbol != s3 and len(s4 & symbol) == 3)
    s2 = find_symbol(input_symbols, lambda symbol: len(symbol) == 5 and len(s4 & symbol) == 2)
    s9 = find_symbol(input_symbols, lambda symbol: len(symbol) == 6 and len(s3 & symbol) == 5)
    s0 = find_symbol(input_symbols, lambda symbol: len(symbol) == 6 and symbol != s9 and len(s1 & symbol) == 2)
    s6 = find_symbol(input_symbols, lambda symbol: len(symbol) == 6 and symbol != s9 and symbol != s0)
    symbols = [(s0, 0), (s1, 1), (s2, 2), (s3, 3), (s4, 4), (s5, 5), (s6, 6), (s7, 7), (s8, 8), (s9, 9)]
    answer += functools.reduce(
        lambda x, s: 10 * x + [value for symbol, value in symbols if symbol == s][0],
        output_symbols, 0)
print(answer)
