#!/usr/bin/python3
# Advent of code 2019 day 18

# This implementation works for graphs which contains loops, with multiple paths to a key accessed via different
# sets of doors. In practice it appears that none of the examples require this. The solution could be considerably
# simpler and faster, with no need to recalculate fastest routes between points as doors are opened. The distances
# could instead be computed up-front, and at runtime shortest-path results just need to be filtered to remove those
# which contain locked doors.
#
# This implementation takes several minutes to run, but it could be reduced to seconds.

import timeit
from dataclasses import dataclass
from typing import List, Set

import networkx as nx

DIRECTIONS = {
    "north": (0, -1),
    "east": (1, 0),
    "south": (0, 1),
    "west": (-1, 0),
}


def get_neighbours(x, y):
    result = set()
    for move in DIRECTIONS.values():
        result.add((x + move[0], y + move[1]))
    return result


def find_direct_distances(grid, start_location):
    route_lengths = {}
    check_neighbours = set()
    route_lengths[start_location] = 0
    check_neighbours.add(start_location)
    while check_neighbours:
        next_check_neighbours = set()
        for location in list(check_neighbours):
            location_distance = route_lengths[location]
            for neighbour in get_neighbours(location[0], location[1]):
                if neighbour in route_lengths.keys():
                    continue
                if grid[neighbour] == "#":
                    continue
                route_lengths[neighbour] = location_distance + 1
                if grid[neighbour] == "." or grid[neighbour].isdigit():
                    next_check_neighbours.add(neighbour)
        check_neighbours = next_check_neighbours
    return route_lengths


def get_all_direct_distances(grid, start_locations, target_locations):
    """This is used to create a cache of the distances between all directly navigable
    (i.e. without moving through another object) objects of interest. Uses a possibly inefficient flood fill, but
    only used once on start-up. This is used to build a networkx graph for the proper route finding.."""
    direct_distances = dict()
    for from_target, from_location in sorted(list(target_locations.items()) + list(start_locations.items())):
        route_lengths = find_direct_distances(grid, from_location)
        for to_target, to_location in sorted(target_locations.items()):
            distance = route_lengths.get(to_location)
            if distance is not None:
                direct_distances[(from_target, to_target)] = distance
    return direct_distances


def build_route_graph(direct_distances, collected_items):
    graph = nx.DiGraph()
    for (from_target, to_target), distance in direct_distances.items():
        if to_target.isdigit():
            # No point heading back to a start location
            continue
        # Cannot move beyond a target if we have not collected it
        if from_target.isdigit() or from_target in collected_items:
            graph.add_edge(from_target, to_target, distance=distance)
    return graph


@dataclass
class RouteState:
    locations: List[str]  # multiple droid locations for part 2
    route_length: int
    collected_list: List[str]
    targets: Set[str]

    def get_state_key(self):
        return tuple(self.locations), tuple(sorted(self.collected_list))


def get_next_route_states(direct_distances, route_state, route_cache):
    result = []

    # Try moving droids one at a time
    for droid in range(0, len(route_state.locations)):
        shortest_paths = find_shortest_paths(direct_distances, route_state, droid, route_cache)

        # Try navigating to all available keys and doors
        for target in sorted(route_state.targets):
            if target.isupper() and target.lower() not in route_state.collected_list:
                # Cannot navigate to a door if we do not have the key
                continue
            route_len = shortest_paths.get(target)
            if route_len is not None:
                new_locations = list(route_state.locations)
                new_locations[droid] = target
                new_targets = set(route_state.targets)
                new_targets.remove(target)
                result.append(RouteState(locations=new_locations,
                                         route_length=route_state.route_length + route_len,
                                         collected_list=route_state.collected_list + [target],
                                         targets=new_targets))

    return result


def find_shortest_paths(direct_distances, route_state, droid, route_cache):
    # The route_cache is a dictionary into which this function can shove anything.
    # Use it as a cache of both graphs and routes

    location = route_state.locations[droid]
    collected_keys = tuple(sorted([target for target in route_state.collected_list]))
    path_cache_key = (location, collected_keys)
    shortest_paths = route_cache.get(path_cache_key)
    if shortest_paths is not None:
        return shortest_paths

    graph_cache_key = collected_keys
    graph = route_cache.get(graph_cache_key)
    if graph is None:
        graph = build_route_graph(direct_distances, set(route_state.collected_list))
        route_cache[graph_cache_key] = graph

    if location not in graph.nodes():
        shortest_paths = {}  # droid has no edges to other nodes
    else:
        shortest_paths = nx.shortest_path_length(graph, location, None, "distance")

    route_cache[path_cache_key] = shortest_paths
    return shortest_paths


def find_all_routes(direct_distances, start_locations, targets):
    initial_state = RouteState(locations=start_locations, route_length=0, targets=targets, collected_list=[])
    all_keys = set([target for target in targets if target.islower()])

    best_routes_by_state = {initial_state.get_state_key(): initial_state}
    route_states_to_check = [initial_state]
    best_complete_route_length = None

    # Travelling salesman-like problem - shortest route to visit all targets to collect all keys
    # Fortunately we have locked doors to help limit the exponential nature; implemented as a breadth-first
    # search with pruning, but it can still take 3-10 minutes for the AoC inputs depending of computer speed..
    # Unlike a standard travelling salesman, the graph changes during the process as doors become unlocked.
    iterations = 0
    while route_states_to_check:
        route_cache = dict()  # for preventing repeated unnecessary route calculations
        prune_count = 0
        print(f"Iteration {iterations} has {len(route_states_to_check)} active states to be checked")
        route_states_to_check.sort(key=lambda r: r.route_length)
        # for x in route_states_to_check:
        #     print(f"    {x.get_state_key()} {x.route_length}")
        # print()
        iterations += 1
        new_route_states_to_check = []
        for route_state in route_states_to_check:
            next_route_states = get_next_route_states(direct_distances, route_state, route_cache)
            for next_route_state in next_route_states:
                if best_complete_route_length and next_route_state.route_length >= best_complete_route_length:
                    prune_count += 1
                    continue
                state_key = next_route_state.get_state_key()
                already_found = best_routes_by_state.get(state_key)
                if already_found and already_found.route_length <= next_route_state.route_length:
                    prune_count += 1
                    continue
                best_routes_by_state[state_key] = next_route_state
                new_route_states_to_check.append(next_route_state)

                if all_keys.issubset(next_route_state.collected_list):
                    best_complete_route_length = next_route_state.route_length

        route_states_to_check = new_route_states_to_check

    # We can end up with one completed route per distinct final state: less than 5 for all the examples
    # Return all of them sorted by length. We really just need the shortest.
    complete_routes = []
    for best_route in best_routes_by_state.values():
        if all_keys.issubset(best_route.collected_list):
            complete_routes.append(best_route)
    complete_routes.sort(key=lambda r: r.route_length)
    return complete_routes


def load_grid(file):
    grid = {}
    start_locations = {}
    target_locations = {}
    with open(file) as f:
        lines = f.readlines()
    for y, line in enumerate(lines):
        for x, cell in enumerate(line.strip()):
            grid[(x, y)] = cell
            if cell == "@":
                start_symbol = str(len(start_locations))
                start_locations[start_symbol] = (x, y)
                grid[(x, y)] = start_symbol
            elif cell.isalpha():
                target_locations[cell] = (x, y)
    return grid, start_locations, target_locations


def process_file(input_file):
    grid, start_locations, target_locations = load_grid(input_file)
    direct_distances = get_all_direct_distances(grid, start_locations, target_locations)
    results = find_all_routes(direct_distances, list(start_locations.keys()), set(target_locations.keys()))
    print(results[0].route_length)


def part1():
    process_file("input_part1.txt")


def part2():
    process_file("input_part2.txt")


# This is pretty slow... several minutes.
if __name__ == "__main__":
    print("Part 1 elapsed time:", timeit.timeit(part1, number=1))
    print("Part 2 elapsed time:", timeit.timeit(part2, number=1))
