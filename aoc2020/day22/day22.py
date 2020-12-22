#!/usr/bin/python3
# Advent of code 2020 day 22
# See https://adventofcode.com/2020/day/22


def load_cards():
    with open("input.txt") as f:
        return [[int(line) for line in block.split("\n")[1:]] for block in f.read().replace("\r", "").split("\n\n")]


def play_game_1(cards):
    round = 0
    while all(cards):
        round += 1
        print(f"Round {round}")
        for i, c in enumerate(cards):
            print(f"Player {i+1}'s deck: {c}")
        played_cards = sorted([(player, cards[player].pop(0)) for player in range(0, 2)], key=lambda p: p[1], reverse=True)
        for player, player_card in played_cards:
            print(f"Player {player} plays: {player_card}")
        winner_player = played_cards[0][0]
        print(f"Player {winner_player+1} wins the round!")
        print()
        cards[winner_player].extend([card[1] for card in played_cards])
    return winner_player, cards[winner_player]


def play_game_2(game_no, cards):
    played_rounds = set()

    round = 0
    while all(cards):

        round += 1
        print(f"Round {round} (Game {game_no})")
        for i, c in enumerate(cards):
            print(f"Player {i+1}'s deck: {c}")

        # Player 0 wins if we've been here before
        round_state = tuple(tuple(player_cards) for player_cards in cards)
        if round_state in played_rounds:
            print(f"Player 1 wins: Repeated round")
            return 0, cards[0]
        played_rounds.add(round_state)

        played_cards = [(player, cards[player].pop(0)) for player in range(0, 2)]
        for player, player_card in played_cards:
            print(f"Player {player} plays: {player_card}")

        if all([len(cards[player]) >= played_card for player, played_card in played_cards]):
            print(f"Playing a sub-game to determine the winner")
            subcards = [cards[player][0:played_card] for player, played_card in played_cards]
            winner_player, _ = play_game_2(game_no+1, subcards)
            print(f"...anyway, back to game {game_no}")
            pass
        else:
            sorted_played_cards = sorted(played_cards, key=lambda p: p[1], reverse=True)
            winner_player = sorted_played_cards[0][0]
        print(f"Player {winner_player+1} wins the round!")
        print()
        cards[winner_player].extend([played_card for player, played_card in played_cards if player == winner_player])
        cards[winner_player].extend([played_card for player, played_card in played_cards if player != winner_player])

    print(f"The winner of game {game_no} is player {winner_player+1}!")
    return winner_player, cards[winner_player]

def calc_score(winning_hand):
    return sum([i*int(c) for i, c in enumerate(reversed(winning_hand), start=1)])


_, winning_hand = play_game_1(load_cards())
print("Part 1:", calc_score(winning_hand))

_, winning_hand = play_game_2(1, load_cards())
print("Part 2:", calc_score(winning_hand))
