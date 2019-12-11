#!/usr/bin/python3
# Advent of code 2017 day 24
# See https://adventofcode.com/2017/day/24


with open("input.txt") as f:
    lines = f.readlines()

components = []
for line in lines:
    components.append(tuple([int(port) for port in line.split("/")]))


def search(bridge: list, remaining, open_link):
    leaf = True
    for component in remaining:
        if component[0] == open_link:
            new_bridge = bridge[:]
            new_bridge.append(component)
            new_remaining = remaining[:]
            new_remaining.remove(component)
            leaf = False
            yield from search(new_bridge, new_remaining, component[1])
        if component[1] == open_link:
            new_bridge = bridge[:]
            new_bridge.append(component)
            new_remaining = remaining[:]
            new_remaining.remove(component)
            leaf = False
            yield from search(new_bridge, new_remaining, component[0])
    if leaf:
        yield (bridge)


def score(bridge):
    score = 0
    for component in bridge:
        score = score + component[0] + component[1]
    return score


bridges = search([], components, 0)
# Part 1
# print(max([score(bridge) for bridge in bridges]))
# Part 2
print(max([(len(bridge), score(bridge)) for bridge in bridges]))
