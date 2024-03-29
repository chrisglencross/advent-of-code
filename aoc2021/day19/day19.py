#!/usr/bin/python3
# Advent of code 2021 day 19
# See https://adventofcode.com/2021/day/19
import itertools

ROTATIONS = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (y, x, -z),
    lambda x, y, z: (-y, z, -x),
    lambda x, y, z: (z, y, -x),
    lambda x, y, z: (z, x, y),
    lambda x, y, z: (-z, x, -y),
    lambda x, y, z: (-y, x, z),
    lambda x, y, z: (x, -z, y),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (-z, -x, y),
    lambda x, y, z: (y, -x, z),
    lambda x, y, z: (z, -x, -y),
    lambda x, y, z: (y, -z, -x),
    lambda x, y, z: (-y, -x, -z),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (-z, -y, -x),
    lambda x, y, z: (-x, z, y),
    lambda x, y, z: (-x, -z, -y),
    lambda x, y, z: (x, z, -y),
    lambda x, y, z: (-x, y, -z),
    lambda x, y, z: (z, -y, x),
    lambda x, y, z: (y, z, x),
    lambda x, y, z: (-y, -z, x),
    lambda x, y, z: (-z, y, x)
]


def rotate(coords, num):
    return ROTATIONS[num](*coords)


ROTATION_INVERSES = {}
ROTATION_ADDITIONS = {}
p0 = (1, 2, 3)
for r0 in range(24):
    for r1 in range(24):
        if rotate(rotate(p0, r0), r1) == p0:
            ROTATION_INVERSES[r0] = r1
        for r2 in range(0, 24):
            if rotate(rotate(p0, r0), r1) == rotate(p0, r2):
                ROTATION_ADDITIONS[(r0, r1)] = r2


def reverse_rotation(r):
    return ROTATION_INVERSES[r]


def add_rotation(r1, r2):
    return ROTATION_ADDITIONS[(r1, r2)]


def add(c1, c2):
    return c1[0] + c2[0], c1[1] + c2[1], c1[2] + c2[2]


def count_common_beacons(s0, s1, s1_orientation, translation):
    # Rotate and shift s1 beacons to the same origin as s0 and compare
    s1_adjusted = set(add(rotate(sb1, s1_orientation), translation) for sb1 in s1)
    return len(s1_adjusted.intersection(s0))


def find_scanners(scanners):
    found_scanners = {0: (0, (0, 0, 0))}
    unfound_scanner_nos = set(range(1, len(scanners)))
    already_checked = {}
    while unfound_scanner_nos:
        for n0 in list(found_scanners.keys()):
            s0 = scanners[n0]
            n1s_to_check = unfound_scanner_nos - already_checked.setdefault(n0, set())
            for n1 in n1s_to_check:
                print(f"Checking {n0} -> {n1}")
                already_checked[n0].add(n1)
                s1 = scanners[n1]
                for sb0, sb1 in itertools.product(s0, s1):
                    for s1_orientation_relative_to_s0 in range(0, 24):
                        rotated_sb1 = rotate(sb1, s1_orientation_relative_to_s0)
                        translation = (sb0[0] - rotated_sb1[0], sb0[1] - rotated_sb1[1], sb0[2] - rotated_sb1[2])
                        n = count_common_beacons(s0, s1, s1_orientation_relative_to_s0, translation)
                        if n == 12:
                            s0_orientation, s0_position = found_scanners[n0]
                            s1_position = add(rotate(translation, s0_orientation), s0_position)
                            s1_orientation = add_rotation(s1_orientation_relative_to_s0, s0_orientation)

                            print(f" -> Scanner {n1} at ({s1_position}) with orientation {s1_orientation}")
                            found_scanners[n1] = (s1_orientation, s1_position)
                            unfound_scanner_nos.remove(n1)
                            break
                    if n1 in found_scanners.keys():
                        break
    return found_scanners


def find_distinct_beacons(scanner_beacons, scanner_locations):
    distinct_beacons = set()
    for scanner_no in range(0, len(scanner_beacons)):
        beacons = scanner_beacons[scanner_no]
        scanner_orientation, scanner_coords = scanner_locations[scanner_no]
        for beacon in beacons:
            relative_coords = rotate(beacon, scanner_orientation)
            absolute_coords = add(scanner_coords, relative_coords)
            distinct_beacons.add(absolute_coords)
    return distinct_beacons


with open("input.txt") as f:
    scanner_beacons = [
        [tuple(int(n) for n in line.split(",")) for line in block.split('\n')[1:]]
        for block in [block.strip() for block in f.read().replace('\r', '').split('\n\n')]
    ]

# Part 1
scanner_locations = find_scanners(scanner_beacons)
distinct_beacons = find_distinct_beacons(scanner_beacons, scanner_locations)
print(len(distinct_beacons))

# Part 2
print(max(
    abs(s1[0] - s2[0]) + abs(s1[1] - s2[1]) + abs(s1[2] - s2[2])
    for (_, s1), (_, s2) in itertools.combinations(scanner_locations.values(), 2)
))
