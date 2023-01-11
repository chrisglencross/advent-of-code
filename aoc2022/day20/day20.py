#!/usr/bin/python3
# Advent of code 2022 day 20
# See https://adventofcode.com/2022/day/20

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


def load(decryption_key):
    values_by_id = []
    positions_by_id = {}
    ids_by_position = {}
    for i, line in enumerate(lines):
        value = int(line) * decryption_key
        values_by_id.append(value)
        positions_by_id[i] = i
        ids_by_position[i] = i
    return values_by_id, positions_by_id, ids_by_position


def shift_left(positions_by_id, ids_by_position, start_range, end_range):
    for position in range(start_range, end_range + 1):
        id = ids_by_position[position]
        new_position = position - 1
        positions_by_id[id] = new_position
        ids_by_position[new_position] = id


def shift_right(positions_by_id, ids_by_position, start_range, end_range):
    for position in range(end_range, start_range - 1, -1):
        id = ids_by_position[position]
        new_position = position + 1
        positions_by_id[id] = new_position
        ids_by_position[new_position] = id


def mix(values_by_id, positions_by_id, ids_by_position):
    list_len = len(values_by_id)
    for id, value in enumerate(values_by_id):
        pos = positions_by_id[id]
        value = values_by_id[id]
        move_to = (value + pos) % (list_len - 1)
        if move_to > pos:
            shift_left(positions_by_id, ids_by_position, pos + 1, move_to)
        elif move_to < pos:
            shift_right(positions_by_id, ids_by_position, move_to, pos - 1)
        positions_by_id[id] = move_to
        ids_by_position[move_to] = id


def get_answer(values_by_id, positions_by_id, ids_by_position):
    list_len = len(values_by_id)
    zero_id = next(id for id, value in enumerate(values_by_id) if value == 0)
    zero_pos = positions_by_id[zero_id]
    answer = 0
    for offset in [1000, 2000, 3000]:
        value = values_by_id[ids_by_position[(zero_pos + offset) % list_len]]
        answer += value
    return answer


# Part 1
data = load(1)
mix(*data)
print(get_answer(*data))

# Part 2
data = load(811589153)
for i in range(0, 10):
    mix(*data)
print(get_answer(*data))
