with open("input") as f:
    lines = f.readlines()

offsets = [int(line) for line in lines]
ip = 0
steps = 0
while 0 <= ip < len(offsets):
    # print(ip, offsets)
    steps = steps + 1
    offset = offsets[ip]
    if offset >= 3:
        offsets[ip] = offset - 1
    else:
        offsets[ip] = offset + 1
    ip = ip + offset

print(ip, offsets)
print(steps)
