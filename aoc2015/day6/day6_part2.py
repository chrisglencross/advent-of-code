#!/usr/bin/python3
# Advent of code 2015 day 6
# See https://adventofcode.com/2015/day/6


with open("input.txt") as f:
    lines = f.readlines()

grid = []
for i in range(1000):
    grid.append([0] * 1000)

for line in lines:
    line = line.strip()
    words = line.split(" ")
    start = 0
    if words[0] == "turn":
        start += 1
    command = words[start]
    top_left = [int(num) for num in words[start + 1].split(",")]
    bottom_right = [int(num) for num in words[start + 3].split(",")]
    for y in range(top_left[1], bottom_right[1] + 1):
        for x in range(top_left[0], bottom_right[0] + 1):
            if command == "on":
                grid[y][x] += 1
            elif command == "off" and grid[y][x] > 0:
                grid[y][x] -= 1
            elif command == "toggle":
                grid[y][x] += 2
lights = 0
for row in grid:
    for light in row:
        lights += light

print(lights)
