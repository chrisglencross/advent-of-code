import hashlib

with open("input") as f:
    lines = f.readlines()

rows = []
for line in lines:
    row = list(line.replace("\n", ""))
    rows.append(row)


def print_grid(rows):
    for row in rows:
        print("".join(row))
    print()


def checksum(rows):
    str = "".join([symbol for row in rows for symbol in row])
    hash = hashlib.sha1()
    hash.update(str.encode())
    return hash.digest()


def get_neighbour_counts(input, x, y):
    result = dict({"#": 0, ".": 0, "|": 0})
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            if y + dy < 0 or y + dy >= len(input):
                continue
            row = input[y + dy]
            if x + dx < 0 or x + dx >= len(row):
                continue
            symbol = input[y + dy][x + dx]
            result[symbol] = result[symbol] + 1
    return result


def iteration(input):
    output = []
    for y, row in enumerate(input):
        new_row = []
        for x, cell in enumerate(row):
            counts = get_neighbour_counts(input, x, y)
            symbol = input[y][x]
            new_symbol = symbol
            if symbol == "." and counts["|"] >= 3:
                new_symbol = "|"
            elif symbol == "|" and counts["#"] >= 3:
                new_symbol = "#"
            elif symbol == "#":
                if counts["#"] >= 1 and counts["|"] >= 1:
                    pass
                else:
                    new_symbol = "."
            new_row.append(new_symbol)
        output.append(new_row)
    return output


iterations = 1000000000
iterations_before_repeat = 563
interval_size = 598 - 563
intervals_to_skip = int((iterations - iterations_before_repeat) / interval_size)
start = (intervals_to_skip * interval_size)
print(start)

checksums = dict()
for i in range(start, 1000000000):
    rows = iteration(rows)
    ck = checksum(rows)
    if ck in checksums.keys():
        print(f"Iteration {i} repeats iteration {checksums[ck]}")

    else:
        checksums[ck] = i
    # print_grid(rows)

woods = sum([1 for row in rows for cell in row if cell == "|"])
lumberyards = sum([1 for row in rows for cell in row if cell == "#"])
print(woods * lumberyards)
