#!/usr/bin/python3
# Advent of code 2019 day 12
import itertools
from dataclasses import dataclass

import numpy


@dataclass
class Moon:
    name: str
    position: tuple
    velocity: tuple


def init_moons():
    global moons
    moons = [
        Moon("a", position=(6, 10, 10), velocity=(0, 0, 0)),
        Moon("b", position=(-9, 3, 17), velocity=(0, 0, 0)),
        Moon("c", position=(9, -4, 14), velocity=(0, 0, 0)),
        Moon("d", position=(4, 14, 4), velocity=(0, 0, 0)),
    ]


def tick():
    for moon1 in moons:
        gravity = list([0, 0, 0])
        for moon2 in moons:
            if moon1.name == moon2.name:
                continue
            for dimension in range(0, 3):
                if moon1.position[dimension] > moon2.position[dimension]:
                    gravity[dimension] = gravity[dimension] - 1
                elif moon1.position[dimension] < moon2.position[dimension]:
                    gravity[dimension] = gravity[dimension] + 1
        moon1.velocity = (
            moon1.velocity[0] + gravity[0], moon1.velocity[1] + gravity[1], moon1.velocity[2] + gravity[2])

    for moon1 in moons:
        moon1.position = (moon1.velocity[0] + moon1.position[0], moon1.velocity[1] + moon1.position[1],
                          moon1.velocity[2] + moon1.position[2])


def print_moons(t):
    print(f"After {t} ticks")
    for moon in moons:
        print(f"{moon.name}: position={moon.position} velocity={moon.velocity}")


def get_energy():
    return sum([sum([abs(p) for p in moon.position]) * sum([abs(v) for v in moon.velocity]) for moon in moons])


def part1():
    init_moons()
    for t in range(0, 1000):
        tick()
    print_moons(1000)
    print(f"Total energy in system {get_energy()}")


# Summarises the state of the system in a single dimension
def get_dimension_state(dimension):
    return tuple([(moon.name, moon.position[dimension], moon.velocity[dimension]) for moon in moons])


def part2():
    init_moons()

    # Record 3 initial dimension states (x, y, z axis), containing velocity and position for all moons in that dimension
    dimension_initial_states = dict()
    for dimension in range(0, 3):
        dimension_initial_states[dimension] = get_dimension_state(dimension)

    repeat_intervals = dict()
    for t in itertools.count(1):
        tick()
        for dimension in range(0, 3):
            dimension_state = get_dimension_state(dimension)
            if dimension not in repeat_intervals and dimension_initial_states[dimension] == dimension_state:
                repeat_intervals[dimension] = t
        if len(repeat_intervals) == 3:
            break

    print(f"Dimension repeat intervals: {repeat_intervals}")

    # Entire system repeats after the lowest-common-multiple of all dimension repeat intervals
    p = 1
    for interval in repeat_intervals.values():
        p = numpy.lcm(p, interval)
    print(f"System repeats after {p} intervals")


if __name__ == "__main__":
    part1()
    part2()
