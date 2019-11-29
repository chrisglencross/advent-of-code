with open("input") as f:
    lines = f.readlines()

found = set()
for line in lines:
    line = line.strip()
    for i in range(0, len(line)):
        chars = list(line)
        chars[i] = '*'
        s = "".join(chars)
        if s in found:
            print(s)
        found.add(s)
