#!/usr/bin/python3
# Advent of code 2021 day 19
# See https://adventofcode.com/2021/day/19
import itertools

with open("input.txt") as f:
    blocks = [block.strip() for block in f.read().replace('\r', '').split('\n\n')]
    scanners = []
    for block in blocks:
        beacons = []
        for line in block.split('\n')[1:]:
            beacons.append(tuple(int(n) for n in line.split(",")))
        scanners.append(beacons)

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
ROTATION_INVERSES = {}
ROTATION_ADDITIONS = {}


def rotate(coords, num):
    return ROTATIONS[num](*coords)


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
    return c1[0]+c2[0], c1[1]+c2[1], c1[2]+c2[2]


def count_common_beacons(s0, s1, s1orientation, translation):
    result = 0
    sb1rs = [add(rotate(sb1, s1orientation), translation) for sb1 in s1]
    for sb0, sb1r in itertools.product(s0, sb1rs):
        if sb0 == sb1r:
            result += 1
    return result


found_scanners = {0: (0, (0, 0, 0))}
unfound_scanner_nos = set(range(1, len(scanners)))
already_checked = {}
while unfound_scanner_nos:
    for n0 in list(found_scanners.keys()):
        s0 = scanners[n0]
        n1s_to_check = unfound_scanner_nos - already_checked.get(n0, set())
        for n1 in n1s_to_check:
            print(f"Checking overlap {n0} <-> {n1}")
            already_checked.setdefault(n0, set()).add(n1)
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

                        print(f" -> Scanner {n1} is at ({s1_position}) relative to origin with orientation {s1_orientation}")
                        found_scanners[n1] = (s1_orientation, s1_position)
                        unfound_scanner_nos.remove(n1)
                        break
                if n1 in found_scanners.keys():
                    break

# Found all the scanners, now find the beacons
beacons = set()
for scanner_no in range(0, len(scanners)):
    scanner_beacons = scanners[scanner_no]
    scanner_orientation, scanner_coords = found_scanners[scanner_no]
    for scanner_beacon in scanner_beacons:
        relative_coords = rotate(scanner_beacon, scanner_orientation)
        absolute_coords = add(scanner_coords, relative_coords)
        beacons.add(absolute_coords)

# Part 1
print(len(beacons))

# Part 2
distances = []
for (_, s1), (_, s2) in itertools.combinations(found_scanners.values(), 2):
    distances.append(abs(s1[0]-s2[0]) + abs(s1[1]-s2[1]) + abs(s1[2]-s2[2]))
print(max(distances))
