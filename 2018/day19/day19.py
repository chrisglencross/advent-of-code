import re

IP = 0
IP_BIND = None
R = [0, 0, 0, 0, 0, 0]


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


def find_opcode(name):
    for op_code in op_codes:
        if name == op_code.__name__:
            return op_code
    raise Exception("Unknown opcode: " + name)


def dispatch(instr):
    pre_R = list(R)  # debugging only
    op_code = find_opcode(instr[0])
    op_code(instr[1], instr[2], instr[3])

    if R[0] != pre_R[0]:
        print(f"ip={IP}\t{op_code.__name__} {instr[1]} {instr[2]} {instr[3]} : {pre_R}\t=> {R}")


with open("input") as f:
    lines = f.readlines()

# Execute samples and filter possible instructions for each opcode
instrs = []
for line in lines:
    if line[0] == "#":
        if IP_BIND is not None:
            raise Exception("Cannot rebind IP")
        IP_BIND = int(line.split(" ")[1])
    else:
        match = re.search("([^ ]+) ([0-9]+) ([0-9]+) ([0-9]+).*", line)
        if match is not None:
            instr = [match.group(1), int(match.group(2)), int(match.group(3)), int(match.group(4))]
            instrs.append(instr)
        else:
            raise ("Unknown instruction: " + line)

R[0] = 1
IP = 0
while IP >= 0 and IP < len(instrs):
    instr = instrs[IP]
    R[IP_BIND] = IP
    # if IP == 4:
    #     R[4] = R[1]
    #     R[5] = R[1] # Fast forward the loop to the end

    # if IP == 13 and R[3] == 2:
    #     R[3] = R[1] + 1  # Fast forward the next loop

    dispatch(instr)
    IP = R[IP_BIND]
    IP = IP + 1
    # input("Press a key")

print(R[0])
