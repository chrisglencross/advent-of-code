#!/usr/bin/python3
# Advent of code 2020 day 19
# See https://adventofcode.com/2020/day/19

def load():
    with open("input.txt") as f:
        rule_block, message_block = f.read().replace("\r", "").split("\n\n")
        rules = dict([(rule_no, parse_rule(rule.strip()))
                      for rule_no, rule in
                      [rule_line.split(":") for rule_line in rule_block.split("\n")]
                      ])
        messages = message_block.split("\n")
    return rules, messages


def parse_rule(rule):
    if rule.startswith('"') and rule.endswith('"'):
        return rule[1:-1]
    else:
        return [option.strip().split(" ") for option in rule.split("|")]


# Checks if the given rule_no matches any prefixes of the message, and returns a collection of the possible remainder
# pieces of text after the prefixes are removed. An empty return value means no matches, and a return value
# containing an empty string means there was at least one full match with no remainder text.
def match_prefix(message, rules, rule_no):
    if message == "":
        return []

    rule = rules[rule_no]
    if type(rule) is str:
        if message[0] == rule:
            remainder = message[1:]
            return [remainder]
        else:
            return []

    results = set()
    for option in rule:
        remainders = [message]
        for sub_rule_no in option:
            new_remainders = set()
            for remainder in remainders:
                new_remainders.update(match_prefix(remainder, rules, sub_rule_no))
            remainders = new_remainders
        results.update(remainders)

    return results


def count_full_matches(rules, messages):
    count = 0
    for message in messages:
        if "" in match_prefix(message, rules, "0"):
            count += 1
    print(count)


def part1():
    rules, messages = load()
    count_full_matches(rules, messages)


def part2():
    rules, messages = load()
    rules["8"] = parse_rule("42 | 42 8")
    rules["11"] = parse_rule("42 31 | 42 11 31")
    count_full_matches(rules, messages)


part1()
part2()
