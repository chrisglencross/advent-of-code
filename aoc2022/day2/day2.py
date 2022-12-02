#!/usr/bin/python3
# Advent of code 2022 day 2
# See https://adventofcode.com/2022/day/2

# rock=0, paper=1, scissors=2
win_combos = {0: 1, 1: 2, 2: 0}
lose_combos = {0: 2, 1: 0, 2: 1}


def get_score(p1, p2):
    s = p2 + 1
    if win_combos[p1] == p2:
        s += 6
    elif lose_combos[p1] != p2:
        s += 3
    return s


with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

score = 0
for line in lines:
    p1, p2 = line.split(" ")
    p1 = ord(p1) - ord('A')
    p2 = ord(p2) - ord('X')
    score += get_score(p1, p2)
print(score)

score = 0
for line in lines:
    p1, s = line.split(" ")
    p1 = ord(p1) - ord('A')
    if s == 'X':
        p2 = lose_combos[p1]
    elif s == 'Z':
        p2 = win_combos[p1]
    else:
        p2 = p1
    score += get_score(p1, p2)
print(score)
