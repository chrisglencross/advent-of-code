#!/usr/bin/python3
# Advent of code 2019 day 18

# Faster version which doesn't work with graphs containing cycles.
# On my laptop part 1 takes 30 seconds, vs. 135 seconds with the previous version.
import string
import timeit
from dataclasses import dataclass
from typing import List, Set

import networkx as nx

from aoc2019.modules.grid import load_grid


@dataclass
class RouteState:
    locations: List[str]  # multiple droid locations for part 2
    route_length: int
    collected_list: List[str]
    targets: Set[str]

    def get_state_key(self):
        return tuple(self.locations), tuple(sorted(self.collected_list))


@dataclass
class RouteInfo:
    path: List[str]
    route_len: int


def find_direct_distances(grid, start_location):
    """Returns distances of all cells directly reachable from start_location without moving beyond any key or door."""

    def custom_is_navigable(grid, from_coords, to_coords):
        return (from_coords == start_location or grid[from_coords] in string.digits + ".") \
               and grid[to_coords] not in "#"

    graph = grid.build_digraph(is_navigable=custom_is_navigable)
    return nx.shortest_path_length(graph, start_location, None, weight="distance")


def build_route_graph(grid, start_locations, target_locations):
    """Creates a graph of navigable objects in the graph."""
    graph = nx.DiGraph()
    for from_target, from_location in sorted(list(target_locations.items()) + list(start_locations.items())):
        route_lengths = find_direct_distances(grid, from_location)
        for to_target, to_location in sorted(target_locations.items()):
            distance = route_lengths.get(to_location)
            if distance is not None and not to_target.isdigit():
                graph.add_edge(from_target, to_target, distance=distance)
    return graph


def get_next_route_states(route_state, route_cache):
    """Given a state of objects in the maze, returns the next set of possible states"""
    result = []

    # Try moving all droids one at a time
    for droid in range(0, len(route_state.locations)):

        # Try navigating to all reachable keys and doors
        for target in route_state.targets:

            if target.isupper() and target.lower() in route_state.targets:
                # Target is a door, and we have not yet collected the key. Don't go there.
                continue

            route_info = route_cache.get((route_state.locations[droid], target))
            if route_info is None:
                # No route to this target (part 2, fully partitioned grid)
                continue
            if not route_state.targets.isdisjoint(route_info.path[1:-1]):
                # Don't follow route if there is an intermediate target in the path that we haven't collected
                # - we will already return a RouteState to go to that intermediate target
                continue

            # Create a new state object representing the moved droid and its effects
            new_locations = list(route_state.locations)
            new_locations[droid] = target
            new_targets = set(route_state.targets)
            new_targets.remove(target)
            result.append(RouteState(locations=new_locations,
                                     route_length=route_state.route_length + route_info.route_len,
                                     collected_list=route_state.collected_list + [target],
                                     targets=new_targets))

    return result


def path_length(graph, path):
    length = 0
    for i, node in enumerate(path[1:]):
        prev = path[i]
        length += graph[prev][node]["distance"]
    return length


def find_all_routes(route_cache, start_locations, targets):
    initial_state = RouteState(locations=start_locations, route_length=0, targets=targets, collected_list=[])
    all_keys = set([target for target in targets if target.islower()])

    best_routes_by_state = {initial_state.get_state_key(): initial_state}
    route_states_to_check = [initial_state]
    best_complete_route_length = None

    # Travelling salesman-like problem - shortest route to visit all targets (i.e. to collect all keys)
    # Fortunately we have locked doors to help limit the exponential nature; implemented as a breadth-first
    # search with pruning, but it can still take 1-3 minutes for part 2, depending on computer speed.
    iterations = 0
    while route_states_to_check:
        prune_count = 0
        print(f"Iteration {iterations} has {len(route_states_to_check)} active states to be checked")
        route_states_to_check.sort(key=lambda r: r.route_length)
        # for x in route_states_to_check:
        #     print(f"    {x.get_state_key()} {x.route_length}")
        # print()
        iterations += 1
        new_route_states_to_check = []
        for route_state in route_states_to_check:
            next_route_states = get_next_route_states(route_state, route_cache)
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

                if all_keys.isdisjoint(next_route_state.targets):
                    best_complete_route_length = next_route_state.route_length

        route_states_to_check = new_route_states_to_check

    # We can end up with one completed route per distinct final state: less than 5 for all the examples
    # Return all of them sorted by length. We really just need the shortest.
    complete_routes = []
    for best_route in best_routes_by_state.values():
        if all_keys.isdisjoint(best_route.targets):
            complete_routes.append(best_route)
    complete_routes.sort(key=lambda r: r.route_length)
    return complete_routes


def process_file(input_file):
    # Load the file
    grid = load_grid(input_file)

    # Replace @ with a digit (part 2 has multiple droids)
    for droid, location in enumerate(grid.find_cells("@")):
        grid[location] = str(droid)
    start_locations = grid.index_cells(string.digits)
    target_locations = grid.index_cells(string.ascii_letters)

    # Pre-calculate and cache the path and distance between all pairs of objects
    graph = build_route_graph(grid, start_locations, target_locations)
    route_cache = dict()
    for source, target_path in nx.shortest_path(graph, None, None, "distance").items():
        for target, path in target_path.items():
            route_cache[(source, target)] = RouteInfo(path, path_length(graph, path))

    results = find_all_routes(route_cache, list(start_locations.keys()), set(target_locations.keys()))
    print(results[0].route_length)


def part1():
    process_file("input_part1.txt")


def part2():
    process_file("input_part2.txt")


if __name__ == "__main__":
    print("Part 1 elapsed time:", timeit.timeit(part1, number=1))
    print("Part 2 elapsed time:", timeit.timeit(part2, number=1))
