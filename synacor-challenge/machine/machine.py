import inspect
import json
import re
from dataclasses import dataclass
from typing import List, Callable

import jsonpickle as jsonpickle

OP_CODES = {}


@dataclass
class OpCode:
    name: str
    code: int
    size: int
    fn: Callable[..., type(None)]
    params: List[str]


def opcode(code):
    def register(func):
        params = list(inspect.signature(func).parameters)
        OP_CODES[code] = OpCode(func.__name__.replace("op_", ""), code, len(params) - 1, func, params)
        return func

    return register


class Machine:

    def __init__(self, program):
        self.pc = 0
        self.instr_pc = 0
        self.memory = [0] * 32768
        for addr, value in enumerate(program):
            self.memory[addr] = value
        self.registers = [0] * 8
        self.stack = []
        self.halted = False
        self.input_buffer = []
        self.modified = {}
        self.trace = False
        self.assist = False

    def run(self):
        while not self.halted:
            self.step()

    def step(self):
        self.instr_pc = self.pc
        code = self.memory[self.pc]
        self.pc += 1
        instr = OP_CODES.get(code)
        if instr is None:
            raise ValueError(f"Invalid opcode {code} at address {self.instr_pc}")
        params = []
        param_names = []
        for i in range(0, instr.size):
            param = self.memory[self.pc]
            params.append(param)

            if param >= 32768:
                param_names.append(f"r{param - 32768}")
            else:
                param_names.append(param)

            self.pc += 1

        instr.fn(self, *params)
        if self.trace:
            print(self.instr_pc, instr.name, param_names)

    def disassemble(self, addr):
        start_addr = addr
        code = self.memory[addr]
        addr += 1
        instr = OP_CODES.get(code)
        if instr is None:
            raise ValueError(f"Invalid opcode {code} at address {self.instr_pc}")
        params = []
        for i in range(0, instr.size):
            param = self.memory[addr]
            if param >= 32768:
                param = f"r{param - 32768}"
            params.append(param)
            addr += 1
        print(start_addr, instr.name, params)
        return addr

    def rvalue(self, value):
        if 0 <= value <= 32767:
            return value
        elif 32768 <= value <= 32775:
            return self.registers[value - 32768]
        else:
            raise ValueError(f"Invalid rvalue: {value}")

    def set_address(self, address, value):
        if self.get_address(address) != value:
            self.modified[address] = value
        if address < 32768:
            self.memory[address] = value
        elif address < 32776:
            self.registers[address - 32768] = value
        else:
            raise ValueError(f"Invalid address: {address}")

    def get_address(self, address):
        if address == 3953 and self.instr_pc != 4417 and self.instr_pc != 4431:
            print(f"Reading address {address} at {self.instr_pc}")
        if address < 32768:
            return self.memory[address]
        elif address < 32776:
            return self.registers[address - 32768]
        else:
            raise ValueError(f"Invalid address: {address}")

    # halt: 0
    # stop execution and terminate the program
    @opcode(code=0)
    def op_halt(self):
        self.halted = True

    # set: 1 a b
    #   set register <a> to the value of <b>
    @opcode(code=1)
    def op_set(self, a, b):
        self.set_address(a, self.rvalue(b))

    # push: 2 a
    #   push <a> onto the stack
    @opcode(code=2)
    def op_push(self, a):
        self.stack.append(self.rvalue(a))

    # pop: 3 a
    #   remove the top element from the stack and write it into <a>; empty stack = error
    @opcode(code=3)
    def op_pop(self, a):
        self.set_address(a, self.stack.pop())

    # eq: 4 a b c
    #   set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
    @opcode(code=4)
    def op_eq(self, a, b, c):
        self.set_address(a, 1 if self.rvalue(b) == self.rvalue(c) else 0)

    # gt: 5 a b c
    #   set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
    @opcode(code=5)
    def op_gt(self, a, b, c):
        self.set_address(a, 1 if self.rvalue(b) > self.rvalue(c) else 0)

    # jmp: 6 a
    #   jump to <a>
    @opcode(code=6)
    def op_jmp(self, a):
        self.pc = self.rvalue(a)

    # jt: 7 a b
    #   if <a> is nonzero, jump to <b>
    @opcode(code=7)
    def op_jt(self, a, b):
        if self.rvalue(a) != 0:
            self.pc = self.rvalue(b)

    # jf: 8 a b
    #   if <a> is zero, jump to <b>
    @opcode(code=8)
    def op_jf(self, a, b):
        if self.rvalue(a) == 0:
            self.pc = self.rvalue(b)

    # add: 9 a b c
    #   assign into <a> the sum of <b> and <c> (modulo 32768)
    @opcode(code=9)
    def op_add(self, a, b, c):
        self.set_address(a, (self.rvalue(b) + self.rvalue(c)) % 32768)

    # mult: 10 a b c
    #   store into <a> the product of <b> and <c> (modulo 32768)
    @opcode(code=10)
    def op_mult(self, a, b, c):
        self.set_address(a, (self.rvalue(b) * self.rvalue(c)) % 32768)

    # mod: 11 a b c
    #   store into <a> the remainder of <b> divided by <c>
    @opcode(code=11)
    def op_mod(self, a, b, c):
        self.set_address(a, self.rvalue(b) % self.rvalue(c))

    # and: 12 a b c
    #   stores into <a> the bitwise and of <b> and <c>
    @opcode(code=12)
    def op_and(self, a, b, c):
        self.set_address(a, self.rvalue(b) & self.rvalue(c))

    # or: 13 a b c
    #   stores into <a> the bitwise or of <b> and <c>
    @opcode(code=13)
    def op_or(self, a, b, c):
        self.set_address(a, self.rvalue(b) | self.rvalue(c))

    # not: 14 a b
    #   stores 15-bit bitwise inverse of <b> in <a>
    @opcode(code=14)
    def op_not(self, a, b):
        self.set_address(a, (~self.rvalue(b)) % 32768)

    # rmem: 15 a b
    #   read memory at address <b> and write it to <a>
    @opcode(code=15)
    def op_rmem(self, a, b):
        self.set_address(a, self.get_address(self.rvalue(b)))

    # wmem: 16 a b
    #   write the value from <b> into memory at address <a>
    @opcode(code=16)
    def op_wmem(self, a, b):
        self.set_address(self.rvalue(a), self.rvalue(b))

    # call: 17 a
    #   write the address of the next instruction to the stack and jump to <a>
    @opcode(code=17)
    def op_call(self, a):
        target = self.rvalue(a)
        if target == 6027:
            self.fn_6027()  # Optimized implementation for teleporter
        else:
            self.stack.append(self.pc)
            self.pc = target

    # ret: 18
    #   remove the top element from the stack and jump to it; empty stack = halt
    @opcode(code=18)
    def op_ret(self):
        if len(self.stack) == 0:
            self.halted = True
        else:
            self.pc = self.stack.pop()

    # out: 19 a
    #   write the character represented by ascii code <a> to the terminal
    @opcode(code=19)
    def op_write(self, a):
        c = self.rvalue(a)
        if c < 32 and chr(c) not in "\n\r\t":
            print(f"<ascii {c}>", end="")
        else:
            print(chr(c), end="")

    # in: 20 a
    #   read a character from the terminal and write its ascii code to <a>
    @opcode(code=20)
    def op_read(self, a):
        while not self.input_buffer:
            if self.assist:
                print(f"Location: {self.memory[2732]}, "
                      f"Orb: {self.memory[3952]}/{self.memory[3953]}")
            line = input()
            match = re.search('^goto (\\d+)$', line.strip())
            if match:
                self.memory[2732] = int(match.group(1))
            elif line == "save":
                with open("saved-game.json", "w") as fp:
                    data = jsonpickle.encode(self)
                    json.dump(data, fp)
            elif line == "prepare teleporter":
                self.registers[7] = 25734  # Code count with FindR7.ajav
                self.warm_fn_6027_cache()
            elif line == "unprepare teleporter":
                self.registers[7] = 0
                self.warm_fn_6027_cache()
            else:
                self.input_buffer.extend([c for c in line])
                self.input_buffer.extend("\n")

        self.set_address(a, ord(self.input_buffer.pop(0)))

    # noop: 21
    #   no operation
    @opcode(code=21)
    def op_noop(self):
        pass

    # Memoization cache of subroutine at address 6027 which only accesses registers r0 and r1; r7 is read only
    #   (r0, r1, r7) -> (r0, r1)
    fn_6027_cache = {}

    def fn_6027(self):

        # Check cache
        in_registers = (self.registers[0], self.registers[1], self.registers[7])
        out_registers = self.fn_6027_cache.get(in_registers)
        if out_registers:
            self.registers[0] = out_registers[0]
            self.registers[1] = out_registers[1]
            return

        # Reimplement bytecode of function in Python (see FindR7.java for an even faster version in Java)
        if self.registers[0] == 0:
            self.registers[0] = (self.registers[1] + 1) % 32768
        elif self.registers[1] == 0:
            self.registers[0] = self.registers[0] - 1
            self.registers[1] = self.registers[7]
            self.fn_6027()
        else:
            t = self.registers[0]
            self.registers[1] = self.registers[1] - 1
            self.fn_6027()
            self.registers[1] = self.registers[0]
            self.registers[0] = t
            self.registers[0] = self.registers[0] - 1
            self.fn_6027()

        # Cache result
        out_registers = (self.registers[0], self.registers[1])
        self.fn_6027_cache[in_registers] = out_registers

    # The algorithm in fn_6027 is recursive, requiring a very deep stack. Prevent stack overflow by calculating the
    # deeper function results first and writing these into the cache.
    def warm_fn_6027_cache(self):
        shadow_registers = list(self.registers)
        self.fn_6027_cache.clear()
        for r0 in range(0, 5):
            for r1 in range(0, 32768):
                self.registers[0] = r0
                self.registers[1] = r1
                self.fn_6027()
        self.registers = list(shadow_registers)


def load_program(file):
    with open(file, "rb") as in_file:
        data = in_file.read()
        program = [(data[addr] + data[addr + 1] * 256) for addr in range(0, len(data), 2)]
    return program


test_machine = Machine(load_program("challenge.bin"))

# Uncomment to restart from saved game
# with open("saved-game.json", "r") as fp:
#     data = json.load(fp)
#     test_machine = jsonpickle.decode(data)

test_machine.run()
