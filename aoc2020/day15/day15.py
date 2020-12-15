#!/usr/bin/python3
# Advent of code 2020 day 15
# See https://adventofcode.com/2020/day/15

def say_number(memory, turn, n):
    previous_turn, _ = memory.get(n, [None, None])
    memory[n] = [turn, previous_turn]
    return n


def say_next_number(memory, previous_number, turn):
    t0, t1 = memory[previous_number]
    assert t0 == turn-1, "Should have just said the previous number"
    if t1 is None:
        n = 0
    else:
        n = t0-t1
    return say_number(memory, turn, n)


def play_game(numbers, limit):
    memory = {}
    for turn, n in enumerate(numbers):
        number = say_number(memory, turn, n)
    for turn in range(len(numbers), limit):
        number = say_next_number(memory, number, turn)
    print(number)


with open("input.txt") as f:
    numbers = [int(n) for n in f.read().split(",")]

play_game(numbers, 2020)
play_game(numbers, 30000000)

