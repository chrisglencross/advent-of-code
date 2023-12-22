#!/usr/bin/python3
# Advent of code 2023 day 20
# See https://adventofcode.com/2023/day/20
import collections
import itertools
import math
from collections import defaultdict

import aoc2023.modules as aoc
aoc.download_input("2023", "20")

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

modules = {}
for line in lines:
    module, targets_str = line.split(" -> ")
    if module[0] in "%&":
        type, module = module[0], module[1:]
    else:
        type = module
    targets = targets_str.split(", ")
    modules[module] = [type, targets]


def push_button():
    global low_pulses, high_pulses
    outputs = collections.defaultdict(lambda: list())
    queue = [("button", "broadcaster", False)]
    while queue:
        new_queue = []
        for source, module, is_high in queue:
            if is_high:
                high_pulses += 1
            else:
                low_pulses += 1
            if module not in modules.keys():
                outputs[module].append(is_high)
                continue
            module_state = modules[module]
            type, targets = module_state
            if type == "broadcaster":
                send_high = is_high
                for target in targets:
                    new_queue.append((module, target, send_high))
            elif type == "%":
                is_on = flipflop_states[module]
                if not is_high:
                    new_is_on = not is_on
                    flipflop_states[module] = new_is_on
                    send_high = new_is_on
                    for target in targets:
                        new_queue.append((module, target, send_high))
                else:
                    send_high = None
            elif type == "&":
                received = conjunction_messages[module]
                received[source] = is_high
                send_high = not all(received.values())
                for target in targets:
                    new_queue.append((module, target, send_high))
            outputs[module].append(send_high)
        queue = new_queue
    return dict(outputs)

def new_conjuntion_messages():
    conjunction_messages = defaultdict(lambda: dict())
    for module, (type, targets) in modules.items():
        for target in targets:
            if target in modules.keys():
                target_module_type = modules[target][0]
                if target_module_type == "&":
                    conjunction_messages[target][module] = False
    return conjunction_messages

# This is too slow to run on the entire test data.
#
# Instead visualize the test data with graphviz and note that it's actually 4 separate
# circuits which implement counters with a periodic pulse at the end, and the final output is an AND
# gate that pulses when all 4 circuits pulse at the same time. Running the process for the individual circuits
# we see the pulses are at 3947, 4007, 4019, 3943. Therefore the solution is the lcm.

print(math.lcm(3947, 4007, 4019, 3943))



flipflop_states = defaultdict(lambda: False)
conjunction_messages = new_conjuntion_messages()
low_pulses = high_pulses = 0
for i in itertools.count(1):
    if i % 100_000 == 0:
        print(i)
    outputs = push_button()
    if not all(outputs["rx"]):
        print(i, outputs["rx"])
print(low_pulses, high_pulses, low_pulses*high_pulses)



def find_modules_with_target(target):
    result = []
    for source, (type, targets) in modules.items():
        if target in targets:
            result.append((type, source))
    return result
