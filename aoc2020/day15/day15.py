#!/usr/bin/python3
# Advent of code 2020 day 15
# See https://adventofcode.com/2020/day/15


def say_number(memory, turn, n):
    previous_turn = memory.get(n, [None, None])[0]
    memory[n] = [turn, previous_turn]


def say_next_number(memory, previous_number, turn):
    t0, t1 = memory[previous_number]
    if t1 is None:
        n = 0
    else:
        n = t0 - t1
    say_number(memory, turn, n)
    return n


def play_game(limit):

    with open("input.txt") as f:
        numbers = [int(n) for n in f.read().split(",")]

    memory = {}

    for turn, n in enumerate(numbers, start=1):
        say_number(memory, turn, n)

    number = numbers[-1]
    for turn in range(len(numbers) + 1, limit + 1):
        number = say_next_number(memory, number, turn)

    print(number)


play_game(2020)
play_game(30000000)

