#!/usr/bin/python3
# Advent of code 2023 day 10
# See https://adventofcode.com/2023/day/10
import networkx as nx

from aoc2023.modules import grid as g
from aoc2023.modules import directions as d

connections = {
    "|": {"N", "S"},
    "-": {"E", "W"},
    "L": {"N", "E"},
    "J": {"N", "W"},
    "7": {"S", "W"},
    "F": {"S", "E"},
    "S": {"N", "E", "S", "W"}
}


# Part 1
def distance_function(grid, from_coord, to_coord):
    from_cell = grid[from_coord]
    to_cell = grid[to_coord]
    if from_cell not in connections.keys() or to_cell not in connections.keys():
        return None
    for direction in connections[from_cell]:
        cd = d.COMPASS_DIRECTIONS[direction]
        neighbour = cd.move(from_coord)
        if neighbour == to_coord and cd.reverse().name in connections[to_cell]:
            return 1
    return None


grid = g.load_grid("input.txt")
graph = grid.build_graph(distance_function=distance_function)

# Create a path between start and end where end is adjacent to start
start = grid.find_cell("S")
final_edge_in_loop = [(f, t) for f, t in graph.edges() if f == start or t == start][0]
end = [n for n in final_edge_in_loop if n != start][0]
graph.remove_edge(*final_edge_in_loop)

path = nx.shortest_path(graph, source=start, target=end)
print(len(path)//2)


# Part 2
def flood_fill(grid, start, boundary, symbol):
    is_edge = False
    stack = [start]
    while stack:
        c = stack.pop()
        if c not in grid.keys():
            is_edge = True
        elif grid[c] != symbol and c not in boundary:
            grid[c] = symbol
            for direction in d.COMPASS_DIRECTIONS.values():
                stack.append(direction.move(c))
    return is_edge


# Flood fill the areas to the left and the right of the path and track which region hits the edge
boundary = set(path)
left_external = False
for f, t in zip(path, path[1:] + [path[0]]):
    moving_direction = [d for d in d.COMPASS_DIRECTIONS.values() if d.move(f) == t][0]
    left = moving_direction.turn_left()
    left_external |= flood_fill(grid, left.move(f), boundary, "l")
    left_external |= flood_fill(grid, left.move(t), boundary, "l")
    right = moving_direction.turn_right()
    flood_fill(grid, right.move(f), boundary, "r")
    flood_fill(grid, right.move(t), boundary, "r")
internal_region = "r" if left_external else "l"
print(len(grid.find_cells(internal_region)))
