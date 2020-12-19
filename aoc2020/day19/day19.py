#!/usr/bin/python3
# Advent of code 2020 day 19
# See https://adventofcode.com/2020/day/19


def parse_rule(rule):
    if rule.startswith('"') and rule.endswith('"'):
        return rule[1:-1]
    else:
        return [option.strip().split(" ") for option in rule.split("|")]


# Checks if the given rule matches a prefix of the message and returns a list of the possible remaining pieces of text
# after the match. Notably for the return value:
#   * Empty list means match is impossible
#   * List containing an empty string means there was at least one full match
def prefix_matches(message, rule_no, rules):
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
                new_remainders.update(prefix_matches(remainder, sub_rule_no, rules))
            remainders = new_remainders
        results.update(remainders)

    return results


def count_matches(rules, messages):
    count = 0
    for message in messages:
        if "" in prefix_matches(message, "0", rules):
            count += 1
    print(count)


with open("input.txt") as f:
    rule_block, message_block = f.read().replace("\r", "").split("\n\n")
    rules = dict([(rule_no, parse_rule(rule.strip()))
                  for rule_no, rule in
                  [rule_line.split(":") for rule_line in rule_block.split("\n")]
                  ])
    messages = message_block.split("\n")

# Part 1
count_matches(rules, messages)

# Part 2
rules["8"] = parse_rule("42 | 42 8")
rules["11"] = parse_rule("42 31 | 42 11 31")
count_matches(rules, messages)
