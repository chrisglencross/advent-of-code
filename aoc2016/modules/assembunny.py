from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Callable


@dataclass
class Program:
    instructions: List[Tuple]
    registers: Dict[str, int] = field(default_factory=dict)
    optimizations: Dict[int, Callable[["Program"], None]] = field(default_factory=dict)
    pc: int = 0
    outputs: List = field(default_factory=list)
    debug: bool = False

    def is_terminated(self):
        return self.pc < 0 or self.pc >= len(self.instructions)

    def run(self):
        while not self.is_terminated():
            self.tick()

    def next_output(self):
        while not self.is_terminated() and not self.outputs:
            self.tick()
        return self.outputs.pop(0)

    def tick(self):
        if self.debug:
            print(f"{self.pc}: {self.instructions[self.pc]}")

        op, *args = self.instructions[self.pc]

        optimization_fn = self.optimizations.get(self.pc)
        if optimization_fn:
            if self.debug:
                print(f"  => INVOKING OPTIMIZED IMPLEMENTATION")
            optimization_fn(self)
            return

        if op == "cpy":
            if type(args[1]) != int:
                self.registers[args[1]] = self.get_value(args[0])
            self.pc += 1
        elif op == "inc":
            self.registers[args[0]] += 1
            self.pc += 1
        elif op == "dec":
            self.registers[args[0]] -= 1
            self.pc += 1
        elif op == "jnz":
            if self.get_value(args[0]) != 0:
                self.pc += self.get_value(args[1])
            else:
                self.pc += 1
        elif op == "tgl":
            addr = self.pc + self.get_value(args[0])
            if 0 <= addr < len(self.instructions):
                other_op, *other_args = self.instructions[addr]
                if other_op == "inc":
                    replace_op = "dec"
                elif len(other_args) == 1:
                    replace_op = "inc"
                elif other_op == "jnz":
                    replace_op = "cpy"
                elif len(other_args) == 2:
                    replace_op = "jnz"
                if self.debug:
                    print(f"  => TOGGLING {addr}: op={other_op} {other_args} with {replace_op}")
                self.instructions[addr] = tuple([replace_op, *other_args])
            self.pc += 1
        elif op == "out":
            value = self.get_value(args[0])
            if self.debug:
                print(f"  => OUTPUT {value}")
            self.outputs.append(value)
            self.pc += 1
        else:
            raise Exception(f"Unknown op {op}")

    def get_value(self, value):
        if type(value) is int:
            return value
        else:
            return self.registers.get(value, 0)


def load_program(file, **kwargs) -> Program:
    def register_or_int(value):
        if value in "abcd":
            return value
        return int(value)

    with open(file) as f:
        lines = [line.strip() for line in f.readlines()]

    instructions = []
    for line in lines:
        op, *args = line.split(" ")
        args = [register_or_int(arg) for arg in args]
        instructions.append((op, *args))

    return Program(instructions=instructions, **kwargs)
