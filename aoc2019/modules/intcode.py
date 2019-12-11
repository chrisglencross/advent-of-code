import inspect
from dataclasses import dataclass, field
from typing import List, Dict, Callable

OP_CODES = {}

@dataclass
class OpResult:
    update: Dict[int, int] = field(default_factory=dict)
    output: int = None
    jump: int = None
    relative_base: int = None
    terminated: bool = False


@dataclass
class OpCode:
    name: str
    code: int
    fn: Callable[..., OpResult]


def opcode(code):
    def register(func):
        OP_CODES[code] = OpCode(func.__name__, code, func)
        return func

    return register


@opcode(code=1)
def op_add(program, a1, a2, target_addr):
    return OpResult(update={target_addr: a1 + a2})


@opcode(code=2)
def op_mul(program, a1, a2, target_addr):
    return OpResult(update={target_addr: a1 * a2})


@opcode(code=3)
def op_input(program, target_addr):
    if not program.input:
        print("Blocking because no input")
        return OpResult(jump=program.pc)
    value = program.input.pop(0)
    return OpResult(update={target_addr: value})


@opcode(code=4)
def op_output(program, a1):
    return OpResult(output=a1)


@opcode(code=5)
def op_jump_if_true(program, a1, a2):
    if a1 != 0:
        return OpResult(jump=a2)
    else:
        return OpResult()


@opcode(code=6)
def op_jump_if_false(program, a1, a2):
    if a1 == 0:
        return OpResult(jump=a2)
    else:
        return OpResult()


@opcode(code=7)
def op_less_than(program, a1, a2, target_addr):
    if a1 < a2:
        return OpResult(update={target_addr: 1})
    else:
        return OpResult(update={target_addr: 0})


@opcode(code=8)
def op_eq(program, a1, a2, target_addr):
    if a1 == a2:
        return OpResult(update={target_addr: 1})
    else:
        return OpResult(update={target_addr: 0})


@opcode(code=9)
def op_adjust_relative_base(program, a):
    return OpResult(relative_base=program.relative_base + a)


@opcode(code=99)
def op_exit(program):
    return OpResult(terminated=True)


@dataclass
class Program:
    name: str = "Program"
    memory: Dict[int, int] = field(default_factory=dict)
    input: List[int] = field(default_factory=list)
    output: List[int] = field(default_factory=list)
    pc: int = 0
    relative_base: int = 0
    debug: bool = False
    tick_count: int = 0
    terminated: bool = False

    def snapshot(self):
        return Program(memory=dict(self.memory), pc=self.pc)

    def is_terminated(self):
        return self.terminated

    def next_output(self):
        while not self.output and not self.is_terminated():
            self.tick()
        if self.output:
            return self.output.pop()
        else:
            return None

    def tick(self):

        if self.terminated:
            print("WARNING: already terminated")
            return False

        self.tick_count = self.tick_count + 1

        # Decode opcode and argument modes
        opcode = self.memory[self.pc]
        arg_modes = [(opcode // 100) % 10, (opcode // 1000) % 10, (opcode // 10000) % 10]
        opcode = opcode % 100

        # Find the operation implementation
        op = OP_CODES.get(opcode, None)
        if op is None:
            raise Exception(f"Unsupported opcode {opcode}")
        params = list(inspect.signature(op.fn).parameters)
        op_size = len(params)

        # Prepare the args for the operation, including addressing mode
        # If the parameter name contains "addr" it is never treated as immediate value
        args = []
        for addr in range(self.pc + 1, self.pc + op_size):
            args.append(self.memory[addr])
        op_args = []
        debug_args = []
        for i in range(len(args)):
            param_name = params[i + 1]
            if arg_modes[i] == 0 and "addr" not in param_name:
                # Position mode
                op_args.append(self.memory.get(args[i], 0))
                debug_args.append(f"{param_name}=*{args[i]}={op_args[i]}")
            elif arg_modes[i] == 2:
                # Relative mode
                if "addr" in param_name:
                    # For address parameters, provide the relative address
                    op_args.append(args[i] + self.relative_base)
                    debug_args.append(f"{param_name}=({self.relative_base}+{args[i]})")
                else:
                    # For other parameters dereference the relative address
                    op_args.append(self.memory.get(args[i] + self.relative_base, 0))
                    debug_args.append(f"{param_name}=*({self.relative_base}+{args[i]})={op_args[i]}")
            else:
                # Immediate mode
                op_args.append(args[i])
                debug_args.append(f"{param_name}={args[i]}")

        if self.debug:
            print(f"T+{self.tick_count}\t@{self.pc} {op.name}({', '.join(debug_args)})")

        # Call the operation
        result = op.fn(self, *op_args)

        # Apply updates
        for addr, value in result.update.items():
            if self.debug:
                print(f"\t\t=> set *{addr}={value}")
            self.memory[addr] = value

        # Write output
        if result.output is not None:
            if self.debug:
                print(f"\t\t=> output {result.output}")
            self.output.append(result.output)

        # Update program counter
        if result.jump is not None:
            if self.debug:
                print(f"\t\t=> jump @{result.jump}")
            self.pc = result.jump
        else:
            self.pc = self.pc + op_size

        if result.relative_base is not None:
            if self.debug:
                print(f"\t\t=> set relative_base={result.relative_base}")
            self.relative_base = result.relative_base

        if result.terminated:
            if self.debug:
                print(f"\t\t=> set terminated={result.terminated}")
            self.terminated = True

        return not self.terminated


# Memory is represented as an addr->value dictionary to give a sparse resizable address space.
def format_memory(program):
    memory = {}
    for addr, value in enumerate(program):
        memory[addr] = value
    return memory


def new_program(memory, **kwargs):
    return Program(memory=format_memory(memory), **kwargs)


def load_program(program_data, **kwargs):
    memory = [int(value) for value in program_data.split(",")]
    return new_program(memory, **kwargs)


def load_file(file, **kwargs):
    with open(file) as f:
        program_data = f.readline()
        return load_program(program_data, **kwargs)
