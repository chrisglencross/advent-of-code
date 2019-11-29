#!/usr/bin/python3
# Advent of code 2017 day 9
# See https://adventofcode.com/2017/day/9


def next_char(line):
    if line:
        return line[0], line[1:]
    else:
        return None, []


def garbage_next_char(line):
    next, line = next_char(line)
    while next == "!":
        # Skip the next character
        next, line = next_char(line)
        next, line = next_char(line)
    return next, line


def skip_garbage(line):
    garbage = []
    while True:
        next, line = garbage_next_char(line)
        if next == ">":
            return line, garbage
        else:
            garbage.append(next)


def score_block(depth, line):
    score = depth
    garbage = []
    next, line = next_char(line)
    while True:
        if next is None and depth == 0:
            return score, line, garbage
        elif next is None:
            raise Exception("Unexpected end of input; expected '}'")
        if next == "{":
            child_score, line, child_garbage = score_block(depth + 1, line)
            score = score + child_score
            garbage.extend(child_garbage)
        elif next == "}":
            return score, line, garbage
        elif next == "<":
            line, child_garbage = skip_garbage(line)
            garbage.extend(child_garbage)
        elif next == ",":
            pass
        else:
            raise Exception("Unexpected character in block: '" + next + "' (" + "".join(line) + " remaining)")
        next, line = next_char(line)


if __name__ == "__main__":

    with open("input.txt") as f:
        lines = f.readlines()

    for line in lines:
        line = line.replace("\n", "")
        print(line)
        score, remainder, garbage = score_block(0, line.strip())
        print("Score:", score, "Garbage count:", len(garbage))
