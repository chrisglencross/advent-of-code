#!/usr/bin/python3
# Advent of code 2020 day 5
# See https://adventofcode.com/2020/day/5

def row_id(boarding_pass: str):
    return int(boarding_pass[0:7].replace("F", "0").replace("B", "1"), 2)


def column_id(boarding_pass: str):
    return int(boarding_pass[7:10].replace("R", "1").replace("L", "0"), 2)


def seat_id(boarding_pass: str):
    return row_id(boarding_pass) * 8 + column_id(boarding_pass)


with open("input.txt") as f:
    seat_ids = [seat_id(b) for b in f.readlines()]

print(max(seat_ids))
print({s for s in range(min(seat_ids), max(seat_ids)+1)}.difference(seat_ids))


