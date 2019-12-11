def get_power_level(x, y, serial_number=7511):
    rack_id = x + 10
    power_level = rack_id * y
    power_level = power_level + serial_number
    power_level = power_level * rack_id
    power_level = int(power_level / 100) % 10
    power_level = power_level - 5
    return power_level


cell_levels = []
for y in range(1, 301):
    row = []
    for x in range(1, 301):
        row.append(get_power_level(x, y))
    cell_levels.append(row)

# Zero indexed here - add one to result
max_level = -1000
for y in range(0, 301):
    for x in range(0, 301):
        max_square_size = min(301 - x, 301 - y)
        power_level = 0
        for square_size in range(1, max_square_size):
            for dx in range(0, square_size):
                power_level = power_level + cell_levels[y + square_size - 1][x + dx]
            for dy in range(0, square_size):
                power_level = power_level + cell_levels[y + dy][x + square_size - 1]
            # Remove double counted bottom-right corner
            power_level = power_level - cell_levels[y + square_size - 1][x + square_size - 1]
            if power_level > max_level:
                max_level = power_level
                print(x + 1, y + 1, square_size)
