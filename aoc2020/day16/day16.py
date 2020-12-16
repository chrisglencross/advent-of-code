#!/usr/bin/python3
# Advent of code 2020 day 16
# See https://adventofcode.com/2020/day/16

import re
from functools import reduce

with open("input.txt") as f:
    lines = f.readlines()

fields = {}
tickets = []

for line in lines:
    match = re.fullmatch(r"^([^:]+): (.*)$", line.strip())
    if match:
        field_name = match.group(1)
        ranges = [(int(f), int(t)) for f, t in [r.split("-", 2) for r in match.group(2).split(" or ")]]
        fields[field_name] = ranges
    elif "," in line:
        tickets.append([int(f) for f in line.strip().split(",")])

answer = 0
valid_tickets = []
for ticket in tickets:
    valid = True
    for field in ticket:
        if not any([f <= field <= t for r in fields.values() for f, t in r]):
            answer += field
            valid = False
    if valid:
        valid_tickets.append(ticket)
print(answer)

possible_positions = dict([(field_name, set(range(0, len(fields)))) for field_name in fields.keys()])
for ticket in valid_tickets:
    for position, value in enumerate(ticket):
        for field_name, ranges in fields.items():
            possible_field_positions = possible_positions[field_name]
            if position in possible_field_positions and not any(f <= value <= t for f, t in ranges):
                possible_field_positions.remove(position)
            if len(possible_field_positions) == 1:
                found = list(possible_field_positions)[0]
                for f, p in possible_positions.items():
                    if f != field_name and found in p:
                        p.remove(found)

positions = [list(positions)[0] for field, positions in possible_positions.items() if field.startswith("departure")]
ticket_values = [tickets[0][position] for position in positions]
print(reduce(lambda x, y: x*y, ticket_values))
