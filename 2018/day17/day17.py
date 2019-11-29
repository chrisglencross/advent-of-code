import re


def get_range(value):
    nums = [int(num) for num in value.split("..")]
    if len(nums) == 1:
        return nums
    if len(nums) == 2:
        return list(range(nums[0], nums[1] + 1))
    raise Exception("Unparseable number range: " + value)


def get_cell(x, y):
    return rows[y][x - min_x]


def set_cell(x, y, symbol, overwrite=False):
    if get_cell(x, y) != '.' and not overwrite:
        raise Exception("Cannot set a cell that is not empty: " + get_cell(x, y))
    rows[y][x - min_x] = symbol


def scan_left_and_right(x, y):
    # Search left
    for scan_x in range(x - 1, min_x - 1, -1):
        if get_cell(scan_x, y) == '.' or (y < max_y and get_cell(scan_x, y + 1) in ["."]):
            return scan_x
        if get_cell(scan_x, y) in ['|'] and get_cell(scan_x, y + 1) in ['|']:
            break
        if get_cell(scan_x, y) in ['#']:
            break
    # Search right
    for scan_x in range(x + 1, max_x + 1, 1):
        if get_cell(scan_x, y) == '.' or (y < max_y and get_cell(scan_x, y + 1) in ["."]):
            return scan_x
        if get_cell(scan_x, y) in ['|'] and get_cell(scan_x, y + 1) in ['|']:
            # Waterfall
            break
        if get_cell(scan_x, y) in ['#']:
            # Hit a wall
            break
    return None


def is_stable(x, y):
    if y == max_y:
        return False  # Falling off the bottom
    for scan_x in range(x - 1, min_x - 1, -1):
        if scan_x == min_x:
            return False  # Flow off the side
        if get_cell(scan_x, y + 1) not in ["#", "~", "|"]:
            return False  # Fall through hole in bottom
        if get_cell(scan_x, y) == "#":
            break
    for scan_x in range(x + 1, max_x + 1, 1):
        if scan_x == max_x:
            return False  # Flow off the side
        if get_cell(scan_x, y + 1) not in ["#", "~", "|"]:
            return False  # Fall through hole in bottom
        if get_cell(scan_x, y) == "#":
            break
    return True


def can_fall_sideways(x, y):
    if get_cell(x, y + 1) == "~":
        return True  # Falling beside some settled water
    if get_cell(x, y + 1) == "|" and get_cell(x, y + 2) in ["~", "#"]:
        return True  # Falling beside surface unstable water
    if is_stable(x, y + 1):
        return True  # Something unstable became stable
    return False


def add_droplet():
    x = 500
    y = 0

    moving = True
    while moving:
        moving = False
        while y < max_y and get_cell(x, y + 1) == '.':
            y = y + 1
            moving = True

        if y < max_y - 1 and can_fall_sideways(x, y):
            new_x = scan_left_and_right(x, y + 1)
            if new_x is not None:
                # Move sideways to fill the row below
                x = new_x
                moving = True

    if is_stable(x, y):
        return x, y, "~"
    else:
        return x, y, "|"


def print_grid():
    for row in rows:
        print("".join(row))
    print("")


with open("input") as f:
    lines = f.readlines()

scan = []
for line in lines:
    match = re.search("([xy])=([0-9.]+), ([xy])=([0-9.]+)", line)
    if match is not None:
        letter1 = match.group(1)
        range1 = get_range(match.group(2))
        letter2 = match.group(3)
        range2 = get_range(match.group(4))
        if letter1 == 'x' and letter2 == 'y':
            scan.append((range1, range2))
        elif letter1 == 'y' and letter2 == 'x':
            scan.append((range2, range1))

x_values = [value for scan_line in scan for value in scan_line[0]]
min_x = min(x_values) - 2
max_x = max(x_values) + 2
y_values = [value for scan_line in scan for value in scan_line[1]]
min_y = min(y_values)
max_y = max(y_values)

clay_coords = set()
for scan_line in scan:
    for x in scan_line[0]:
        for y in scan_line[1]:
            clay_coords.add((x, y))

rows = []
for y in range(0, max_y + 1):
    row = []
    for x in range(min_x, max_x + 1):
        if (x, y) in clay_coords:
            row.append("#")
        elif (x, y) == (500, 0):
            row.append("+")
        else:
            row.append(".")
    rows.append(row)

# print_grid()

droplets = 0
while True:
    droplets = droplets + 1
    x, y, symbol = add_droplet()
    if y == 0:
        break
    set_cell(x, y, symbol)
    if droplets % 1000 == 0:
        print(droplets, y, max_y)

# print_grid()


count = 0
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        if get_cell(x, y) in ["~", "|"]:
            count = count + 1
print(count)

stable_count = 0
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        if get_cell(x, y) == "~":
            stable_count = stable_count + 1
        elif get_cell(x, y) == "|":
            if is_stable(x, y):
                set_cell(x, y, "~", True)
                stable_count = stable_count + 1
            else:
                set_cell(x, y, ".", True)
print_grid()
print(stable_count)
