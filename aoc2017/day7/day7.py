import re
from dataclasses import dataclass

with open("input") as f:
    lines = f.readlines()


@dataclass
class Program:
    name: str
    weight: int
    programs: tuple
    tower_weight: int = None

    def get_tower_weight(self):
        if self.tower_weight is None:
            self.tower_weight = self.weight + sum([programs[program].get_tower_weight() for program in self.programs])
        return self.tower_weight

    def is_inbalanced(self):
        return len(set([programs[program].get_tower_weight() for program in self.programs])) > 1


programs = dict()
all_children = []
for line in lines:
    match = re.search("^([a-z]+) \\(([0-9]+)\\)(.*)$", line.strip())
    children = tuple()
    if match.group(3):
        suffix = match.group(3).replace(" ", "").replace("->", "")
        if suffix:
            children = tuple(suffix.replace(" ", "").split(","))
    all_children.extend(children)
    program = Program(name=match.group(1), weight=int(match.group(2)), programs=children)
    programs[program.name] = program

print(set(programs.keys()) - set(all_children))

for program in programs.values():
    if program.is_inbalanced():
        children_unbalanced = False
        for child in program.programs:
            child = programs[child]
            if child.is_inbalanced():
                children_unbalanced = True
        if not children_unbalanced:
            print("One of these children is not like the others... adjust its weight to make the tower_weight the same")
            for child in program.programs:
                child = programs[child]
                print(child)
