#!/usr/bin/python3
# Advent of code 2022 day 7
# See https://adventofcode.com/2022/day/7

with open("input.txt") as line:
    blocks = [b.strip() for b in line.read().split("$ ") if b]


def add_to_dir(dir_file_sizes, file_path, size):
    for i in range(0, len(file_path)+1):
        key = tuple(file_path[0:i])
        dir_file_sizes[key] = dir_file_sizes.setdefault(key, 0) + size


dir_sizes = {}
cwd = []
for block in blocks:
    lines = block.split("\n")
    match lines[0].split(" "):
        case ["cd", "/"]:
            cwd = []
        case ["cd", ".."]:
            cwd.pop()
        case ["cd", name]:
            cwd.append(name)
        case ["ls"]:
            for line in lines[1:]:
                if not line.startswith("dir "):
                    fsize, fname = line.split(" ")
                    add_to_dir(dir_sizes, cwd, int(fsize))

# Part 1
print(sum(s for s in dir_sizes.values() if s <= 100000))

# Part 2
used_space = dir_sizes.get(tuple())
free_space = 70000000 - used_space
delete_space = 30000000 - free_space
print(min(s for s in dir_sizes.values() if s >= delete_space))
