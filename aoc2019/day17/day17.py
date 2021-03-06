#!/usr/bin/python3
# Advent of code 2019 day 17

from typing import List

from aoc2019.modules import intcode
from aoc2019.modules.textgridprinter import TextGridPrinter

DIRECTIONS = {
    "^": ((0, -1), ("<", ">", "v")),
    ">": ((1, 0), ("^", "v", "<")),
    "v": ((0, 1), (">", "<", "^")),
    "<": ((-1, 0), ("v", "^", ">"))
}


def load_grid():
    program = intcode.load_file("input.txt", debug=False)
    x = 0
    y = 0
    grid = {}
    while not program.is_terminated():
        cell = program.next_output()
        if cell is None:
            break
        if cell == 10:
            x = 0
            y += 1
        else:
            grid[(x, y)] = chr(cell)
            x = x + 1
    return grid


def move_direction(location, direction):
    move = DIRECTIONS[direction][0]
    new_location = (location[0] + move[0], location[1] + move[1])
    if 0 <= new_location[0] <= max_x and 0 <= new_location[1] <= max_y and grid[new_location] in "O#":
        return new_location
    else:
        return None


def get_intersections():
    intersections = []
    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            if grid[(x, y)] == "#":
                scaffold_neighbours = 0
                for direction in DIRECTIONS.keys():
                    neighbour = move_direction((x, y), direction)
                    if neighbour is not None and grid[neighbour] == "#":
                        scaffold_neighbours += 1
                if scaffold_neighbours >= 3:
                    intersections.append((x, y))
    return intersections


grid = load_grid()
grid_printer = TextGridPrinter()
grid_printer.print(grid)

xs = [c[0] for c in grid.keys()]
ys = [c[1] for c in grid.keys()]
max_x = max(xs)
max_y = max(ys)

# Part 1
intersections = get_intersections()
for intersection in intersections:
    grid[intersection] = "O"
print(sum([c[0] * c[1] for c in intersections]))


# Part 2


def turn_left(direction):
    return DIRECTIONS[direction][1][0]


def turn_right(direction):
    return DIRECTIONS[direction][1][1]


def print_grid(grid, location, direction, visited_locations):
    debug_grid = dict(grid)
    for l in visited_locations:
        debug_grid[l] = "@"
    debug_grid[location] = direction
    grid_printer.print(debug_grid)


# Get the directions we can move in from the current location, in order of preference
def get_possible_turn_directions(location, facing_direction, visited_locations) -> List[str]:
    unvisited_directions = []
    visited_directions = []
    for command, new_direction in [("L", turn_left(facing_direction)),
                                   ("R", turn_right(facing_direction))]:
        # ("LL", reverse(facing_direction))]: no reversing at the moment
        new_location = move_direction(location, new_direction)
        if new_location is not None:
            if new_location in visited_locations:
                visited_directions.append((new_direction, command))
            else:
                unvisited_directions.append((new_direction, command))
    # return unvisited_directions + visited_directions # First try to find a solution without doubling back
    return unvisited_directions


def get_route(prefix, location, direction, visited_locations, cycle_detector):
    cycle_detector = dict(cycle_detector)

    # We can have the ability to call 10 functions, each can be 20 characters long
    prefix_str = ",".join([str(step) for step in prefix])
    # print(prefix_str)
    if len(prefix_str) > 200 + 3:  # no trailing commas in each function
        return

    previous = cycle_detector.get((location, direction))
    if previous == len(visited_locations):
        # We're in a cycle without achieving anything new
        return
    cycle_detector[(location, direction)] = len(visited_locations)

    # If all grid cells visited, done
    if len(visited_locations) == total_scaffold:
        yield prefix
        return

    # First search for solutions where we continue head on from the junction (fewer steps)

    # Try moving forward until we hit a 'O' or cannot move forward any more
    if move_direction(location, direction):
        yield from move_forward(prefix, location, direction, visited_locations, cycle_detector)

    # Now instead try turning if we have not already just turned
    if not prefix or prefix[-1] not in ['R', 'L']:
        for new_direction, turn_command in get_possible_turn_directions(location, direction, visited_locations):
            yield from get_route(prefix + list(turn_command), location, new_direction, visited_locations,
                                 cycle_detector)


def move_forward(prefix, location, direction, visited_locations, cycle_detector):
    visited_locations = set(visited_locations)

    count = 0
    next_location = move_direction(location, direction)
    while next_location is not None:
        location = next_location
        visited_locations.add(location)
        count = count + 1
        if grid[location] == "O":
            # We've reached a junction
            break
        next_location = move_direction(location, direction)
    if isinstance(prefix[-1], int):
        new_prefix = list(prefix)
        new_prefix[-1] += count
    else:
        new_prefix = prefix + [count]
    yield from get_route(new_prefix, location, direction, visited_locations, cycle_detector)


total_scaffold = sum([1 for value in grid.values() if value in "#O^><v"])
location = [i[0] for i in grid.items() if i[1] in "^><v"][0]
direction = grid[location]

print_grid(grid, location, direction, set())
grid[location] = "#"

print("Enumerating reasonable routes")
routes = []
for route in get_route([], location, direction, set([location]), dict()):
    print(len(routes), len(route), ",".join([str(step) for step in route]))
    routes.append(route)
    # In our case we can stop after the first one, because it's the best - no unnecessary turns
    # Enumerating all routes with all possible turns is very slow.
    break

route_steps = [str(step) for step in routes[0]]


def find_function_candidates(remaining_segments):
    """Finds the best candidate functions from the instruction segments. These are the repeating subsequences which are
    longest and are used the most times."""
    segment_counts = {}
    for segment in remaining_segments:
        for start in range(0, len(segment)):
            for end in range(start + 1, len(route_steps)):
                subsegment = tuple(segment[start:end + 1])
                if len(",".join(subsegment)) <= 20:
                    segment_counts[subsegment] = segment_counts.get(subsegment, 0) + 1

    result = []
    for sequence, count in dict(segment_counts).items():
        if count > 1:
            result.append((list(sequence), count))
    result.sort(reverse=True, key=lambda seq: len(seq[0]) * seq[1])
    return result


def find_first_sublist(seq, sublist, start=0):
    length = len(sublist)
    for index in range(start, len(seq)):
        if seq[index:index + length] == sublist:
            return index, index + length


def replace_sublist(seq, sublist, replacement):
    length = len(replacement)
    index = 0
    for start, end in iter(lambda: find_first_sublist(seq, sublist, index), None):
        seq[start:end] = replacement
        index = start + length


def find_functions(remaining_segments, functions):
    """Finds the 3 functions which together can replace the input segments. Searches candidate functions using
    a recursive implementation."""
    if len(functions) > 3:
        return None
    if len(remaining_segments) == 0:
        return functions
    if len(functions) == 3:
        return None

    function_candidates = find_function_candidates(remaining_segments)
    for i, function_candidate in enumerate(function_candidates):
        new_functions = list(functions)
        new_functions.append(function_candidate[0])
        new_remaining_segments = []
        for segment in remaining_segments:
            for start, end in iter(lambda: find_first_sublist(segment, function_candidate[0]), None):
                if start > 0:
                    new_remaining_segments.append(segment[0:start])
                segment = segment[end:]
            if segment:
                new_remaining_segments.append(segment)
        solution = find_functions(new_remaining_segments, new_functions)
        if solution is not None:
            return solution

    return None


# Identify the functions to use and the sequence of functions to call
functions = find_functions([route_steps], [])
named_functions = {}
function_sequence = list(route_steps)
for i, function in enumerate(functions):
    function_name = chr(65 + i)
    named_functions[function_name] = ",".join(function)
    replace_sublist(function_sequence, function, function_name)

print(function_sequence)
print(named_functions)

def encode(value):
    return [ord(c) for c in value] + [10]


# Re-run the program with these functions to obtain the answer
program = intcode.load_file("input.txt", debug=False)
program.memory[0] = 2
program.input.extend(encode(",".join(function_sequence)))
program.input.extend(encode(named_functions["A"]))
program.input.extend(encode(named_functions["B"]))
program.input.extend(encode(named_functions["C"]))
program.input.extend(encode("n"))

# Print the output - final number is the answer
result = None
message = []
while not program.is_terminated():
    output = program.next_output()
    if output is None:
        break
    if output > 255:
        result = output
    else:
        message.append(chr(output))
print("".join(message))
print(result)
