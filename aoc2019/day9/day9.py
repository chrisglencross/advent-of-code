#!/usr/bin/python3
# Advent of code 2019 day 9
import inspect
from dataclasses import dataclass, field
from typing import List, Dict, Callable

OP_CODES = list()


@dataclass
class OpResult:
    update: Dict[int, int] = field(default_factory=dict)
    output: int = None
    jump: int = None
    relative_base: int = None


@dataclass()
class OpCode:
    name: str
    code: int
    size: int
    fn: Callable[..., OpResult]


def opcode(code, size):
    def register(func):
        OP_CODES.append(OpCode(func.__name__, code, size, func))
        return func

    return register


@opcode(code=1, size=4)
def op_add(program, a1, a2, target_addr):
    return OpResult(update={target_addr: a1 + a2})


@opcode(code=2, size=4)
def op_mul(program, a1, a2, target_addr):
    return OpResult(update={target_addr: a1 * a2})


@opcode(code=3, size=2)
def op_input(program, target_addr):
    if not program.input:
        print("Blocking because no input")
        return OpResult(jump=program.pc)
    value = program.input.pop(0)
    return OpResult(update={target_addr: value})


@opcode(code=4, size=2)
def op_output(program, a1):
    return OpResult(output=a1)


@opcode(code=5, size=3)
def op_jump_if_true(program, a1, a2):
    if a1 != 0:
        return OpResult(jump=a2)
    else:
        return OpResult()


@opcode(code=6, size=3)
def op_jump_if_false(program, a1, a2):
    if a1 == 0:
        return OpResult(jump=a2)
    else:
        return OpResult()


@opcode(code=7, size=4)
def op_less_than(program, a1, a2, target_addr):
    if a1 < a2:
        return OpResult(update={target_addr: 1})
    else:
        return OpResult(update={target_addr: 0})


@opcode(code=8, size=4)
def op_eq(program, a1, a2, target_addr):
    if a1 == a2:
        return OpResult(update={target_addr: 1})
    else:
        return OpResult(update={target_addr: 0})


@opcode(code=9, size=2)
def op_adjust_relative_base(program, a):
    return OpResult(relative_base=program.relative_base + a)


@opcode(code=99, size=1)
def op_exit(program):
    return OpResult()


@dataclass
class Program:
    name: str = "Program"
    memory: Dict[int, int] = field(default_factory=dict)
    input: List[int] = field(default_factory=list)
    output: List[int] = field(default_factory=list)
    pc: int = 0
    relative_base: int = 0
    debug: bool = False

    def snapshot(self):
        return Program(memory=dict(self.memory), pc=self.pc)

    def is_terminated(self):
        return self.memory[self.pc] == 99

    def tick(self):

        # Decode opcode and argument modes
        opcode = self.memory[self.pc]
        arg_modes = [(opcode // 100) % 10, (opcode // 1000) % 10, (opcode // 10000) % 10]
        opcode = opcode % 10

        # Terminate
        if opcode == 99:
            return False

        # Find the operation implementation
        op = [op_code for op_code in OP_CODES if op_code.code == opcode]
        if not op:
            raise Exception(f"Unsupported opcode {opcode}")
        op = op[0]

        # Prepare the args for the operation, including addressing mode
        # If the parameter name contains "addr" it is never treated as immediate value
        args = []
        for addr in range(self.pc + 1, self.pc + op.size):
            args.append(self.memory[addr])
        params = list(inspect.signature(op.fn).parameters)
        op_args = []
        debug_args = []
        for i in range(len(args)):
            if arg_modes[i] == 0 and "addr" not in params[i + 1]:
                # Position mode
                op_args.append(self.memory.get(args[i], 0))
                debug_args.append(f"@{args[i]}={op_args[i]}")
            elif arg_modes[i] == 2:
                # Relative mode
                if "addr" in params[i + 1]:
                    # For address parameters, provide the relative address
                    op_args.append(args[i] + self.relative_base)
                    debug_args.append(f"@[{self.relative_base}+{args[i]}]")
                else:
                    # For other parameters dereference the relative address
                    op_args.append(self.memory.get(args[i] + self.relative_base, 0))
                    debug_args.append(f"@[{self.relative_base}+{args[i]}]={op_args[i]}")
            else:
                # Immediate mode
                op_args.append(args[i])
                debug_args.append(f"@{args[i]}")

        # Call the operation
        result = op.fn(self, *op_args)
        if self.debug:
            print(f"@{self.pc} {op.name} {' '.join(debug_args)}")

        # Apply updates
        for addr, value in result.update.items():
            if self.debug:
                print(f"\tset @{addr}={value}")
            self.memory[addr] = value

        # Write output
        if result.output is not None:
            if self.debug:
                print(f"\toutput {result.output}")
            self.output.append(result.output)

        # Update program counter
        if result.jump is not None:
            if self.debug:
                print(f"\tjump @{result.jump}")
            self.pc = result.jump
        else:
            self.pc = self.pc + op.size

        if result.relative_base is not None:
            if self.debug:
                print(f"\tset relative_base={result.relative_base}")
            self.relative_base = result.relative_base

        return True


def run_program(memory, input_values):
    dict_memory = {}
    for i, b in enumerate(memory):
        dict_memory[i] = b
    p = Program(memory=dict_memory, pc=0, input=input_values)
    while not p.is_terminated():
        p.tick()
    return p.output


with open("input.txt") as f:
    lines = f.readlines()
memory = [int(value) for value in lines[0].split(",")]
output = run_program(memory, [2])
print(output)
