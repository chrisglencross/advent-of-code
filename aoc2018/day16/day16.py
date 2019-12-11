import re

R = [0, 0, 0, 0]


def addr(ra, rb, rc):
    R[rc] = R[ra] + R[rb]


def addi(ra, b, rc):
    R[rc] = R[ra] + b


def mulr(ra, rb, rc):
    R[rc] = R[ra] * R[rb]


def muli(ra, b, rc):
    R[rc] = R[ra] * b


def banr(ra, rb, rc):
    R[rc] = R[ra] & R[rb]


def bani(ra, b, rc):
    R[rc] = R[ra] & b


def borr(ra, rb, rc):
    R[rc] = R[ra] | R[rb]


def bori(ra, b, rc):
    R[rc] = R[ra] | b


def setr(ra, rb, rc):
    R[rc] = R[ra]


def seti(a, b, rc):
    R[rc] = a


def gtir(a, rb, rc):
    if a > R[rb]:
        R[rc] = 1
    else:
        R[rc] = 0


def gtri(ra, b, rc):
    if R[ra] > b:
        R[rc] = 1
    else:
        R[rc] = 0


def gtrr(ra, rb, rc):
    if R[ra] > R[rb]:
        R[rc] = 1
    else:
        R[rc] = 0


def eqir(a, rb, rc):
    if a == R[rb]:
        R[rc] = 1
    else:
        R[rc] = 0


def eqri(ra, b, rc):
    if R[ra] == b:
        R[rc] = 1
    else:
        R[rc] = 0


def eqrr(ra, rb, rc):
    if R[ra] == R[rb]:
        R[rc] = 1
    else:
        R[rc] = 0


op_codes = [
    addr,
    addi,
    mulr,
    muli,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtir,
    gtri,
    gtrr,
    eqir,
    eqri,
    eqrr
]


def dispatch(op_code, instr):
    input_r = list(R)
    op_code(instr[1], instr[2], instr[3])
    print(op_code.__name__, instr[1], instr[2], instr[3], ":", input_r, "=>", R)


def get_possible_opcodes(input_r, instr, expected_output_r):
    global R
    print(f"Executing {instr} with input {input_r} expecting {expected_output_r}")
    result = set()
    for op_code in op_codes:
        R = list(input_r)
        dispatch(op_code, instr)
        output_r = list(R)

        if output_r == expected_output_r:
            result.add(op_code)

    print(f"   => {result} matched")
    return result


with open("input-part1") as f:
    lines = f.readlines()

# Start off with any opcode possibly mapping any instruction
op_code_mapping = dict()
for i in range(0, 16):
    op_code_mapping[i] = set(op_codes)

# Execute samples and filter possible instructions for each opcode
for line in lines:
    # Before: [1, 1, 2, 1]
    match = re.search("Before: \\[([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+)\\]", line)
    if match is not None:
        input_r = [int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))]

    # 1 2 3 4
    match = re.search("([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)", line)
    if match is not None:
        current_instr = [int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))]

    match = re.search("After: +\\[([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+)\\]", line)
    if match is not None:
        expected_output_r = [int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))]
        possible_opcodes = get_possible_opcodes(input_r, current_instr, expected_output_r)
        op_code_mapping[current_instr[0]].intersection_update(possible_opcodes)

# Sudoku-ish removal of items - no more than one opcode per instruction
modified = True
while modified:
    modified = False
    for key, values in op_code_mapping.items():
        if len(values) == 1:
            value_to_remove = list(values)[0]
            for key2, values2 in op_code_mapping.items():
                if key2 != key and value_to_remove in values2:
                    values2.remove(value_to_remove)
                    modified = True

# Execute the program
for key, values in op_code_mapping.items():
    print(f"{key}:\t{', '.join([value.__name__ for value in values])}")

with open("input-part2") as f:
    lines = f.readlines()

# Does this matter?
R = [0, 0, 0, 0]
for line in lines:
    match = re.search("([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)", line)
    if match is not None:
        current_instr = [int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))]
        op_code = list(op_code_mapping[current_instr[0]])[0]
        dispatch(op_code, current_instr)

print(R)
