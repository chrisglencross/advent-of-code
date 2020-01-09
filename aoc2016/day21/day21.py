#!/usr/bin/python3
# Advent of code 2016 day 21
# See https://adventofcode.com/2016/day/21
import itertools
import re

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


def swap(password, p1, p2):
    t = password[p1]
    password[p1] = password[p2]
    password[p2] = t


def rotate_right(password, steps):
    initial_password = password[:]
    for i in range(0, len(password)):
        password[i] = initial_password[(i - steps) % len(password)]


def shuffle(password):
    for line in lines:
        if match := re.fullmatch(r"swap position (.*) with position (.*)", line):
            p1 = int(match.group(1))
            p2 = int(match.group(2))
            swap(password, p1, p2)
        elif match := re.fullmatch(r"swap letter (.*) with letter (.*)", line):
            c1 = match.group(1)
            c2 = match.group(2)
            swap(password, password.index(c1), password.index(c2))
        elif match := re.fullmatch(r"rotate (left|right) (.*) steps?", line):
            left_right = match.group(1)
            steps = int(match.group(2))
            if left_right == "right":
                rotate_right(password, steps)
            else:
                rotate_right(password, len(password) - steps)
        elif match := re.fullmatch(r"rotate based on position of letter (.*)", line):
            c = match.group(1)
            i = password.index(c)
            steps = i + 1
            if i >= 4:
                steps += 1
            rotate_right(password, steps)
        elif match := re.fullmatch(r"reverse positions (.*) through (.*)", line):
            p1 = int(match.group(1))
            p2 = int(match.group(2))
            for i in range((p2 - p1 + 1) // 2):
                swap(password, p1 + i, p2 - i)
        elif match := re.fullmatch(r"move position (.*) to position (.*)", line):
            p1 = int(match.group(1))
            p2 = int(match.group(2))
            value = password[p1]
            del password[p1]
            password.insert(p2, value)
        else:
            raise Exception(f"Unknown command {line}")


# Part 1
password = list("abcdefgh")
shuffle(password)
print("".join(password))

# Part 2
for password in itertools.permutations(list("abcdefgh")):
    shuffled_password = list(password)
    shuffle(shuffled_password)
    if "".join(shuffled_password) == "fbgdceah":
        print("".join(password))
        break
