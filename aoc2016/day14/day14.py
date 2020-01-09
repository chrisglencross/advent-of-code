#!/usr/bin/python3
# Advent of code 2016 day 14
# See https://adventofcode.com/2016/day/14
import binascii
import hashlib
import itertools
import re
from functools import lru_cache


@lru_cache(maxsize=2000)
def make_md5(data, rehash=0):
    data = data.encode()
    for i in range(0, rehash + 1):
        m = hashlib.md5()
        m.update(data)
        data = binascii.hexlify(m.digest())
    return data.decode()


def get_answer(salt, hashfunc):
    count = 0
    for i in itertools.count():
        result = hashfunc(salt + str(i))
        if match := re.search(r"(.)\1\1", result):
            find_sequence = match.group(1) * 5
            if any(hashfunc(salt + str(i + 1 + j)).find(find_sequence) >= 0 for j in range(0, 1000)):
                count += 1
                if count == 64:
                    return i


print("Part 1:", get_answer("qzyelonm", lambda data: make_md5(data)))
print("Part 2:", get_answer("qzyelonm", lambda data: make_md5(data, 2016)))
