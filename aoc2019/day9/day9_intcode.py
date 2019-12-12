from aoc2019.modules import intcode

program = intcode.load_file("input.txt", input=[2])
print(program.run())
