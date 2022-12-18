#!/usr/bin/python3
# Advent of code 2022 day 18
# See https://adventofcode.com/2022/day/18

import itertools

with open("input.txt") as f:
    coords = [(int(v) for v in line.split(",")) for line in f.readlines()]

# List of external cube faces:
# - plane of the square
# - coords of the square vertex closest to the origin
# - direction of the face along the axis perpendicular to the plane
squares = list()
for x, y, z in coords:
    squares.extend([
        ('x', (x, y, z),  -1),
        ('x', (x+1, y, z), 1),
        ('y', (x, y, z),  -1),
        ('y', (x, y+1, z), 1),
        ('z', (x, y, z),  -1),
        ('z', (x, y, z+1), 1),
    ])

# Part 1
surfaces = {surface
            for surface, items
            in itertools.groupby(sorted((plane, coords) for plane, coords, direction in squares))
            if len(list(items)) == 1}
print(len(surfaces))

# Part 2
surfaces_with_direction = {
    (plane, coords, direction)
    for plane, coords, direction in squares
    if (plane, coords) in surfaces}

start = min(surfaces_with_direction)
visited = set([start])
dirty = True
while dirty:
    dirty = False
    for plane, (x, y, z), direction in list(visited):
        # For each cube face visit the neighbouring faces (keeping to the external facing direction)
        # Neighbours along each edge of the square may be one of concave, flat or convex with that precedence.
        # Lots of literal hand waving required to come up with these tables:
        if plane == 'x':
            neighbours = [
                [('y', (x, y, z),    direction), ('x', (x, y-1, z), direction), ('y', (x-1, y, z),  -direction)],
                [('y', (x, y+1, z), -direction), ('x', (x, y+1, z), direction), ('y', (x-1, y+1, z), direction)],
                [('z', (x, y, z),    direction), ('x', (x, y, z-1), direction), ('z', (x-1, y, z),  -direction)],
                [('z', (x, y, z+1), -direction), ('x', (x, y, z+1), direction), ('z', (x-1, y, z+1), direction)]
            ]
        if plane == 'y':
            neighbours = [
                [('x', (x, y, z),    direction), ('y', (x-1, y, z), direction), ('x', (x, y-1, z),  -direction)],
                [('x', (x+1, y, z), -direction), ('y', (x+1, y, z), direction), ('x', (x+1, y-1, z), direction)],
                [('z', (x, y, z),    direction), ('y', (x, y, z-1), direction), ('z', (x, y-1, z),  -direction)],
                [('z', (x, y, z+1), -direction), ('y', (x, y, z+1), direction), ('z', (x, y-1, z+1), direction)]
            ]
        if plane == 'z':
            neighbours = [
                [('y', (x, y, z),    direction), ('z', (x, y-1, z), direction), ('y', (x, y, z-1),  -direction)],
                [('y', (x, y+1, z), -direction), ('z', (x, y+1, z), direction), ('y', (x, y+1, z-1), direction)],
                [('x', (x, y, z),    direction), ('z', (x-1, y, z), direction), ('x', (x, y, z-1),  -direction)],
                [('x', (x+1, y, z), -direction), ('z', (x+1, y, z), direction), ('x', (x+1, y, z-1), direction)]
            ]
        # Shorthand to avoid repeating the tables for negative direction faces
        if direction == -1:
            neighbours = [reversed(neighbour) for neighbour in neighbours]

        for edge_neighbours in neighbours:
            for edge_neighbour in edge_neighbours:
                if edge_neighbour in surfaces_with_direction:
                    if edge_neighbour not in visited:
                        visited.add(edge_neighbour)
                        dirty = True
                    break

print(len(visited))
