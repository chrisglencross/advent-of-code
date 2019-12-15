#!/usr/bin/python3
# Advent of code 2019 day 15

import networkx as nx

from aoc2019.modules import intcode
from aoc2019.modules.imagegridprinter import ImageGridPrinter
from aoc2019.modules.intcode import Program

DIRECTIONS = {
    "north": (1, (0, -1)),
    "east": (4, (1, 0)),
    "south": (2, (0, 1)),
    "west": (3, (-1, 0)),
}

GENERATE_ANIMATED_GIF = True


def move_location(location, direction_name):
    move = DIRECTIONS[direction_name][1]
    return location[0] + move[0], location[1] + move[1]


def add_locations_to_check(grid, location):
    for direction in DIRECTIONS.keys():
        new_location = move_location(location, direction)
        if new_location not in grid.keys():
            grid[new_location] = "?"


def find_direction(location, neighbour):
    for direction in DIRECTIONS.keys():
        if move_location(location, direction) == neighbour:
            return direction
    return None


def manhatten_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_route(grid, location, target):
    # Find cells containing this target character, and find the closest
    target_cells = [loc for loc, cell in grid.items() if cell == target]
    if not target_cells:
        return None
    target_loc = min(target_cells, key=lambda loc: manhatten_distance(location, loc))
    if target_loc == location:
        raise Exception("Finding route to self should not happen")

    # Build a graph, with each grid cell as a node, and edges connecting (possibly) navigable cells
    graph = nx.DiGraph()
    for loc, cell in grid.items():
        graph.add_node(loc, symbol=cell)
    for loc, cell in grid.items():
        if cell in {"#", " ", "?"}:
            continue
        for direction in DIRECTIONS.keys():
            neighbour_loc = move_location(loc, direction)
            if grid[neighbour_loc] in {"#", " "}:
                continue
            graph.add_edge(loc, neighbour_loc, direction=direction)

    # Dijkstra's algorithm
    return nx.shortest_path(graph, location, target_loc)


def follow_route(program: Program, grid, location, route):
    for new_location in route:
        direction = find_direction(location, new_location)
        direction_command = DIRECTIONS[direction][0]
        program.input.append(direction_command)
        output = program.next_output()
        content = grid[new_location]
        if output == 0 and content != "?":
            raise Exception("Hit a wall while following a route. That should not happen.")
        elif output == 0 and content == "?":
            grid[new_location] = "#"
            break
        elif output == 1:
            if content in {"?", " "}:
                grid[new_location] = "."
            elif content != ".":
                raise Exception(f"Internal error: cell {new_location} turned from {content} to .")
        elif output == 2:
            if content in {"?", " "}:
                grid[new_location] = "o"
            elif content != "o":
                raise Exception(f"Internal error: cell {new_location} turned from {content} to o")
        location = new_location
    return location


def build_grid():
    grid = {}
    location = (0, 0)
    program = intcode.load_file("input.txt", debug=False)

    # grid_printer = NoOpGridPrinter()
    grid_printer = ImageGridPrinter(filename="map.gif", max_height=400, max_width=400, duration=20, sample=4,
                                    colour_map={"#": (255, 255, 255), ".": (0, 0, 0), "?": (128, 128, 128),
                                                "D": (255, 0, 0), "o": (0, 255, 0)})
    # grid_printer = TextGridPrinter(symbol_map={0: " "})

    grid[(0, 0)] = "."
    while True:
        add_locations_to_check(grid, location)
        print_grid(grid_printer, grid, location)
        # Find a location to check nearby
        route = find_route(grid, location, "?")
        if route is None:
            break
        location = follow_route(program, grid, location, route[1:])

    grid_printer.close()

    return grid


def print_grid(grid_printer, grid, location):
    if grid_printer is None:
        return
    grid = dict(grid)
    if location is not None:
        grid[location] = "D"
    grid_printer.print(grid)


def part1(grid):
    # Part 1: Find the route from the origin to the oxygen
    route = find_route(grid, (0, 0), "o")
    print(len(route) - 1)


def part2(grid):
    # Part 2: Find the furthest point from any cell to the oxygen
    longest_route = []
    for location, symbol in grid.items():
        if symbol == ".":
            route = find_route(grid, location, "o")
            if len(route) > len(longest_route):
                longest_route = route
    print(len(longest_route) - 1)


def main():
    print("Building grid")
    grid = build_grid()
    print("Part 1")
    part1(grid)
    print("Part 2")
    part2(grid)


if __name__ == "__main__":
    main()
