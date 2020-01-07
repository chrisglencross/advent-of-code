#!/usr/bin/python3
# Advent of code 2016 day 10
# See https://adventofcode.com/2016/day/10
import collections
import re
from dataclasses import dataclass
from typing import Optional

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


@dataclass
class Bot:
    low_type: str  # "bot" or "output"
    low_to: Optional[int]
    high_type: str  # "bot" or "output"
    high_to: Optional[int]
    holding: Optional[int] = None


bots = {}
bot_queue = []
outputs = collections.defaultdict(list)

for line in lines:
    if match := re.fullmatch(r"value (\d+) goes to bot (\d+)", line):
        bot_queue.append((int(match.group(2)), int(match.group(1))))
    elif match := re.fullmatch(r"bot (\d+) gives low to (.*) (\d+) and high to (.*) (\d+)", line):
        bots[int(match.group(1))] = Bot(low_type=match.group(2), low_to=int(match.group(3)),
                                        high_type=match.group(4), high_to=int(match.group(5)))

while bot_queue:
    bot_no, value = bot_queue.pop()
    bot = bots[bot_no]
    if bot.holding is None:
        bot.holding = value
    else:
        low, high = sorted([bot.holding, value])
        if [low, high] == [17, 61]:
            print("Part 1:", bot_no)
        if bot.low_type == "bot":
            bot_queue.append((bot.low_to, low))
        else:
            outputs[bot.low_to].append(low)
        if bot.high_type == "bot":
            bot_queue.append((bot.high_to, high))
        else:
            outputs[bot.high_to].append(high)
        bot.holding = None

print("Part 2:", outputs[0][0] * outputs[1][0] * outputs[2][0])
