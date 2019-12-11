with open("input") as f:
    line = f.readlines()[0].replace(" ", "\t")

banks = [int(value) for value in line.split("\t")]

seen = set()
messages = 0
while True:
    t = tuple(banks)
    if t in seen:
        # Part 1
        print(f"Repeat after {len(seen)}")
        # Part 2
        seen.clear()
        messages = messages + 1
        if messages == 2:
            break
    seen.add(tuple(banks))
    max_value = max(banks)
    current_index = banks.index(max_value)
    distribute = banks[current_index]
    banks[current_index] = 0
    while distribute > 0:
        current_index = (current_index + 1) % len(banks)
        banks[current_index] = banks[current_index] + 1
        distribute = distribute - 1
