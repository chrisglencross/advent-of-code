#!/usr/bin/python3
# Advent of code 2021 day 7
# See https://adventofcode.com/2021/day/7
import statistics

with open("input.txt") as f:
    lines = f.readlines()

positions = [int(v) for v in lines[0].split(",")]

# Part 1
median = round(statistics.median(positions))
print(sum(abs(p - median) for p in positions))


# Part 2
def get_move_cost(distance):
    return distance * (distance + 1) // 2


def get_cost(positions, target):
    return sum(get_move_cost(abs(p - target)) for p in positions)


def find_minimum(left, right, function):
    mid = (left + right) // 2
    mid_cost = function(mid)
    if function(mid - 1) < mid_cost:
        return find_minimum(left, mid, function)  # cost is lower to the left
    elif function(mid + 1) < mid_cost:
        return find_minimum(mid, right, function)  # cost is lower to the right
    else:
        return mid_cost


print(find_minimum(min(positions), max(positions) + 1, lambda x: get_cost(positions, x)))
