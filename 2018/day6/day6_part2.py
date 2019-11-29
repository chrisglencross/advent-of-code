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

count = 0
for y in range(min_y, max_y + 1):
    row = []
    for x in range(min_x, max_x + 1):
        total = 0
        for coord in coords:
            total = total + abs(coord[0] - x) + abs(coord[1] - y)
        if total < 10000:
            count = count + 1

print(count)
