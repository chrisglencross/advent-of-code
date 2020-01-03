#!/usr/bin/python3
# Advent of code 2015 day 4
# See https://adventofcode.com/2015/day/4
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
print(make_md5("abcdef609043"))

# Part 2
for counter in itertools.count():
    if make_md5("ckczppom" + str(counter)).startswith("000000"):
        print(counter)
        break
