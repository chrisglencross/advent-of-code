target = 277678

directions = [
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 1)
]


def get_coords(cell_number):
    x = 0
    y = 0
    i = 0
    stride_length = 0
    remaining = cell_number - 1
    while remaining != 0:
        direction = directions[i % len(directions)]
        i = i + 1
        if direction == (1, 0) or direction == (-1, 0):
            stride_length = stride_length + 1
        move_distance = min(stride_length, remaining)
        x = x + direction[0] * move_distance
        y = y + direction[1] * move_distance
        # print(x, y)
        remaining = remaining - move_distance
    return x, y


# part 1
x, y = get_coords(target)
print(abs(x) + abs(y))

# part 2
cell_indices = dict()
for i in range(1, 10000):
    coords = get_coords(i)
    cell_indices[coords] = i

cell_values = dict()
cell_values[(0, 0)] = 1
for i in range(2, 10000):
    coords = get_coords(i)
    neighbour_sum = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            neighbour_value = cell_values.get((coords[0] + dx, coords[1] + dy), 0)
            neighbour_sum = neighbour_sum + neighbour_value
    cell_values[coords] = neighbour_sum
    print(coords, neighbour_sum)
    if neighbour_sum > target:
        break

cell_values = {}
