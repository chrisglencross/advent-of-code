initial_state = "#...##.#...#..#.#####.##.#..###.#.#.###....#...#...####.#....##..##..#..#..#..#.#..##.####.#.#.###"

with open("input", "r") as f:
    lines = f.readlines()
rules = {}
for line in lines:
    sequence = line[0:5]
    result = line[9]
    rules[sequence] = result

iterations = 1000

padding = "." * 2 * iterations
state = padding + initial_state + padding
print(state)

total = 0

found = set()
for iteration in range(0, iterations):
    new_state = []
    new_state.extend([".", "."])
    for i in range(2, len(state) - 2):
        sequence = state[i - 2:i + 3]
        new_state.append(rules[sequence])
    new_state.extend([".", "."])
    state = "".join(new_state)
    dupe = state.strip(".") in found

    found.add(state.strip("."))
    # print(state)

    previous_total = total
    total = 0
    for i, c in enumerate(state):
        if c == '#':
            total = total + (i - len(padding))
    print(iteration + 1, "=>", total, total - previous_total, dupe, state.strip("."))
    delta = ((iteration + 1) * (total - previous_total)) - total
    print(delta)

print(102 * iterations + 1377)
print(102 * 50000000000 + 1377)
