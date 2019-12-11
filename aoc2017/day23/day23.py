#!/usr/bin/python3
# Advent of code 2017 day 23
# See https://adventofcode.com/2017/day/23


import re
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Op:
    op: str
    arg1: str
    arg2: str

    def dispatch(self, program):
        fn = getattr(self, "op_" + self.op)
        return fn(program)

    def op_set(self, program):
        program.registers[self.arg1] = self.arg2_val(program)

    def op_sub(self, program):
        program.registers[self.arg1] = self.arg1_val(program) - self.arg2_val(program)

    def op_mul(self, program):
        program.registers[self.arg1] = self.arg1_val(program) * self.arg2_val(program)
        program.mul_count = program.mul_count + 1

    def op_jnz(self, program):
        if self.arg1_val(program) != 0:
            return self.arg2_val(program)
        else:
            return None

    def arg1_val(self, program):
        try:
            return int(self.arg1)
        except ValueError:
            return program.registers.get(self.arg1, 0)

    def arg2_val(self, program):
        try:
            return int(self.arg2)
        except ValueError:
            return program.registers.get(self.arg2, 0)


@dataclass
class Program:
    ops: List[Op]
    name: str = "p"
    pc: int = 0
    registers: Dict[str, int] = field(default_factory=dict)
    mul_count: int = 0

    def is_terminated(self):
        return self.pc < 0 or self.pc >= len(self.ops)

    def is_blocked(self):
        op = self.ops[self.pc]
        return op.op == "rcv" and len(self.in_queue) == 0

    def tick(self):
        if self.is_terminated():
            raise Exception(f"Program {self.name} terminated")
        op = self.ops[self.pc]
        print(f"{self.name}@{self.pc + 1}:\t{op.op} {op.arg1} {op.arg2}\t{self.registers}")
        jmp = op.dispatch(self)
        if jmp is not None:
            self.pc = self.pc + jmp
        else:
            self.pc = self.pc + 1


if __name__ == "__main__":

    with open("input.txt") as f:
        lines = f.readlines()

    ops = []
    for line in lines:
        match = re.search("^([a-z]+) ([-a-z0-9]+)( ([-a-z0-9]+))?$", line.strip())
        if match:
            op = match.group(1)
            arg1 = match.group(2)
            arg2 = match.group(4)
            ops.append(Op(op=op, arg1=arg1, arg2=arg2))
        else:
            raise Exception("Bad input: " + line)

    # Part 1
    # p = Program(ops=ops)
    # while not p.is_terminated():
    #     p.tick()
    # print(p.mul_count)

    # Part 2
    p = Program(ops=ops, registers={"a": 1})
    while not p.is_terminated():
        p.tick()
        if p.pc + 1 == 23:
            print("g", p.registers["g"])
            input()
    print(p.registers["h"])
