#!/usr/bin/python3
# Advent of code 2016 day 5
# See https://adventofcode.com/2016/day/5
import binascii
import hashlib
import itertools


def make_md5(data):
    m = hashlib.md5()
    m.update(data.encode())
    result = m.digest()
    result = binascii.hexlify(result).decode()
    return result


# Part 1
password = ""
for i in itertools.count():
    m = make_md5("abbhdwsy" + str(i))
    if m.startswith("00000"):
        password += m[5]
        print(password)
        if len(password) == 8:
            break
print(password)

# Part 2
password = [None] * 8
count = 0
for i in itertools.count():
    m = make_md5("abbhdwsy" + str(i))
    if m.startswith("00000"):
        pos = int(m[5], 16)
        if pos < 8 and password[pos] is None:
            password[pos] = m[6]
            count += 1
            print(password)
            if count == 8:
                break
print("".join(password))
