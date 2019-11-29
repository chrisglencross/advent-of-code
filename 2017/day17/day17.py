#!/usr/bin/python3
# Advent of code 2017 day 17
# See https://adventofcode.com/2017/day/17

# Circular buffer which has a resizable buffer and a pointer to a current item.
# Set do_insert=False to prevent data actually getting inserted into the buffer, instead only tracking the first two
# data elements in the buffer, plus the virtual length and pointer. This optimisation is required for part 2.
class CircularBuffer:
    def __init__(self, do_insert=True):
        self.data = [0]
        self.current = 0
        self.len = 1
        self.do_insert = do_insert

    def forward(self, steps):
        self.current = (self.current + steps) % self.len

    def insert(self, value):
        if not self.do_insert and self.current == 0:
            self.data = [0, value]
        elif self.do_insert:
            self.data.insert(self.current + 1, value)
        self.len = self.len + 1
        self.current = self.current + 1

    def __str__(self):
        result = []
        for i, item in enumerate(self.data):
            if i == self.current:
                result.append(f"({item})")
            else:
                result.append(f"{item}")
        if not self.do_insert:
            result.append(f"(len={self.len}, current={self.current})")
        return " ".join(result)


# My input
step = 380

if __name__ == "__main__":

    # Part 1
    b = CircularBuffer()
    for i in range(1, 2017 + 1):
        b.forward(step)
        b.insert(i)
    print(b.data[b.current + 1])

    # Part 2
    b = CircularBuffer(do_insert=False)
    for i in range(1, 50000000 + 1):
        b.forward(step)
        b.insert(i)
        if i % 1000000 == 0:
            print(f"Progress: {(100 * i) // 50000000}%")
    print(b.data[1])
