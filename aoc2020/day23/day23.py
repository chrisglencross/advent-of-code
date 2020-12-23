#!/usr/bin/python3
# Advent of code 2020 day 23
# See https://adventofcode.com/2020/day/23

def do_move(current_cup, cup_index, max_cup_no):
    remove_cup_1 = cup_index[current_cup]
    remove_cup_2 = cup_index[remove_cup_1]
    remove_cup_3 = cup_index[remove_cup_2]
    next_cup = cup_index[remove_cup_3]
    cup_index[current_cup] = next_cup

    destination_cup = current_cup
    while True:
        destination_cup = destination_cup - 1
        if destination_cup == 0:
            destination_cup = max_cup_no
        if destination_cup not in [remove_cup_1, remove_cup_2, remove_cup_3]:
            break

    next_cup = cup_index[destination_cup]
    cup_index[destination_cup] = remove_cup_1
    cup_index[remove_cup_3] = next_cup


def play_game(cups, turns):

    # Index of cup to next cup
    cup_count = len(cups)
    cup_index = [None] * (cup_count+1)
    for i, c in enumerate(cups):
        cup_index[c] = cups[(i + 1) % cup_count]

    current_cup = cups[0]
    max_cup_no = max(cups)
    for turn in range(0, turns):
        do_move(current_cup, cup_index, max_cup_no)
        current_cup = cup_index[current_cup]

    return cup_index


def part1(puzzle):
    cups = [int(c) for c in puzzle]
    cup_index = play_game(cups, 100)

    result = []
    next1 = cup_index[1]
    while next1 != 1:
        result.append(str(next1))
        next1 = cup_index[next1]
    print("Part 1:", "".join(result))


def part2(puzzle):
    cups = [int(c) for c in puzzle]
    cups.extend(range(10, 1_000_001))
    cup_index = play_game(cups, 10_000_000)

    next1 = cup_index[1]
    next2 = cup_index[next1]
    print("Part 2:", next1 * next2)


part1("952316487")
part2("952316487")
