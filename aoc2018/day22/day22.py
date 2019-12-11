# depth=510
# target=(10, 10)

depth = 11991
target = (6, 797)

# We really want an expandable grid...
# Set a fixed maximum
max_x = target[0] + 200
max_y = target[1] + 500


def empty_grid():
    rows = []
    for y in range(0, max_y + 1):
        rows.append([None] * (max_x + 1))
    return rows


erosion_levels = empty_grid()
risk_levels = empty_grid()


def get_geologic_index(coords):
    if coords == (0, 0):
        return 0
    if coords == target:
        return 0
    x = coords[0]
    y = coords[1]
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    return erosion_levels[y][x - 1] * erosion_levels[y - 1][x]


def get_risk_level(coords):
    geologic_index = get_geologic_index(coords)
    erosion_level = (geologic_index + depth) % 20183
    x = coords[0]
    y = coords[1]
    erosion_levels[y][x] = erosion_level
    risk_level = erosion_level % 3
    risk_levels[y][x] = risk_level
    return risk_level


# Part 1
# total_risk_level = 0
# for y in range(0, target[1] + 1):
#     for x in range(0, target[0] + 1):
#         total_risk_level = total_risk_level + get_risk_level((x, y))
# print(total_risk_level)

# Part 2

# Precalculate risk levels
for y in range(0, max_y + 1):
    for x in range(0, max_x + 1):
        get_risk_level((x, y))


def get_allowable_equip(coords):
    current_risk_level = risk_levels[coords[1]][coords[0]]
    if current_risk_level == 0:  # Rocky
        return ["climbing", "torch"]
    if current_risk_level == 1:  # Wet
        return ["climbing", "neither"]
    if current_risk_level == 2:
        return ["torch", "neither"]
    raise Exception("Unknown risk level: " + str(current_risk_level))


class Move:
    def __init__(self, name, move, equip, cost):
        self.name = name;
        self.move = move
        self.equip = equip
        self.cost = cost


all_moves = [
    Move("equip neither", None, "neither", 7),
    Move("equip torch", None, "torch", 7),
    Move("equip climbing", None, "climbing", 7),
    Move("up", (0, -1), None, 1),
    Move("left", (-1, 0), None, 1),
    Move("right", (1, 0), None, 1),
    Move("down", (0, 1), None, 1),
]


class State:

    def __init__(self, coords, equip):
        self.coords = coords
        self.equip = equip

    # Returns a tuple of move + next state
    def next_states(self):
        result = []
        allowable_equip = get_allowable_equip(self.coords)
        for move in all_moves:
            if move.equip is not None and move.equip in allowable_equip:
                result.append((move, State(self.coords, move.equip)))
            elif move.move is not None:
                new_coords = (self.coords[0] + move.move[0], self.coords[1] + move.move[1])
                if 0 <= new_coords[0] < max_x and 0 <= new_coords[1] < max_y:
                    allowable_equip = get_allowable_equip(new_coords)
                    if self.equip in allowable_equip:
                        result.append((move, State(new_coords, self.equip)))
        return result

    def __str__(self):
        return f"{self.coords}:{self.equip}"


state_scores = dict()

initial_state = State((0, 0), "torch")
state_scores[str(initial_state)] = 0
dirty_states = {initial_state}
best_target_score = None

while dirty_states:
    new_dirty_states = set()
    for state in dirty_states:
        print(f"Scanning from {state}")
        current_score = state_scores[str(state)]
        for move, next_state in state.next_states():
            new_score = current_score + move.cost
            # No point carrying on if we've already got to target with a better score
            if best_target_score is None or new_score < best_target_score:
                best_score = state_scores.get(str(next_state))
                # Reached this point with a new best score
                if best_score is None or best_score > new_score:
                    state_scores[str(next_state)] = new_score
                    new_dirty_states.add(next_state)
                    # print(new_score)
                    if next_state.coords == target and next_state.equip == "torch":
                        best_target_score = new_score
                        print(new_score)
    dirty_states = new_dirty_states

print(best_target_score)
