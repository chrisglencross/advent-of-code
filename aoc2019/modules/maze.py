import networkx as nx

COMPASS_DIRECTIONS = {
    "north": (0, -1),
    "east": (1, 0),
    "south": (0, 1),
    "west": (-1, 0),

}


def load_grid(file):
    grid = {}
    with open(file) as f:
        lines = f.readlines()
    for y, line in enumerate(lines):
        for x, cell in enumerate(line.rstrip()):
            grid[(x, y)] = cell
    return grid


def move_location(from_location, direction):
    return from_location[0] + direction[0], from_location[1] + direction[1]


def get_grid_limits(grid):
    xs = set([c[0] for c in grid.keys()])
    ys = set([c[1] for c in grid.keys()])
    return (min(xs), min(ys)), (max(xs), max(ys))


def find_contents(grid, items):
    pass


def build_digraph(grid):
    graph = nx.DiGraph()
    return add_graph_edges(graph, grid)


def add_graph_edges(graph, grid):
    for loc, cell in grid.items():
        graph.add_node(loc, symbol=cell)
    for loc, cell in grid.items():
        if cell in {"."}:
            for direction in COMPASS_DIRECTIONS.values():
                neighbour_loc = move_location(loc, direction)
                if grid.get(neighbour_loc) in {"."}:
                    graph.add_edge(loc, neighbour_loc, direction=direction, distance=1)
    return graph

#
# start_locations = {}
# target_locations = {}
# if cell == "@":
#     start_symbol = str(len(start_locations))
#     start_locations[start_symbol] = (x, y)
#     grid[(x, y)] = start_symbol
# elif cell.isalpha():
#     target_locations[cell] = (x, y)
#
# start_locations, target_locations
