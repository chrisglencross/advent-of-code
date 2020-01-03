#!/usr/bin/python3
# Advent of code 2015 day 5
# See https://adventofcode.com/2015/day/5

with open("input.txt") as f:
    lines = f.readlines()
nice = 0
for line in lines:
    line = line.strip()
    strings = False
    vowel = 0
    double_letter = False

    for i, c in enumerate(line):
        if c.lower() in "aeiou":
            vowel += 1
        if i > 0 and c == line[i - 1]:
            double_letter = True
    if line.find("ab") >= 0 or line.find("cd") >= 0 or line.find("pq") >= 0 or line.find("xy") >= 0:
        strings = True
    if vowel >= 3 and double_letter == True and strings == False:
        nice += 1

print(nice)
