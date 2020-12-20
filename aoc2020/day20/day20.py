#!/usr/bin/python3
# Advent of code 2020 day 20
# See https://adventofcode.com/2020/day/20

from math import isqrt
import aoc2020.modules.grid as g

with open("sea_monster.txt") as f:
    sea_monster = f.readlines()


def load_tiles():
    with open("input.txt") as f:
        blocks = f.read().replace("\r", "").split("\n\n")

    tiles = {}
    for block in blocks:
        lines = block.split("\n")
        tile_no = int(lines[0].removeprefix("Tile ").removesuffix(":"))
        tile = g.parse_grid("\n".join(lines[1:]))
        tiles[tile_no] = tile

    return tiles


def matches_top(place_tile, match_tile):
    if match_tile is None or place_tile is None:
        return True
    (min_x, min_y), (max_x, max_y) = match_tile.get_bounds()
    top_row = "".join([match_tile[x, min_y] for x in range(min_x, max_x)])
    (min_x, min_y), (max_x, max_y) = place_tile.get_bounds()
    bottom_row = "".join([place_tile[x, max_y - 1] for x in range(min_x, max_x)])
    return top_row == bottom_row


def matches_bottom(place_tile, match_tile):
    return matches_top(match_tile, place_tile)


def matches_left(place_tile, match_tile):
    if match_tile is None or place_tile is None:
        return True
    (min_x, min_y), (max_x, max_y) = match_tile.get_bounds()
    left_column = "".join([match_tile[min_x, y] for y in range(min_y, max_y)])
    (min_x, min_y), (max_x, max_y) = place_tile.get_bounds()
    right_column = "".join([place_tile[max_x - 1, y] for y in range(min_y, max_y)])
    return right_column == left_column


def matches_right(place_tile, match_tile):
    return matches_left(match_tile, place_tile)


def get_blank_spaces(board, tile_count):
    (min_x, min_y), (max_x, max_y) = get_bounds(board)
    board_size = isqrt(tile_count)
    if max_x - min_x < board_size:
        min_x -= 1
        max_x += 1
    if max_y - min_y < board_size:
        min_y -= 1
        max_y += 1
    result = []
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            if (x, y) not in board.keys() and (
                    (x + 1, y) in board.keys() or
                    (x - 1, y) in board.keys() or
                    (x, y + 1) in board.keys() or
                    (x, y - 1) in board.keys()
            ):
                result.append((x, y))
    return result


def get_bounds(board):
    min_x = min([x for x, y in board.keys()])
    max_x = max([x for x, y in board.keys()]) + 1
    min_y = min([y for x, y in board.keys()])
    max_y = max([y for x, y in board.keys()]) + 1
    return (min_x, min_y), (max_x, max_y)


def get_tile(board, x, y):
    cell = board.get((x, y))
    return cell[1] if cell else None


def try_placing_tile(place_tile, board, tiles):
    possible_place_tiles = []
    for x, y in get_blank_spaces(board, len(tiles)):
        for rotate_place in range(0, 4):
            for flip in range(0, 2):
                if matches_top(place_tile, get_tile(board, x, y + 1)) and \
                        matches_right(place_tile, get_tile(board, x - 1, y)) and \
                        matches_bottom(place_tile, get_tile(board, x, y - 1)) and \
                        matches_left(place_tile, get_tile(board, x + 1, y)):
                    possible_place_tiles.append(((x, y), place_tile))
                place_tile = place_tile.flip_y()
            place_tile = place_tile.rotate_cw()
    return possible_place_tiles


def find_solution(board, remaining_tiles, tiles):
    if not remaining_tiles:
        return board

    for place_tile_no, place_tile in remaining_tiles.items():
        for coords, placed_tile in try_placing_tile(place_tile, board, tiles):
            print(f"Progress: {len(remaining_tiles)} remaining")
            new_board = dict(board)
            new_board[coords] = (place_tile_no, placed_tile)
            new_remaining_tiles = dict(remaining_tiles)
            del new_remaining_tiles[place_tile_no]
            solution = find_solution(new_board, new_remaining_tiles, tiles)
            if solution:
                return solution

    return None


def format_output(solution):
    lines = []
    (min_x, min_y), _ = get_bounds(solution)
    for row in range(0, 12 * 8):
        line = []
        for column in range(0, 12 * 8):
            tile_no, tile = solution[(min_x + row // 8, min_y + column // 8)]
            tile_min_x, tile_min_y = tile.get_origin()
            cell = tile[(tile_min_x + (row % 8) + 1, tile_min_y + (column % 8) + 1)]
            line.append(cell)
        lines.append("".join(line))
    return "\n".join(lines)


def part1():
    tiles = load_tiles()
    remaining_tiles = dict(tiles)

    # Place one tile on the board
    tile_no, tile = list(remaining_tiles.items())[0]
    initial_board = {(0, 0): (tile_no, tile)}
    del remaining_tiles[tile_no]

    # Place the remaining tiles
    solution = find_solution(initial_board, remaining_tiles, tiles)

    # Find corners
    (min_x, min_y), (max_x, max_y) = get_bounds(solution)
    print("Part 1:", solution[(min_x, min_y)][0] * solution[(min_x, max_y - 1)][0] * solution[(max_x - 1, min_y)][0] *
          solution[(max_x - 1, max_y - 1)][0])

    return solution


def is_sea_monster(grid, X, Y):
    for y, sm_row in enumerate(sea_monster):
        for x, sm_char in enumerate(sm_row.strip()):
            map_char = grid.get((X + x, Y + y))
            if (sm_char == "#" or sm_char == "O") and map_char != "#":
                return None

    copy = g.Grid(grid.grid)
    for y, sm_row in enumerate(sea_monster):
        for x, sm_char in enumerate(sm_row.strip()):
            if sm_char == "#":
                copy[(X + x, Y + y)] = "O"

    return copy


def find_sea_monsters(grid):
    count = 0
    (min_x, min_y), (max_x, max_y) = grid.get_bounds()
    for Y in range(min_y, max_y):
        for X in range(min_x, max_x):
            match = is_sea_monster(grid, X, Y)
            if match:
                count += 1
                grid = match
    return count, len([c for c in grid.grid.values() if c == "#"])


def part2(monster_map):
    grid = g.parse_grid(monster_map)
    for rotate in range(0, 4):
        for flip in range(0, 2):
            monsters, roughness = find_sea_monsters(grid)
            if monsters:
                print(f"Part 2: Found {monsters} monsters, with sea roughness {roughness}")
            grid = grid.flip_x()
        grid = grid.rotate_cw()


solution = part1()
monster_map = format_output(solution)
part2(monster_map)
