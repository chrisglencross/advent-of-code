#!/usr/bin/python3
# Advent of code 2017 day 18
# See https://adventofcode.com/2017/day/18

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

    def op_snd(self, program):
        snd = self.arg1_val(program)
        program.out_queue.append(snd)
        program.out_count = program.out_count + 1
        print(f"{program.name} out queue length is {len(program.out_queue)}")

    def op_set(self, program):
        program.registers[self.arg1] = self.arg2_val(program)

    def op_add(self, program):
        program.registers[self.arg1] = self.arg1_val(program) + self.arg2_val(program)

    def op_mul(self, program):
        program.registers[self.arg1] = self.arg1_val(program) * self.arg2_val(program)

    def op_mod(self, program):
        program.registers[self.arg1] = self.arg1_val(program) % self.arg2_val(program)

    def op_rcv(self, program):
        # Part 1
        # if self.arg1_val(program) != 0:
        #     print(f"Recovered {program.out_queue.pop()}")
        #     exit(0)

        # Part 2
        if not program.in_queue:
            # print("Receive blocked")
            return 0  # blocked, stick with this instruction
        # print("Receive not blocked")
        program.registers[self.arg1] = program.in_queue.pop(0)

    def op_jgz(self, program):
        if self.arg1_val(program) > 0:
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
    out_queue: List[int] = field(default_factory=list)
    in_queue: List[int] = field(default_factory=list)
    out_count = 0

    def is_terminated(self):
        return self.pc < 0 or self.pc >= len(self.ops)

    def is_blocked(self):
        op = self.ops[self.pc]
        return op.op == "rcv" and len(self.in_queue) == 0

    def tick(self):
        if self.is_terminated():
            raise Exception(f"Program {self.name} terminated")
        op = self.ops[self.pc]
        # print(f"{self.name}@{self.pc}:\t{op.op} {op.arg1} {op.arg2}")
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

    # Part 2
    q0 = list()
    q1 = list()
    p0 = Program(name="p0", ops=ops, registers={"p": 0}, out_queue=q0, in_queue=q1)
    p1 = Program(name="p1", ops=ops, registers={"p": 1}, out_queue=q1, in_queue=q0)
    while True:
        if p0.is_terminated() and p1.is_terminated():
            print("Both threads terminated")
            break
        if p0.is_blocked() and p1.is_blocked():
            print("Deadlock")
            break
        if not p0.is_terminated():
            p0.tick()
        if not p1.is_terminated():
            p1.tick()

    print(p1.out_count)
