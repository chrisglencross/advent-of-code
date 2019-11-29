import re

with open("input") as f:
    lines = f.readlines()

stars = []
for line in lines:
    # position=< 9,  1> velocity=< 0,  2>
    print("*", line.strip())
    match = re.search("^position=<([- 0-9]+), ([- 0-9]+)> velocity=<([- 0-9]+), ([- 0-9]+)>$", line.strip())
    x = int(match.group(1))
    y = int(match.group(2))
    dx = int(match.group(3))
    dy = int(match.group(4))
    stars.append(((x, y), (dx, dy)))
print(stars)


def get_grid_coords(stars):
    min_x = min([star[0][0] for star in stars])
    max_x = max([star[0][0] for star in stars])
    min_y = min([star[0][1] for star in stars])
    max_y = max([star[0][1] for star in stars])
    top_left = (min_x, min_y)
    bottom_right = (max_x, max_y)
    return top_left, bottom_right


def get_grid_size(top_left, bottom_right):
    return (bottom_right[0] - top_left[0]) * (bottom_right[1] - top_left[0])


def move_stars(stars):
    return [((star[0][0] + star[1][0], star[0][1] + star[1][1]), star[1]) for star in stars]


def print_stars(stars):
    top_left, bottom_right = get_grid_coords(stars)
    star_coords = set([star[0] for star in stars])
    for y in range(top_left[1], bottom_right[1] + 1):
        row = []
        for x in range(top_left[0], bottom_right[0] + 1):
            if (x, y) in star_coords:
                row.append("*")
            else:
                row.append(" ")
        print("".join(row))


top_left, bottom_right = get_grid_coords(stars)
grid_size = get_grid_size(top_left, bottom_right)
min_grid_size = grid_size + 1
time = 0
while grid_size < min_grid_size:
    min_grid_size = grid_size
    prev_stars = stars
    stars = move_stars(stars)
    top_left, bottom_right = get_grid_coords(stars)
    grid_size = get_grid_size(top_left, bottom_right)
    time = time + 1

print(grid_size)
print_stars(prev_stars)
print(time - 1)
