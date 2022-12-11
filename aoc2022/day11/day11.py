#!/usr/bin/python3
# Advent of code 2022 day 11
# See https://adventofcode.com/2022/day/11

class Monkey:
    def __init__(self, starting_items, operation_fn, target_fn):
        self.items = starting_items
        self.operation_fn = operation_fn
        self.target_fn = target_fn
        self.inspected = 0

    def get_targets(self, part1):
        items = list(self.items)
        self.items = []
        targets = []
        for old in items:
            self.inspected += 1
            new = self.operation_fn(old)
            if part1:
                new = new // 3
            target = self.target_fn(new)
            targets.append((target, new))
        return targets


monkeys = [
    Monkey([66, 71, 94],
           lambda old: old * 5,
           lambda x: 7 if x % 3 == 0 else 4),
    Monkey([70],
           lambda old: old + 6,
           lambda x: 3 if x % 17 == 0 else 0),
    Monkey([62, 68, 56, 65, 94, 78],
           lambda old: old + 5,
           lambda x: 3 if x % 2 == 0 else 1),
    Monkey([89, 94, 94, 67],
           lambda old: old + 2,
           lambda x: 7 if x % 19 == 0 else 0),
    Monkey([71, 61, 73, 65, 98, 98, 63],
           lambda old: old * 7,
           lambda x: 5 if x % 11 == 0 else 6),
    Monkey([55, 62, 68, 61, 60],
           lambda old: old + 7,
           lambda x: 2 if x % 5 == 0 else 1),
    Monkey([93, 91, 69, 64, 72, 89, 50, 71],
           lambda old: old + 1,
           lambda x: 5 if x % 13 == 0 else 2),
    Monkey([76, 50],
           lambda old: old * old,
           lambda x: 4 if x % 7 == 0 else 6),
]

# Use modular arithmetic to stop worry levels getting too high
m = 3 * 17 * 2 * 19 * 11 * 5 * 13 * 7


def process(part1, rounds):
    for round in range(0, rounds):
        for monkey_no, monkey in enumerate(monkeys):
            targets = monkey.get_targets(part1)
            for target, value in targets:
                monkeys[target].items.append(value % m)
    inspected = sorted([monkey.inspected for monkey in monkeys], reverse=True)
    return inspected[0] * inspected[1]


print(process(True, 20))
print(process(False, 10000))

