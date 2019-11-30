#!/usr/bin/python3
# Advent of code 2017 day 20
# See https://adventofcode.com/2017/day/20

import re
from dataclasses import dataclass

import numpy as np


@dataclass
class Particle:
    name: str
    p: np.ndarray
    v: np.ndarray
    a: np.ndarray

    def position_at(self, ticks):
        final_velocity = self.v + (self.a * ticks)
        average_velocity = (self.v + self.a + final_velocity) / 2
        final_position = self.p + (average_velocity * ticks)
        return final_position


def load_particles():
    particles = []
    with open("input.txt") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        # p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
        match = re.search(
            "^p=<([- 0-9]+),([- 0-9]+),([- 0-9]+)>, v=<([- 0-9]+),([- 0-9]+),([- 0-9]+)>, a=<([- 0-9]+),([- 0-9]+),([- 0-9]+)>$",
            line.strip())
        if match:
            p = np.array([int(match.group(1)), int(match.group(2)), int(match.group(3))])
            v = np.array([int(match.group(4)), int(match.group(5)), int(match.group(6))])
            a = np.array([int(match.group(7)), int(match.group(8)), int(match.group(9))])
            particles.append(Particle(f"particle-{i}", p, v, a))
        else:
            raise Exception("Invalid input:" + line)
    return particles


particles = load_particles()

# Part 1: particle with min acceleration will end up closest to origin
min_acceleration = min(particles, key=lambda p: np.linalg.norm(p.a))
print(min_acceleration)

# Part 2 - naive approach which doesn't really know when to stop.
# In practice less than 50 ticks required for input data.
for tick in range(0, 5000):
    positions = dict()
    for p in particles[:]:
        position = tuple(p.position_at(tick))
        collision_particle = positions.get(position)
        if collision_particle is not None:
            print(f"{p} collided with {collision_particle} at {tick}")
            particles.remove(p)
            if collision_particle in particles:
                particles.remove(collision_particle)
        else:
            positions[position] = p

    if tick % 1000 == 0:
        print("Progress... ", tick, len(particles))
