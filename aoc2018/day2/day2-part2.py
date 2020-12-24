with open("input") as f:
    lines = [line.strip() for line in f.readlines()]

found = set()
for line in lines:
    for i in range(0, len(line)):
        chars = list(line)
        chars[i] = '*'
        s = "".join(chars)
        if s in found:
            print(s)
        found.add(s)
