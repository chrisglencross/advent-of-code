#!/usr/bin/python3
# Advent of code 2019 day 6
import copy

with open("input.txt") as f:
    lines = f.readlines()

# Build dictionary object -> set(orbiters)
direct_orbits = {}
for line in lines:
    parts = line.strip().split(")")
    if parts[0] in direct_orbits:
        direct_orbits[parts[0]].add(parts[1])
    else:
        direct_orbits[parts[0]] = set([parts[1]])

# Part 1
indirect_orbits = copy.deepcopy(direct_orbits)

# Inefficient - would be better to have the direct_orbits
# dictionary inverted and have a count_descendents recursive function
# that returns the number of descendents of each node, caching the result.
modified = True
while modified:
    modified = False
    for orbited, orbiters in indirect_orbits.items():
        for orbiter in list(orbiters):
            new_orbiters = set(indirect_orbits.get(orbiter, set()))
            new_orbiters.difference_update(orbiters)
            if new_orbiters:
                orbiters.update(new_orbiters)
                modified = True

count = 0
for orbiter in indirect_orbits.values():
    count = count + len(orbiter)
print(count)


# Part 2
def find_orbit(orbiter):
    # Again, this would be better if the direct_orbits dictionary was inverted
    # Not my finest solution.
    for l, rs in direct_orbits.items():
        if orbiter in rs:
            return l
    return None


def find_chain(orbiter):
    result = []
    while True:
        orbiter = find_orbit(orbiter)
        if orbiter is None:
            break
        result.insert(0, orbiter)
    return result


you_chain = find_chain("YOU")
san_chain = find_chain("SAN")
while you_chain[0] == san_chain[0]:
    you_chain.pop(0)
    san_chain.pop(0)
print(len(you_chain) + len(san_chain))
