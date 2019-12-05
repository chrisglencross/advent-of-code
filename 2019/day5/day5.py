#!/usr/bin/python3
# Advent of code 2019 day 5
import inspect
from dataclasses import dataclass, field
from typing import List, Dict, Callable

OP_CODES = list()


@dataclass
class OpResult:
    update: Dict[int, int] = field(default_factory=dict)
    output: int = None
    jump: int = None


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
def op_less_than(program, a1, a2, target_addr):
    if a1 == a2:
        return OpResult(update={target_addr: 1})
    else:
        return OpResult(update={target_addr: 0})


@opcode(code=99, size=1)
def op_exit(program):
    return OpResult()


@dataclass
class Program:
    memory: List[int] = field(default_factory=list)
    input: List[int] = field(default_factory=list)
    output: List[int] = field(default_factory=list)
    pc: int = 0
    debug: bool = True

    def snapshot(self):
        return Program(memory=self.memory[:], pc=self.pc)

    def is_terminated(self):
        return self.memory[self.pc] == 99

    def tick(self):

        # Decode opcode and argument modes
        opcode = self.memory[self.pc]
        mode1 = (opcode // 100) % 10
        mode2 = (opcode // 1000) % 10
        mode3 = (opcode // 10000) % 10
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
        args = self.memory[self.pc + 1:self.pc + op.size]
        op_args = args[:]
        debug_args = [str(arg) for arg in args]
        params = list(inspect.signature(op.fn).parameters)
        if len(args) >= 1 and mode1 == 0 and "addr" not in params[1]:
            op_args[0] = self.memory[args[0]]
            debug_args[0] = f"@{args[0]}={op_args[0]}"
        if len(args) >= 2 and mode2 == 0 and "addr" not in params[2]:
            op_args[1] = self.memory[args[1]]
            debug_args[1] = f"@{args[1]}={op_args[1]}"
        if len(args) >= 3 and mode3 == 0 and "addr" not in params[3]:
            op_args[2] = self.memory[args[2]]
            debug_args[1] = f"@{args[2]}={op_args[2]}"

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
        if result.output:
            if self.debug:
                print(f"\toutput {result.output}")
            self.output.append(result.output)

        # Update program counter
        if result.jump:
            if self.debug:
                print(f"\tjump @{result.jump}")
            self.pc = result.jump
        else:
            self.pc = self.pc + op.size

        return True


def run_program(memory, input_value):
    p = Program(memory=memory, pc=0, input=[input_value])
    while not p.is_terminated():
        p.tick()
    return p.output


with open("input.txt") as f:
    lines = f.readlines()
memory = [int(value) for value in lines[0].split(",")]

# Part 1
print(run_program(memory[:], input_value=1))

# Part 2
print(run_program(memory[:], input_value=5))
