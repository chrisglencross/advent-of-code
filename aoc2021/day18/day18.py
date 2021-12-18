# Advent of code 2021 day 18
# See https://adventofcode.com/2021/day/18
from __future__ import annotations

import functools
import itertools
from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Optional


@dataclass
class Node(ABC):
    parent: Optional["PairNode"] = None

    def depth(self):
        if self.parent is None:
            return 0
        else:
            return 1 + self.parent.depth()

    def find_explode_candidate(self) -> Optional[PairNode]:
        return None

    @abstractmethod
    def find_split_candidate(self) -> Optional[IntNode]:
        pass

    @abstractmethod
    def magnitude(self):
        pass


@dataclass
class IntNode(Node):
    value: int = None

    def find_number(self, left, prune) -> Optional[IntNode]:
        return self

    def magnitude(self) -> int:
        return self.value

    def find_split_candidate(self) -> Optional[IntNode]:
        return self if self.value > 9 else None

    def split(self):
        left = IntNode(value=self.value // 2)
        right = IntNode(value=self.value - left.value)
        self.parent.replace_child(self, pair(left, right))

    def __str__(self):
        return str(self.value)


@dataclass
class PairNode(Node):
    left: Node = None
    right: Node = None

    def find_number(self, search_left, origin_node) -> Optional[IntNode]:
        """Searches for the closest IntNode to the syntactic left or right of a neighbouring origin node."""
        recurse_to = []
        if search_left and self.left is not origin_node:
            if self.right is not origin_node:
                recurse_to.append(self.right)
            recurse_to.append(self.left)
        if not search_left and self.right is not origin_node:
            if self.left is not origin_node:
                recurse_to.append(self.left)
            recurse_to.append(self.right)
        if self.parent is not None and self.parent is not origin_node:
            recurse_to.append(self.parent)

        return next((number
                     for number in (node.find_number(search_left, self) for node in recurse_to)
                     if number is not None), None)

    def find_explode_candidate(self) -> Optional[PairNode]:
        if isinstance(self.left, IntNode) and isinstance(self.right, IntNode) and self.depth() >= 4:
            return self
        else:
            return self.left.find_explode_candidate() or self.right.find_explode_candidate()

    def explode(self):
        left = self.parent.find_number(True, self)
        right = self.parent.find_number(False, self)
        if left:
            left.value += self.left.value
        if right:
            right.value += self.right.value
        self.parent.replace_child(self, IntNode(value=0))

    def find_split_candidate(self) -> Optional[IntNode]:
        return self.left.find_split_candidate() or self.right.find_split_candidate()

    def replace_child(self, old_child, new_child):
        new_child.parent = self
        if old_child == self.left:
            self.left = new_child
        elif old_child == self.right:
            self.right = new_child

    def magnitude(self) -> int:
        return self.left.magnitude() * 3 + self.right.magnitude() * 2

    def __str__(self):
        return f"[{self.left}, {self.right}]"


def pair(left, right) -> PairNode:
    parent = PairNode(left=left, right=right)
    left.parent = parent
    right.parent = parent
    return parent


def parse_node(chars: list) -> Node:
    c = chars.pop(0)
    if c == '[':
        left = parse_node(chars)
        chars.pop(0)  # ,
        right = parse_node(chars)
        chars.pop(0)  # ]
        return pair(left, right)
    else:
        return IntNode(value=int(c))


def explode(node: PairNode) -> bool:
    explode_node = node.find_explode_candidate()
    if explode_node:
        explode_node.explode()
    return bool(explode_node)


def split(node: Node) -> bool:
    split_node = node.find_split_candidate()
    if split_node:
        split_node.split()
    return bool(split_node)


def add(left: Node, right: Node) -> PairNode:
    value = pair(left, right)
    while explode(value) or split(value):
        pass
    return value


with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

# Part 1
print(functools.reduce(add, [parse_node(list(line)) for line in lines]).magnitude())

# Part 2
print(max(add(parse_node(list(p[0])), parse_node(list(p[1]))).magnitude() for p in itertools.permutations(lines, 2)))
