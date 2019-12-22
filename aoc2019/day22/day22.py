#!/usr/bin/python3
# Advent of code 2019 day 22

from typing import List


# The _expr functions return an expression tree node for calculating the output position in the deck from a given
# input position. Input positions can be other expressions, in which case the resultant expression will be a tree.
# Expression results should be evaluated modulo the deck size. All expression tree nodes are tuples of the form
# (int_value, operator, expression) except for the leaf tuple representing the input value which is a
# string "c". This makes optimising the expression tree easier.


def deal_into_new_stack(deck: List):
    return list(reversed(deck))


def deal_into_new_stack_expr(input_pos):
    return -1, '-', input_pos


def cut(deck: List, n: int):
    return deck[n:] + deck[0:n]


def cut_expr(n, input_pos):
    return -n, "+", input_pos


def deal_with_increment(deck: List, n: int):
    positions = len(deck)
    new_deck = [None] * positions
    to_pos = 0
    for card in deck:
        new_deck[to_pos] = card
        to_pos = (to_pos + n) % positions
    return new_deck


def deal_with_increment_expr(n, input_pos):
    return n, '*', input_pos


# Inverse mod function taken from a Google search - can't remember where exactly,
# but something like https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/

def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    return gcd, y1 - (b // a) * x1, x1


def mod_inverse(a, m):
    g, x, y = gcd_extended(a, m)
    if g != 1:
        raise Exception(f"Inverse does not exist: {a}, {m}")
    return (x % m + m) % m


def invert_plus_minus(symbol):
    if symbol == "+":
        return "-"
    elif symbol == "-":
        return "+"
    else:
        raise Exception("Internal error")


def evaluate_expression(expression, deck_len, start_pos):
    if type(expression) is int:
        return expression
    elif expression == "c":
        # c is the variable representing the card start position
        return start_pos % deck_len
    elif type(expression) is tuple:
        lhs = evaluate_expression(expression[0], deck_len, start_pos)
        op = expression[1]
        rhs = evaluate_expression(expression[2], deck_len, start_pos)
        if op == "+":
            return (lhs + rhs) % deck_len
        elif op == "-":
            return (lhs - rhs) % deck_len
        elif expression[1] == "*":
            return (lhs * rhs) % deck_len
        else:
            raise Exception(f"Bad operator {expression[1]}")
    else:
        raise Exception(f"Bad expression: {expression}")


def simplify_expression(expression):

    if type(expression) is not tuple:
        return expression

    lhs = simplify_expression(expression[0])
    op = expression[1]
    rhs = simplify_expression(expression[2])

    if type(lhs) is int and type(rhs) is tuple and type(rhs[0] is int):
        # Simplify (a op1 (b op2 E)) where a, b are integers
        op2 = rhs[1]
        if op == "*" and op2 == "*":
            # a * (b * E) => (a * b) * E
            return simplify_expression((lhs * rhs[0], '*', rhs[2]))
        elif op == "*" and op2 in "-+":
            # a * (b [+-] E) => a*b [+-] a*E
            return simplify_expression((lhs * rhs[0], op2, (lhs, '*', rhs[2])))
        elif op in "+" and op2 in "+-":
            # a + (b [+-] E) => (a+b) [+-] E
            return simplify_expression((lhs + rhs[0], op2, rhs[2]))
        elif op == "-" and op2 in "+-":
            # a - (b [+-] E) => (a-b) [-+] E
            return simplify_expression((lhs - rhs[0], invert_plus_minus(op2), rhs[2]))

    # No other simplifications required
    return lhs, op, rhs


def shuffle(deck):
    """Follows instructions to shuffle the deck, and returns the shuffled deck. It also returns an algebraic expression
    to be used in part 2 that calculates the output position of the shuffle for any given input position. The expression
    must be evaluated modulo the deck size."""
    with open("input.txt") as f:
        lines = f.readlines()
    expression = "c"
    for line in lines:
        line = line.strip()
        if line.startswith("deal into new stack"):
            deck = deal_into_new_stack(deck)
            expression = deal_into_new_stack_expr(expression)
        elif line.startswith("cut"):
            n = int(line.split(" ")[-1])
            deck = cut(deck, n)
            expression = cut_expr(n, expression)
        elif line.startswith("deal with increment"):
            n = int(line.split(" ")[-1])
            deck = deal_with_increment(deck, n)
            expression = deal_with_increment_expr(n, expression)

        # Assertions in preparation for part 2
        # Check that we can build an expression which calculates the correct position algebraically
        # with modulo arithmetic
        pos2019 = deck.index(2019)
        assert evaluate_expression(expression, len(deck), 2019) == pos2019
        assert evaluate_expression(simplify_expression(expression), len(deck), 2019) == pos2019

    # Return the deck and the expression for part 2
    return deck, simplify_expression(expression)


# Part 1
initial_deck = list(range(0, 10007))
shuffled_deck, shuffle_expression = shuffle(initial_deck)
print("Part 1", shuffled_deck.index(2019))

# Part 2
iterations = 101741582076661
deck_len = 119315717514047
card_pos = 2020

# The expression for locating the position of a card after a shuffle is:
# new_card_pos = A + B * prev_card_pos
# You'll want to remove or change this assertion for your personal inputs...
assert shuffle_expression == (-3477865808702686900085753959259001600827908176407381603684399670, '+',
                              (479266488811915049360163333705199628427569459248496640000000, '*', 'c'))

# All arithmetic using A and B are modulo the deck length. We can modulo A and B by the deck length now.
# https://en.wikipedia.org/wiki/Modulo_operation#Properties_(identities)
A = shuffle_expression[0] % deck_len
B = shuffle_expression[2][0] % deck_len

# Rearranging this expression:
#    new_card_pos = A + B * prev_card_pos
# becomes:
#    prev_card_pos = (new_card_pos - A) * B_inverse
#    prev_card_pos = (new_card_pos * B_inverse) - (A * B_inverse)
# where B_inverse is the "inverse mod" of deck_len % B
# Inverse mod: https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
#              https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
B_inverse = mod_inverse(B, deck_len)

# We now need to apply "prev_card_pos = (new_card_pos * B_inverse) - (A * B_inverse)" iteratively approximately 10^14
# times (see iterations variable). We can't do that. This is the point where I got stuck and looked at the subreddit
# (cheat!) to get some help with the maths of turning this series into a simple calculation.
# This link explains: https://www.nayuki.io/page/fast-skipping-in-a-linear-congruential-generator

a = B_inverse
b = -A * B_inverse
m = deck_len
n = iterations
x = card_pos

# Magic from https://www.nayuki.io/res/fast-skipping-in-a-linear-congruential-generator/lcgrandom.py skip function
a1 = a - 1
ma = a1 * m
y = (pow(a, n, ma) - 1) // a1 * b
z = pow(a, n, m) * x
result = (y + z) % m

print("Part 2", result)
