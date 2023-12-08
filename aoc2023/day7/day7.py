#!/usr/bin/python3
# Advent of code 2023 day 7
# See https://adventofcode.com/2023/day/7

from itertools import groupby

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

HAND_TYPE_SCORES = {
    tuple([5]): 7,
    (1, 4): 6,
    (2, 3): 5,
    (1, 1, 3): 4,
    (1, 2, 2): 3,
    (1, 1, 1, 2): 2,
    (1, 1, 1, 1, 1): 1,
}

CARD_SCORES = {str(i): i for i in range(2, 10)} | {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

def score_hands(hands):
    score = 0
    for i, hand in enumerate(sorted(hands)):
        rank = i+1
        bid = hand[3]
        score += bid * rank
    return score


# Part 1
def get_hand_type_score(cards):
    hand_type = tuple(sorted([len(list(v)) for k, v in groupby(sorted(list(cards)))]))
    return HAND_TYPE_SCORES[hand_type]

hands = []
for line in lines:
    cards, bid = line.split()
    hands.append((get_hand_type_score(cards), [CARD_SCORES[c] for c in cards], cards, int(bid)))
print(score_hands(hands))


# Part 2
CARD_SCORES["J"] = 0

def get_hand_type_score_with_joker(cards):
    jokers = sum(1 for card in cards if card == "J")
    cards_without_jokers = [card for card in cards if card != "J"]
    card_groups = sorted([len(list(v)) for k, v in groupby(sorted(list(cards_without_jokers)))])
    if len(card_groups) == 0:
        card_groups = [jokers]  # all cards are jokers
    else:
        card_groups[-1] += jokers
    hand_type = tuple(card_groups)
    return HAND_TYPE_SCORES[hand_type]


hands = []
for line in lines:
    cards, bid = line.split()
    hands.append((get_hand_type_score_with_joker(cards), [CARD_SCORES[c] for c in cards], cards, int(bid)))
print(score_hands(hands))
