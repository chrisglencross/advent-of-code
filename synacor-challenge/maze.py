# Breadth first search through the grid to find the shortest route to the end with value 30

maze = [
    ["*", 8, "-", 1],
    [4, "*", 11, "*"],
    ["+", 4, "-", 18],
    [22, "-", 9, "*"]
]


def find_path(paths):
    depth = 0
    while paths:
        depth += 1
        print(f"Depth {depth} has {len(paths)} paths")
        new_paths = []
        for x, y, total, operator, path in paths:
            if x == 0 and y == 3:
                pass  # resets if you go back to start
            else:

                if operator is None:
                    new_operator = maze[y][x]
                    new_total = total
                else:
                    new_operator = None
                    value = maze[y][x]
                    if operator == "+":
                        new_total = total + value
                    elif operator == "-":
                        new_total = total - value
                    elif operator == "*":
                        new_total = total * value
                    else:
                        raise ValueError(f"Bad operator {operator}")

                if x == 3 and y == 0:
                    if new_total == 30:
                        return path

                elif new_total > 0:
                    adjacent = []
                    if x > 0:
                        adjacent.append((x - 1, y, 'west'))
                    if x < 3:
                        adjacent.append((x + 1, y, 'east'))
                    if y > 0:
                        adjacent.append((x, y - 1, 'north'))
                    if y < 3:
                        adjacent.append((x, y + 1, 'south'))

                    for new_x, new_y, dir in adjacent:
                        new_path = list(path)
                        new_path.append((x, y, maze[y][x], new_total, dir))
                        new_paths.append((new_x, new_y, new_total, new_operator, new_path))

        paths = new_paths


pp = find_path(
    [(0, 2, 22, None, [(0, 3, 22, 22, 'north')]),
     (1, 3, 22, None, [(0, 3, 22, 22, 'east')])])
for p in pp:
    print(p[4])

# Route through maze is:
# north
# east
# east
# north
# west
# south
# east
# east
# west
# north
# north
# east
