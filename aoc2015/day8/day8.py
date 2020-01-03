#!/usr/bin/python3
# Advent of code 2015 day 8
# See https://adventofcode.com/2015/day/8


with open("input.txt") as f:
    lines = f.readlines()


def escape(line):
    output = ['"']
    i = 0
    while i < len(line):
        c = line[i]
        if c in '"\\':
            output.append('\\')
            output.append(c)
        else:
            output.append(c)
        i += 1
    output.append('"')
    return "".join(output)


def unescape(line):
    if line[0] != '"' or line[-1] != '"':
        raise Exception(f"Line {line} is not properly quoted")
    line = line[1:-1]

    output = []
    i = 0
    while i < len(line):
        c = line[i]
        if c == '\\':
            if line[i + 1] == 'x':
                ascii_hex = line[i + 2:i + 4]
                output.append(chr(int(ascii_hex, 16)))
                i += 4
            else:
                output.append(line[i + 1])
                i += 2
        else:
            output.append(c)
            i += 1

    return "".join(output)


diff = 0
for line in lines:
    line = line.strip()
    diff += len(line) - len(unescape(line))
print(diff)

print(escape("\"aaa\\\"aaa\""))
diff = 0
for line in lines:
    line = line.strip()
    diff += len(escape(line)) - len(line)
print(diff)
