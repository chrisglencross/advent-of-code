# Advent of code 2021 day 18
# See https://adventofcode.com/2021/day/18
from __future__ import annotations

import functools
import itertools
from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    parent: Optional["PairNode"] = None

    def depth(self):
        if self.parent is None:
            return 0
        else:
            return 1 + self.parent.depth()

    @abstractmethod
    def magnitude(self):
        pass

@dataclass
class IntNode(Node):
    value: int = None

    def find_number(self, left, prune) -> Optional[IntNode]:
        return self

    def magnitude(self):
        return self.value

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

    def replace_child(self, old_child, new_child):
        new_child.parent = self
        if old_child == self.left:
            self.left = new_child
        elif old_child == self.right:
            self.right = new_child

    def magnitude(self):
        return self.left.magnitude() * 3 + self.right.magnitude() * 2

    def __str__(self):
        return f"[{self.left}, {self.right}]"


def pair(left, right):
    if not left:
        return right
    parent = PairNode(left=left, right=right, parent=None)
    left.parent = parent
    right.parent = parent
    return parent


def parse_node(chars: list):
    c = chars.pop(0)
    if c == '[':
        left = parse_node(chars)
        chars.pop(0)  # ,
        right = parse_node(chars)
        chars.pop(0)  # ]
        return pair(left, right)
    else:
        return IntNode(value=int(c), parent=None)


def find_explode_candidate(node: PairNode) -> Optional[PairNode]:
    if isinstance(node.left, IntNode) and isinstance(node.right, IntNode):
        depth = node.depth()
        if depth >= 4:
            return node
    if isinstance(node.left, PairNode):
        left = find_explode_candidate(node.left)
        if left:
            return left
    if isinstance(node.right, PairNode):
        right = find_explode_candidate(node.right)
        if right:
            return right
    return None


def explode(node: PairNode) -> bool:
    explode_node = find_explode_candidate(node)
    if explode_node:
        parent = explode_node.parent
        left = parent.find_number(True, explode_node)
        right = parent.find_number(False, explode_node)
        if left:
            left.value += explode_node.left.value
        if right:
            right.value += explode_node.right.value
        parent.replace_child(explode_node, IntNode(value=0, parent=None))
        return True
    return False


def find_split_candidate(node: Node) -> IntNode:
    if isinstance(node, IntNode):
        return node if node.value > 9 else None
    if isinstance(node, PairNode):
        result = find_split_candidate(node.left)
        if result is None:
            result = find_split_candidate(node.right)
        return result


def split(node: Node) -> bool:
    split_node = find_split_candidate(node)
    if split_node:
        left = IntNode(value=split_node.value // 2, parent=None)
        right = IntNode(value=split_node.value - left.value, parent=None)
        split_node.parent.replace_child(split_node, pair(left, right))
        return True
    else:
        return False


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
