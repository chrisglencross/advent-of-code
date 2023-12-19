#!/usr/bin/python3
# Advent of code 2023 day 19
# See https://adventofcode.com/2023/day/19
import functools
import operator
import re

with open("input.txt") as f:
    workflow_block, ratings_block = [block.strip() for block in f.read().split("\n\n")]
    workflow_lines = [line.strip() for line in workflow_block.split("\n")]
    ratings_lines = [line.strip() for line in ratings_block.split("\n")]


def parse_workflow_rules(workflow_lines):
    workflow_rules = {}
    for workflow_line in workflow_lines:
        name, rules_str = re.match("^([^{]+)\\{(.*)\\}$", workflow_line).groups()
        rules = []
        for rule_str in rules_str.split(","):
            if ":" not in rule_str:
                rules.append(tuple([rule_str]))
            else:
                condition, destination = rule_str.split(":")
                for c in "<>":
                    if c in condition:
                        rating, value_str = condition.split(c)
                        rules.append((c, rating, int(value_str), destination))
        workflow_rules[name] = rules
    return workflow_rules


def build_workflow_tree(workflow_rules, name, step_no):
    if name == "A" or name == "R":
        return name
    workflow = workflow_rules[name]
    step = workflow[step_no]
    if len(step) == 1:
        destination = step[0]
        return build_workflow_tree(workflow_rules, destination, 0)
    condition, rating, value, destination = step
    return (condition, rating, value,
            build_workflow_tree(workflow_rules, destination, 0),
            build_workflow_tree(workflow_rules, name, step_no + 1))


workflows = parse_workflow_rules(workflow_lines)
workflow_tree = build_workflow_tree(workflows, "in", 0)


# Part 1
def parse_ratings(ratings_lines):
    items = []
    for ratings_line in ratings_lines:
        x, m, a, s = [int(v) for v in re.match("^\\{x=(.*),m=(.*),a=(.*),s=(.*)\\}$", ratings_line).groups()]
        items.append({"x": x, "m": m, "a": a, "s": s})
    return items


def is_acceptable(node, item):
    if node == "A":
        return True
    if node == "R":
        return False
    condition, rating, value, true_node, false_node = node
    rating_value = item[rating]
    condition_matches = (condition == "<" and rating_value < value) or (condition == ">" and rating_value > value)
    return is_acceptable(true_node if condition_matches else false_node, item)


items = parse_ratings(ratings_lines)
print(sum((sum(item.values())) for item in items if is_acceptable(workflow_tree, item)))


# Part 2
def split_space(space, condition, rating, value):
    lo, hi = space[rating]
    if not lo <= value <= hi:
        empty_space = {rating: (0, -1) for rating in "xmas"}
        return empty_space, space
    match_space = dict(space)
    mismatch_space = dict(space)
    if condition == "<":
        match_space[rating] = (lo, min(value-1, hi))
        mismatch_space[rating] = (max(lo, value), hi)
    if condition == ">":
        match_space[rating] = (max(lo, value+1), hi)
        mismatch_space[rating] = (lo, min(hi, value))
    return match_space, mismatch_space


def get_acceptable_ranges(node, space):
    if node == "A":
        return [space]
    if node == "R":
        return []
    condition, rating, value, true_node, false_node = node
    true_space, false_space = split_space(space, condition, rating, value)
    return get_acceptable_ranges(true_node, true_space) + get_acceptable_ranges(false_node, false_space)


def space_size(space):
    return functools.reduce(operator.mul, ((hi-lo+1) for lo, hi in space.values()))


initial_space = {rating: (1, 4000) for rating in "xmas"}
print(sum(space_size(space) for space in get_acceptable_ranges(workflow_tree, initial_space)))
