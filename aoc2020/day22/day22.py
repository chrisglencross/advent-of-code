#!/usr/bin/python3
# Advent of code 2020 day 22
# See https://adventofcode.com/2020/day/22

import logging

logging.basicConfig(format="%(message)s")
logger = logging.getLogger('game')
logger.setLevel(logging.WARNING)


def load_cards():
    with open("input.txt") as f:
        return [[int(line) for line in block.split("\n")[1:]] for block in f.read().replace("\r", "").split("\n\n")]


def play_game(game_no, cards, recurse=False):
    played_rounds = set()
    round_no = 0
    while all(cards):

        round_no += 1
        logger.info(f"Round {round_no} (Game {game_no})")
        for i, c in enumerate(cards):
            logger.info(f"Player {i + 1}'s deck: {c}")

        # Player 0 wins if we've been here before
        round_state = tuple(tuple(player_cards) for player_cards in cards)
        if round_state in played_rounds:
            logger.info(f"Player 1 wins: Repeated round_no")
            return 0, cards[0]
        played_rounds.add(round_state)

        played_cards = [(player, cards[player].pop(0)) for player in range(0, 2)]
        for player, player_card in played_cards:
            logger.info(f"Player {player} plays: {player_card}")

        if recurse and all([len(cards[player]) >= played_card for player, played_card in played_cards]):
            logger.info(f"Playing a sub-game to determine the winner")
            sub_cards = [cards[player][0:played_card] for player, played_card in played_cards]
            winner_player, _ = play_game(game_no + 1, sub_cards, True)
            logger.info(f"...anyway, back to game {game_no}")
            pass
        else:
            sorted_played_cards = sorted(played_cards, key=lambda p: p[1], reverse=True)
            winner_player = sorted_played_cards[0][0]

        logger.info(f"Player {winner_player + 1} wins the round_no!\n")
        cards[winner_player].extend([played_card for player, played_card in played_cards if player == winner_player])
        cards[winner_player].extend([played_card for player, played_card in played_cards if player != winner_player])

    logger.info(f"The winner of game {game_no} is player {winner_player + 1}!")
    return winner_player, cards[winner_player]


def calc_score(winning_hand):
    return sum([i * int(c) for i, c in enumerate(reversed(winning_hand), start=1)])


_, winning_hand = play_game(1, load_cards(), False)
print("Part 1:", calc_score(winning_hand))

_, winning_hand = play_game(1, load_cards(), True)
print("Part 2:", calc_score(winning_hand))
