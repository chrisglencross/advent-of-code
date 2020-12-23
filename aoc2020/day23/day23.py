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
    cup_count = len(cups)

    # Index of cup to next cup
    cup_index = [None] * (cup_count+1)
    for i in range(0, len(cups)):
        c = cups[i]
        n = cups[(i + 1) % cup_count]
        cup_index[c] = n

    current_cup = cups[0]
    max_cup_no = max(cups)
    for turn in range(0, turns):
        do_move(current_cup, cup_index, max_cup_no)
        current_cup = cup_index[current_cup]

    return cup_index


puzzle = "952316487"

# Part 1
cups = [int(c) for c in puzzle]
cup_index = play_game(cups, 100)

result = []
cup = cup_index[1]
while cup != 1:
    result.append(str(cup))
    cup = cup_index[cup]
print("Part 1:", "".join(result))

# Part 2
cups = [int(c) for c in puzzle]
for i in range(10, 1_000_000 + 1):
    cups.append(i)
cup_index = play_game(cups, 10_000_000)

next1 = cup_index[1]
next2 = cup_index[next1]
print("Part 2:", next1 * next2)
