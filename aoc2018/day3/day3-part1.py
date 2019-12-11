import re

with open("input") as f:
    lines = f.readlines()

cloth = [[set() for row in range(0, 1000)] for col in range(0, 1000)]

non_overlap_claims = set()

for line in lines:
    # #1306 @ 693,253: 20x23
    match = re.search("^#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)$", line.strip())
    claim = match.group(1)
    non_overlap_claims.add(claim)
    left = int(match.group(2))
    top = int(match.group(3))
    width = int(match.group(4))
    height = int(match.group(5))
    for x in range(left, left + width):
        for y in range(top, top + height):
            cloth[x][y].add(claim)

count = 0
for row in cloth:
    for cell in row:
        if len(cell) > 1:
            count = count + 1
            for claim in cell:
                if claim in non_overlap_claims:
                    non_overlap_claims.remove(claim)

print(non_overlap_claims)
