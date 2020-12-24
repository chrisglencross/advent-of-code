import itertools
from collections import defaultdict

with open("input") as f:
    lines = [line.strip() for line in f.readlines()]

counts = defaultdict(lambda: 0)
for line in lines:
    for s in {len(list(v)) for k, v in itertools.groupby(sorted(line))}:
        counts[s] += 1

print(counts[2] * counts[3])
