#!/usr/bin/python3
# Advent of code 2021 day 4
# See https://adventofcode.com/2021/day/4

with open("input.txt") as f:
    lines = f.readlines()


def load_boards(lines):
    boards = []
    for i in range(2, len(lines), 6):
        board = []
        for y in range(0, 5):
            board.append([int(v) for v in lines[i + y].split(" ") if v.strip()])
        boards.append(board)
    return boards


def is_board_full(board, called_numbers):
    for row in board:
        if all(v in called_numbers for v in row):
            return True

    for x in range(0, len(board[0])):
        column = [board[y][x] for y in range(0, len(board))]
        if all(v in called_numbers for v in column):
            return True

    return False


def get_unmarked_numbers(board, called_numbers):
    return [v for row in board for v in row if v not in called_numbers]


def play_game(boards, numbers):
    finished_boards = []
    for i in range(0, len(numbers)):
        called_numbers = numbers[0:i]
        for b in range(0, len(boards)):
            if b not in finished_boards and is_board_full(boards[b], called_numbers):
                score = sum(get_unmarked_numbers(boards[b], called_numbers))
                last_number = called_numbers[-1]
                print(score * last_number)
                finished_boards.append(b)


play_game(boards=load_boards(lines), numbers=[int(v) for v in lines[0].split(",")])
