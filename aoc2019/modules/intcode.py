import inspect
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Set

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
    size: int
    fn: Callable[..., OpResult]
    params: List[str]


def opcode(code):
    def register(func):
        params = list(inspect.signature(func).parameters)
        OP_CODES[code] = OpCode(func.__name__.replace("op_", ""), code, len(params), func, params)
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
        print("Program is blocked waiting for input")
        return OpResult(jump=program.pc)
    value = program.input.pop(0)
    return OpResult(update={target_addr: value})


@opcode(code=4)
def op_output(program, a1):
    return OpResult(output=a1)


@opcode(code=5)
def op_jump_if_true(program, a1, target):
    if a1 != 0:
        return OpResult(jump=target)
    else:
        return OpResult()


@opcode(code=6)
def op_jump_if_false(program, a1, target):
    if a1 == 0:
        return OpResult(jump=target)
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

    # Identify addresses which are code and addresses which are data
    # The intersection is self-modifying code
    # Used for annotating the disassembly
    code_addr: Set[int] = field(default_factory=set)
    read_data_addr: Set[int] = field(default_factory=set)
    write_data_addr: Set[int] = field(default_factory=set)
    jump_targets: Set[int] = field(default_factory=set)
    relative_base_addr: Set[int] = field(default_factory=set)


    def snapshot(self):
        return Program(memory=dict(self.memory), pc=self.pc)

    def is_terminated(self):
        return self.terminated

    def is_blocked(self):
        return self.memory_get(self.pc) == 3 and len(self.input) == 0

    def next_output(self):
        while not self.output and not self.is_terminated() and not self.is_blocked():
            self.tick()
        if self.output:
            return self.output.pop()
        else:
            return None

    def run(self, limit=None):
        count = 0
        while not self.is_terminated():
            if limit is not None and count >= limit:
                break
            self.tick()
            count = count + 1
        return self.output

    def memory_get(self, address, code=False, data=False):
        if code:
            self.code_addr.add(address)
        if data:
            self.read_data_addr.add(address)
        return self.memory.get(address, 0)

    def tick(self):

        if self.terminated:
            print("WARNING: already terminated")
            return False

        self.tick_count = self.tick_count + 1

        is_self_modifying_code = self.pc in self.write_data_addr

        # Decode opcode and argument modes
        opcode = self.memory_get(self.pc, code=True)
        arg_modes = [(opcode // 100) % 10, (opcode // 1000) % 10, (opcode // 10000) % 10]
        opcode = opcode % 100

        # Find the operation implementation
        op = OP_CODES.get(opcode, None)
        if op is None:
            raise Exception(f"Unsupported opcode {opcode}")
        op_size = op.size
        params = op.params

        # Prepare the args for the operation, including addressing mode
        # If the parameter name contains "addr" it is never treated as immediate value
        args = []
        for addr in range(self.pc + 1, self.pc + op_size):
            args.append(self.memory_get(addr, code=True))
            is_self_modifying_code = is_self_modifying_code or self.pc in self.write_data_addr
        op_args = []
        debug_args = []
        for i in range(len(args)):
            param_name = params[i + 1]
            if arg_modes[i] == 0 and "addr" not in param_name:
                # Position mode
                op_args.append(self.memory_get(args[i]))
                debug_args.append(f"{param_name}=@{args[i]:04}={op_args[i]}")
            elif arg_modes[i] == 2:
                # Relative mode
                if "addr" in param_name:
                    # For address parameters, provide the relative address
                    op_args.append(args[i] + self.relative_base)
                    debug_args.append(f"{param_name}=({self.relative_base:04}+{args[i]})")
                else:
                    # For other parameters dereference the relative address
                    op_args.append(self.memory_get(args[i] + self.relative_base))
                    debug_args.append(f"{param_name}=@({self.relative_base:04}+{args[i]})={op_args[i]}")
            else:
                # Immediate mode
                op_args.append(args[i])
                if "target" in param_name:
                    debug_args.append(f"{param_name}={args[i]:04}")
                else:
                    debug_args.append(f"{param_name}={args[i]}")

        if self.debug:
            comments = []
            if is_self_modifying_code:
                comments.append("DATA")
            if self.pc in self.jump_targets:
                comments.append("JUMP TARGET")
            if comments:
                comment_str = f"\t# {', '.join(comments)}"
            else:
                comment_str = ""
            print(f"T+{self.tick_count:04} @{self.pc:04} {op.name}({', '.join(debug_args)}){comment_str}")

        # Call the operation
        result = op.fn(self, *op_args)

        # Apply updates
        for addr, value in result.update.items():
            if self.debug:
                print(f"\t\t\t\t=> set @{addr}={value}")
            self.memory[addr] = value
            self.write_data_addr.add(addr)

        # Write output
        if result.output is not None:
            if self.debug:
                print(f"\t\t\t\t=> output {result.output}")
            self.output.append(result.output)

        # Update program counter
        if result.jump is not None:
            if self.debug:
                print(f"\t\t\t\t=> jump @{result.jump:04}")
            self.pc = result.jump
            self.jump_targets.add(result.jump)
        else:
            self.pc = self.pc + op_size

        if result.relative_base is not None:
            if self.debug:
                print(f"\t\t\t\t=> set relative_base={result.relative_base}")
            self.relative_base = result.relative_base
            self.relative_base_addr.add(result.relative_base)

        if result.terminated:
            if self.debug:
                print(f"\t\t\t\t=> set terminated={result.terminated}")
            self.terminated = True

        return not self.terminated

    def print_disassembly(self):
        max_address = max(self.memory.keys())
        addr = 0
        while addr <= max_address:

            is_self_modifying_code = addr in self.write_data_addr

            # Decode opcode and argument modes
            opcode = self.memory_get(addr)
            arg_modes = [(opcode // 100) % 10, (opcode // 1000) % 10, (opcode // 10000) % 10]
            opcode = opcode % 100

            # Find the operation implementation
            op = OP_CODES.get(opcode, None)

            # Debug as data if not understood, or tracing history shows this has been used as data and never executed
            if op is None or (addr not in self.code_addr and
                              (addr in self.read_data_addr or addr in self.write_data_addr)):
                is_relative_base = addr in self.relative_base_addr
                comment_str = ""
                if is_relative_base:
                    comment_str = "\t# RELATIVE BASE"
                print(f"@{addr:04}\t{opcode}{comment_str}")
                addr = addr + 1
            else:
                op_size = op.size
                params = op.params

                # Prepare the args for the operation, including addressing mode
                # If the parameter name contains "addr" it is never treated as immediate value
                args = []
                for param_addr in range(addr + 1, addr + op_size):
                    is_self_modifying_code = is_self_modifying_code or param_addr in self.write_data_addr
                    args.append(self.memory_get(param_addr))
                debug_args = []
                for i, arg in enumerate(args):
                    param_name = params[i + 1]
                    if arg_modes[i] == 0 and "addr" not in param_name:
                        # Position mode
                        debug_args.append(f"{param_name}=@{arg:04}")
                    elif arg_modes[i] == 2:
                        # Relative mode
                        if "addr" in param_name:
                            # For address parameters, provide the relative address
                            debug_args.append(f"{param_name}=(relative_base+{arg})")
                        else:
                            # For other parameters dereference the relative address
                            debug_args.append(f"{param_name}=@(relative_base+{arg})")
                    else:
                        # Immediate mode
                        if "target" in param_name:
                            debug_args.append(f"{param_name}={arg:04}")
                        else:
                            debug_args.append(f"{param_name}={arg}")

                comments = []
                if is_self_modifying_code:
                    comments.append("DATA")
                if addr in self.jump_targets:
                    comments.append("JUMP TARGET")
                if comments:
                    comment_str = f"\t# {', '.join(comments)}"
                else:
                    comment_str = ""

                print(f"@{addr:04}\t{op.name}({', '.join(debug_args)}){comment_str}")
                addr = addr + op_size


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
