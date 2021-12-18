# Advent of code 2021 day 18
# See https://adventofcode.com/2021/day/18
from __future__ import annotations

import functools
import itertools
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


@dataclass
class IntNode(Node):
    value: int = None

    def find_number(self, left, prune) -> Optional[IntNode]:
        return self

    def __str__(self):
        return str(self.value)


@dataclass
class PairNode(Node):
    left: Node = None
    right: Node = None

    def find_number(self, search_left, prune) -> Optional[IntNode]:
        recurse_to = []
        if search_left and self is not prune and self.left is not prune:
            if self.right is not prune:
                recurse_to.append(self.right)
            recurse_to.append(self.left)
        if not search_left and self is not prune and self.right is not prune:
            if self.left is not prune:
                recurse_to.append(self.left)
            recurse_to.append(self.right)
        if self.parent is not None and self.parent is not prune:
            recurse_to.append(self.parent)

        for node in recurse_to:
            found = node.find_number(search_left, self)
            if found:
                return found
        return None

    def replace_child(self, child, new_child):
        new_child.parent = self
        if child == self.left:
            self.left = new_child
        elif child == self.right:
            self.right = new_child

    def __str__(self):
        return f"[{self.left}, {self.right}]"


def pair(left, right):
    if not left:
        return right
    parent = PairNode(left=left, right=right, parent=None)
    left.parent = parent
    right.parent = parent
    return parent


def parse_node(chars : list):
    c = chars.pop(0)
    if c == '[':
        left = parse_node(chars)
        chars.pop(0)  # ,
        right = parse_node(chars)
        chars.pop(0)  # ]
        return pair(left, right)
    else:
        return IntNode(value=int(c), parent=None)


def find_explosion_candidate(node: PairNode) -> Optional[PairNode]:
    if isinstance(node.left, IntNode) and isinstance(node.right, IntNode):
        depth = node.depth()
        if depth >= 4:
            return node
    if isinstance(node.left, PairNode):
        left = find_explosion_candidate(node.left)
        if left:
            return left
    if isinstance(node.right, PairNode):
        right = find_explosion_candidate(node.right)
        if right:
            return right
    return None


def explode(node: PairNode) -> bool:
    to_explode = find_explosion_candidate(node)
    if to_explode:
        to_left = to_explode.find_number(True, to_explode)
        to_right = to_explode.find_number(False, to_explode)
        if to_left:
            to_left.value += to_explode.left.value
        if to_right:
            to_right.value += to_explode.right.value
        to_explode.parent.replace_child(to_explode, IntNode(value=0, parent=None))
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
    to_split = find_split_candidate(node)
    if to_split:
        left = IntNode(value=to_split.value // 2, parent=None)
        right = IntNode(value=to_split.value - left.value, parent=None)
        to_split.parent.replace_child(to_split, pair(left, right))
        return True
    else:
        return False


def add(left, right):
    total = pair(left, right)
    while True:
        while explode(total):
            pass
        if not split(total):
            break
    return total


def magnitude(node: Node):
    if isinstance(node, IntNode):
        return node.value
    elif isinstance(node, PairNode):
        return 3*magnitude(node.left) + 2*magnitude(node.right)


with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

# Part 1
print(magnitude(functools.reduce(add, [parse_node(list(line)) for line in lines])))

# Part 2
print(max(magnitude(add(parse_node(list(p[0])), parse_node(list(p[1])))) for p in itertools.permutations(lines, 2)))
