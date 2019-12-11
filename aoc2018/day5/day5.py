with open("input") as f:
    lines = f.readlines()


def get_collapsed_length(new_line):
    line = None
    while new_line != line:
        line = new_line
        buffer = []
        skip = False
        for i in range(0, len(line)):
            if skip:
                skip = False
            else:
                c1 = line[i]
                if i == len(line) - 1:
                    c2 = None
                else:
                    c2 = line[i + 1]
                if c2 is not None and c1 != c2 and c1.upper() == c2.upper():
                    skip = True
                else:
                    buffer.append(c1)
                    skip = False
        new_line = "".join(buffer)
    return len(new_line)


sequence = lines[0].strip()
result = get_collapsed_length(sequence)
print(result)

letter_lengths = []
for i in range(65, 65 + 26):
    c = chr(i)
    result = get_collapsed_length(sequence.replace(c, "").replace(c.lower(), ""))
    print(c, result)
    letter_lengths.append({"c": c, "length": result})

letter_lengths.sort(key=lambda v: v["length"])
print(letter_lengths)
