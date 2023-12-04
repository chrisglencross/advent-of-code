#!/usr/bin/python3
# Advent of code 2023 day 4
# See https://adventofcode.com/2023/day/4

import re
from collections import defaultdict

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

card_counts = defaultdict(lambda: 0)
score = 0
for line in lines:
    c, w, n = re.match('^Card +([0-9]+): (.*) \\| (.*)$', line).groups()
    card = int(c)
    card_counts[card] += 1
    matches = len(set(w.split()) & set(n.split()))
    score += 2 ** (matches-1) if matches > 0 else 0
    for i in range(card+1, card+matches+1):
        card_counts[i] += card_counts[card]

print(score)
print(sum(card_counts.values()))
