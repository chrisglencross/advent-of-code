# Possible moves in order of preference (reading order)
moves = [(0, -1), (-1, 0), (1, 0), (0, 1)]


# elf_attack_power = 8
# elf_attack_power = 3

def get_initial_cell(symbol):
    if symbol == 'E':
        return dict({"symbol": symbol, "hp": 200, "attack": elf_attack_power})
    elif symbol == 'G':
        return dict({"symbol": symbol, "hp": 200, "attack": 3})
    else:
        return dict({"symbol": symbol})


def get_enemy_symbol(symbol):
    if symbol == 'E':
        return 'G'
    elif symbol == 'G':
        return 'E'
    else:
        raise Exception("Unknown symbol " + symbol)


def find_movement_targets(enemy_symbol):
    results = set()
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            if cell["symbol"] == enemy_symbol:
                for move in moves:
                    if rows[y + move[1]][x + move[0]]["symbol"] == '.':
                        results.add((x + move[0], y + move[1]))
    return results


# Flood fill to find the nearest target
def find_nearest_target(start_x, start_y, targets):
    drows = create_empty_grid()
    modified = True
    possible_nearest_targets = []
    iteration = 0
    drows[start_y][start_x] = iteration
    while len(possible_nearest_targets) == 0 and modified:
        modified = False
        # print_distances(drows)
        for y, row in enumerate(rows):
            for x, cell in enumerate(row):
                d = drows[y][x]
                if d == iteration:
                    if (x, y) in targets:
                        possible_nearest_targets.append((x, y))
                    for move in moves:
                        if rows[y + move[1]][x + move[0]]["symbol"] == '.' and drows[y + move[1]][x + move[0]] is None:
                            drows[y + move[1]][x + move[0]] = d + 1
                            modified = True
        iteration = iteration + 1

    # print_distances(drows)

    if len(possible_nearest_targets) == 0:
        return -1, -1
    # Sort into reading order
    possible_nearest_targets.sort(key=lambda target: target[1] * 100000 + target[0])
    return possible_nearest_targets[0]


def create_empty_grid():
    drows = []
    for row in rows:
        drow = []
        for cell in row:
            drow.append(None)
        drows.append(drow)
    return drows


def find_next_step(from_x, from_y, target_x, target_y):
    # Walk backwards from destination to an adjacent cell and find the closest
    adjacent_cells = []
    for move in moves:
        if rows[from_y + move[1]][from_x + move[0]]["symbol"] == ".":
            adjacent_cells.append((from_x + move[0], from_y + move[1]))
    return find_nearest_target(target_x, target_y, adjacent_cells)


# Returns the coords of the adjacent enemy with the lowest hp
def find_adjacent_enemy(from_x, from_y, enemy_symbol):
    adjacent_enemies = []
    for move in moves:
        if rows[from_y + move[1]][from_x + move[0]]["symbol"] == enemy_symbol:
            adjacent_enemies.append((from_x + move[0], from_y + move[1]))
    if len(adjacent_enemies) == 0:
        return -1, -1
    adjacent_enemies.sort(
        key=lambda coords: rows[coords[1]][coords[0]]["hp"] * 100000000 + coords[1] * 10000 + coords[0])
    return adjacent_enemies[0]


def move(from_x, from_y, mover):
    symbol = mover["symbol"]
    print(f"Starting move of {symbol} at {from_x}, {from_y}")
    enemy_symbol = get_enemy_symbol(symbol)
    target_x, target_y = find_adjacent_enemy(from_x, from_y, enemy_symbol)
    if target_x != -1:
        # adjacent to enemy: do not want to move
        return from_x, from_y
    movement_targets = find_movement_targets(enemy_symbol)
    target_x, target_y = find_nearest_target(from_x, from_y, movement_targets)
    print(f"Nearest target to {symbol} {from_x}, {from_y} is {target_x}, {target_y}")
    if target_x == -1:
        # Cannot move
        return from_x, from_y
    print(f"Finding next step:")
    next_x, next_y = find_next_step(from_x, from_y, target_x, target_y)
    rows[from_y][from_x] = get_initial_cell(".")
    rows[next_y][next_x] = mover
    print(f"Next step is to {next_x}, {next_y}")
    return next_x, next_y


def attack(from_x, from_y, attacker):
    symbol = attacker["symbol"]
    print(f"Starting attack of {symbol} at {from_x}, {from_y}")
    enemy_symbol = get_enemy_symbol(symbol)
    target_x, target_y = find_adjacent_enemy(from_x, from_y, enemy_symbol)
    if target_x == -1:
        # No adjacent enemy
        return
    enemy = rows[target_y][target_x]
    enemy["hp"] = enemy["hp"] - attacker["attack"]
    if enemy["hp"] <= 0:
        print(f"Killed enemy {enemy_symbol} at {target_x}, {target_y}")
        rows[target_y][target_x] = get_initial_cell(".")


def distance_str(x, y, d):
    if d is None:
        return rows[y][x]["symbol"]
    return str(d)


def print_distances(drows):
    for y, drow in enumerate(drows):
        print("".join([distance_str(x, y, d) for x, d in enumerate(drow)]))


def print_grid():
    for row in rows:
        map_line = "".join([cell["symbol"] for cell in row])
        stats = "  ".join([f'{cell["symbol"]}={cell["hp"]}' for cell in row if cell["symbol"] in ["E", "G"]])
        print(map_line + "   " + stats)


def get_symbol_counts(symbols):
    result = dict()
    for symbol in symbols:
        result[symbol] = 0
    for row in rows:
        for cell in row:
            symbol = cell["symbol"]
            if symbol in symbols:
                result[symbol] = result[symbol] + 1
    return result


def finished():
    return 0 in get_symbol_counts({'E', 'G'}).values()


for elf_attack_power in range(4, 10000):

    rows = []
    with open("input") as f:
        for line in f.readlines():
            rows.append([get_initial_cell(symbol) for symbol in line.replace("\n", "")])

    print_grid()
    initial_elf_count = get_symbol_counts({"E"})["E"]

    turn = 0
    finished_early = False
    while not finished():
        if get_symbol_counts({"E"})["E"] < initial_elf_count:
            print("Elf died")
            break
        already_moved = set()
        finished_early = False
        for y, row in enumerate(rows):
            for x, cell in enumerate(row):
                symbol = cell["symbol"]
                if symbol in ['E', 'G']:
                    if (x, y) in already_moved:
                        pass  # Moved into this cell this turn
                    else:
                        if finished():
                            finished_early = True
                        new_x, new_y = move(x, y, cell)
                        already_moved.add((new_x, new_y))
                        attack(new_x, new_y, rows[new_y][new_x])
        turn = turn + 1
        print(f"After turn {turn}")
        if finished_early:
            print("(Partial turn)")
        print_grid()

    if finished_early:
        turn = turn - 1

    if get_symbol_counts({"E"})["E"] == initial_elf_count:
        print("Completed with no elf dying: attack=" + str(elf_attack_power))
        break

print(f"Battle completed after {turn} full rounds")
total_hp = 0
for row in rows:
    for cell in row:
        if cell["symbol"] in ['E', 'G']:
            total_hp = total_hp + cell["hp"]

print(f"Total HP remaining is {total_hp}")
print(f"Result is {total_hp * (turn)}")
