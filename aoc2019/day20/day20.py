#!/usr/bin/python3
# Advent of code 2019 day 20
import networkx as nx

from aoc2019.modules.directions import COMPASS_DIRECTIONS
from aoc2019.modules.grid import load_grid


def is_outer_portal(grid, portal):
    (min_x, min_y), (max_x, max_y) = grid.get_bounds()
    return abs(portal[0] - max_x) <= 2 or abs(portal[0] - min_x) <= 2 \
           or abs(portal[1] - max_y) <= 2 or abs(portal[1] - min_y) <= 2


def find_portals(grid):
    # Returns a dictionary where keys are portal names and each value is a pair of portal coordinates.
    # The outer portal is always the first in the pair. AA and ZZ appear as portals with a None inner coordinate.
    result = {}
    for coord, cell in grid.items():
        if cell == ".":
            for direction in COMPASS_DIRECTIONS.values():
                label1 = direction.move(coord)
                label2 = direction.move(label1)
                label1, label2 = sorted([label1, label2])
                if grid.get(label1) and grid.get(label2):
                    label = grid.get(label1) + grid.get(label2)
                    if label.isalpha():
                        if label not in result.keys():
                            result[label] = [None, None]
                        if is_outer_portal(grid, coord):
                            result[label][0] = coord
                        else:
                            result[label][1] = coord
    return result


def print_portals_traversed(graph: nx.DiGraph, route):
    portals = []
    for step_no, move_to in enumerate(route[1:]):
        move_from = route[step_no]
        edge_data = graph.get_edge_data(move_from, move_to)
        if edge_data and "portal" in edge_data:
            portals.append(edge_data["portal"])
    print("Route:", ", ".join(portals))


def part1():
    grid = load_grid("input.txt")
    grid.print()
    graph = grid.build_graph()
    portals = find_portals(grid)
    for portal_name, portal_coords in portals.items():
        if portal_coords[0] and portal_coords[1]:
            graph.add_edge(portal_coords[0], portal_coords[1], portal=portal_name, distance=1)
    start = portals["AA"][0]
    end = portals["ZZ"][0]
    path = nx.shortest_path(graph, start, end, weight="distance")
    print_portals_traversed(graph, path)
    print(len(path) - 1)


def part2():
    maze = load_grid("input.txt")
    portals = find_portals(maze)
    max_depth = len(portals) + 1

    # Build a graph with each node in 3d space
    # Would be more efficient to take the graph from part 1 and just add portal-to-portal edges, but this completes
    # in less than 30 seconds so not necessary.

    graph = nx.Graph()

    # Build multiple sub-graphs, one for each inception level, with a depth on each node
    for inception in range(0, max_depth):
        maze.add_graph_edges(graph, node_factory=lambda coords: (inception, coords))

    # Add the edges between levels
    for portal_name, portal_coords in portals.items():
        if portal_coords[0] and portal_coords[1]:
            for inception in range(0, max_depth):
                # Let's go deeper - inner portal to outer portal
                graph.add_edge((inception, portal_coords[1]), (inception + 1, portal_coords[0]),
                               portal=portal_name + str(inception + 1), distance=1)
                if inception > 0:
                    # Outer portal to inner portal
                    graph.add_edge((inception, portal_coords[0]), (inception - 1, portal_coords[1]),
                                   portal=portal_name + str(inception - 1), distance=1)

    start = (0, portals["AA"][0])
    end = (0, portals["ZZ"][0])
    path = nx.shortest_path(graph, start, end, weight="distance")
    print_portals_traversed(graph, path)
    print(len(path) - 1)


if __name__ == "__main__":
    part1()
    part2()
