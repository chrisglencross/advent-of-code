#!/usr/bin/python3
# Advent of code 2021 day 21
# See https://adventofcode.com/2021/day/21
import collections

with open("input.txt") as f:
    start_positions = [int(line.strip().split(": ")[-1]) for line in f.readlines()]


def part1(start_positions):
    scores = [0, 0]
    rolls = 0
    player_turn = 0
    positions = list(start_positions)
    while not any(score >= 1000 for score in scores):
        total_rolled = rolls * 3 + 6
        rolls += 3
        positions[player_turn] = (positions[player_turn] - 1 + total_rolled) % 10 + 1
        scores[player_turn] += positions[player_turn]
        player_turn = 1 - player_turn
    return rolls * min(scores)


def part2(start_positions):
    ROLL_UNIVERSES = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    games_in_progress = {((start_positions[0], 0), (start_positions[1], 0)): 1}
    won_games = [0, 0]
    player_turn = 0
    while games_in_progress:
        new_games_in_progress = collections.defaultdict(lambda: 0)
        for game_state, state_universes in games_in_progress.items():
            for total_rolled, roll_universes in ROLL_UNIVERSES.items():

                p, s = game_state[player_turn]
                new_pos = (p - 1 + total_rolled) % 10 + 1
                new_score = s + new_pos
                new_universes = roll_universes * state_universes

                if new_score >= 21:
                    won_games[player_turn] += new_universes
                else:
                    new_game_state = list(game_state)
                    new_game_state[player_turn] = (new_pos, new_score)
                    new_games_in_progress[tuple(new_game_state)] += new_universes

        games_in_progress = new_games_in_progress
        player_turn = 1 - player_turn

    return max(won_games)


print(part1(start_positions))
print(part2(start_positions))
