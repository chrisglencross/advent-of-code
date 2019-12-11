#!/usr/bin/python3
# Advent of code 2017 day 8
# See https://adventofcode.com/2017/day/8

import re
from dataclasses import dataclass


@dataclass
class Instruction:
    register: str
    opcode: str
    value: int
    cond_register: str
    cond: str
    cond_value: int

    def evaluate_condition(self, registers):
        cond_register_value = registers.get(self.cond_register, 0)
        if self.cond == "==":
            return cond_register_value == self.cond_value
        elif self.cond == "<":
            return cond_register_value < self.cond_value
        elif self.cond == ">":
            return cond_register_value > self.cond_value
        elif self.cond == "<=":
            return cond_register_value <= self.cond_value
        elif self.cond == ">=":
            return cond_register_value >= self.cond_value
        elif self.cond == "!=":
            return cond_register_value != self.cond_value
        else:
            raise Exception("Unrecognized condition " + self.cond)

    def apply(self, registers):
        if self.evaluate_condition(registers):
            add_value = self.value
            if self.opcode == "inc":
                registers[self.register] = registers.get(self.register, 0) + self.value
            elif self.opcode == "dec":
                registers[self.register] = registers.get(self.register, 0) - self.value
            else:
                raise Exception("Unrecognized opcode " + self.opcode)


registers = {}
instructions = []
max_value = 0

if __name__ == "__main__":

    with open("input.txt") as f:
        lines = f.readlines()

    for line in lines:
        if not line.strip():
            continue
        # b inc 5 if a > 1
        match = re.search("^([A-Za-z]+) (inc|dec) ([-0-9]+) if ([A-Za-z]+) (.+) ([-0-9]+)$", line.strip())
        if not match:
            raise Exception("Cannot parse " + line.strip())

        instructions.append(
            Instruction(register=match.group(1),
                        opcode=match.group(2),
                        value=int(match.group(3)),
                        cond_register=match.group(4),
                        cond=match.group(5),
                        cond_value=int(match.group(6))))

    for instruction in instructions:
        print(instruction)
        instruction.apply(registers)
        max_value = max(max_value, max(registers.values()))

    print(max(registers.values()))
    print(max_value)
