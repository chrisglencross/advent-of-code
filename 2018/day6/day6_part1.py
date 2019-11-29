import copy
from statistics import mode

with open("input", "r") as f:
    lines = f.readlines()

coords = []
for line in lines:
    vals = line.split(",")
    coords.append(tuple([int(vals[0]), int(vals[1])]))

min_x = min(coords, key=lambda coord: coord[0])[0] - 1
max_x = max(coords, key=lambda coord: coord[0])[0] + 1
min_y = min(coords, key=lambda coord: coord[1])[1] - 1
max_y = max(coords, key=lambda coord: coord[1])[1] + 1

grid = []
for y in range(min_y, max_y + 1):
    row = []
    for x in range(min_x, max_x + 1):
        row.append([])
    grid.append(row)

for coord in coords:
    grid[coord[1] - min_y][coord[0] - min_x] = {coord}

# Flood fill
iterations = 0
modified = True
while modified:
    print(iterations)
    iterations = iterations + 1
    modified = False
    new_grid = copy.deepcopy(grid)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):

            current = grid[y - min_y][x - min_x]
            if len(current) > 0:
                # Already got closest neighbour
                continue

            up = None
            down = None
            left = None
            right = None
            neighbours = []
            if y - min_y - 1 >= 0:
                up = grid[y - min_y - 1][x - min_x]
                neighbours.extend(up)
            if y - min_y + 1 < len(grid):
                down = grid[y - min_y + 1][x - min_x]
                neighbours.extend(down)
            if x - min_x - 1 >= 0:
                left = grid[y - min_y][x - min_x - 1]
                neighbours.extend(left)
            if x - min_x + 1 < len(grid[0]):
                right = grid[y - min_y][x - min_x + 1]
                neighbours.extend(right)

            if len(neighbours) > 0:
                new_grid[y - min_y][x - min_x] = set(neighbours)
                modified = True

    grid = new_grid

for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        cell = grid[y - min_y][x - min_x]
        if len(cell) == 1:
            grid[y - min_y][x - min_x] = list(cell)[0]
        else:
            grid[y - min_y][x - min_x] = None

print("Grid:")
for row in grid:
    print(row)
print()

infinite_cells = set([])
for y in range(min_y, max_y + 1):
    infinite_cells.add(grid[y - min_y][min_y - min_y])
    infinite_cells.add(grid[y - min_y][max_x - min_x])
for x in range(min_x, max_x + 1):
    infinite_cells.add(grid[min_y - min_y][x - min_x])
    infinite_cells.add(grid[max_y - min_y][x - min_x])

print("Infinite Cells:")
print(infinite_cells)
print()

print(tuple([8, 3]) in infinite_cells)

cells = []
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        cell = grid[y - min_y][x - min_x]
        if cell not in infinite_cells:
            cells.append(tuple(cell))

# Most common:
most_common = mode(cells)
print(most_common)
print(cells.count(most_common))
