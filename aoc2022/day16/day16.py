#!/usr/bin/python3
# Advent of code 2022 day 16
# See https://adventofcode.com/2022/day/16

import re

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

network = {}
for line in lines:
    v, flow, tunnels = re.match("^Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)$", line).groups()
    network[v] = (int(flow), tunnels.split(", "))


def move(visited, frontier, move_elephant, minutes_remaining):
    new_frontier = []
    for key in frontier:
        me, elephant, valves_open = key
        location = elephant if move_elephant else me
        score = visited[key]
        flow, tunnels = network[location]
        if flow > 0 and location not in valves_open:
            # Open the valve
            new_key = (me, elephant, frozenset(valves_open | {location}))
            new_score = score + minutes_remaining * flow
            if visited.get(new_key, -1) < new_score:
                visited[new_key] = new_score
                new_frontier.append(new_key)
        for new_location in tunnels:
            # Move to a new location
            new_key = (me, new_location, valves_open) if move_elephant else (new_location, elephant, valves_open)
            if visited.get(new_key, -1) < score:
                visited[new_key] = score
                new_frontier.append(new_key)
    return new_frontier


# Part 1
start_key = ("AA", None, frozenset({}))
visited = {start_key: 0}
frontier = [start_key]
for minute in range(0, 30):
    frontier = move(visited, frontier, False, 29 - minute)
print(max(visited.values()))


# Part 2
start_key = ("AA", "AA", frozenset({}))
visited = {start_key: 0}
frontier = [start_key]
for minute in range(0, 26):
    # Heuristic for reasonable performance: Prune solutions which don't look promising (not in the top 100k)
    if len(frontier) > 100_000:
        good_enough_score = sorted(visited.values(), reverse=True)[100_000]
        frontier = [f for f in frontier if visited[f] >= good_enough_score]
    frontier = move(visited, frontier, False, 25 - minute)   # Move me
    frontier = move(visited, frontier, True,  25 - minute)   # Move my elephant
print(max(visited.values()))
