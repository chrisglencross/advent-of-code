from __future__ import annotations

from typing import Tuple, Dict, List

import networkx as nx

from aoc2019.modules import textgridprinter
from aoc2019.modules.directions import COMPASS_DIRECTIONS

Coords = Tuple[int, int]


def default_is_navigable(grid: Grid, from_coord: Coords, to_coord: Coords):
    return grid[from_coord] in {"."} and grid[to_coord] in {"."}


def default_node_factory(coords):
    return coords


class Grid:
    def __init__(self, grid, directions=COMPASS_DIRECTIONS.values()):
        self.grid = grid
        self.directions = directions

    def items(self):
        return self.grid.items()

    def get_bounds(self) -> Tuple[Coords, Coords]:
        xs = set([c[0] for c in self.grid.keys()])
        ys = set([c[1] for c in self.grid.keys()])
        if not xs:
            xs = {0}
        if not ys:
            ys = {0}
        return (min(xs), min(ys)), (max(xs), max(ys))

    def find_cell(self, symbol) -> Coords:
        for coords, cell in self.grid.items():
            if cell == symbol:
                return coords
        return None

    def find_cells(self, symbol) -> List[Coords]:
        result = []
        for coords, cell in self.grid.items():
            if cell == symbol:
                result.append(coords)
        return result

    def index_cells(self, symbols=None, not_symbols=None) -> Dict[str, Coords]:
        if symbols is None and not_symbols is None:
            not_symbols = {".", "#", " "}
        result = {}
        for coords, cell in self.grid.items():
            if (symbols and cell in symbols) or (not_symbols and cell not in not_symbols):
                if result.get(cell) is not None:
                    raise Exception(f"Symbol {cell} is repeated in grid. Index it with index_repeating_cells()")
                result[cell] = coords
        return result

    def index_repeating_cells(self, symbols=None, not_symbols=None) -> Dict[str, List[Coords]]:
        if symbols is None and not_symbols is None:
            not_symbols = {".", "#", " "}
        result = {}
        for coords, cell in self.grid.items():
            if (symbols and cell in symbols) or (not_symbols and cell not in not_symbols):
                result_list = result.get(cell)
                if result_list is None:
                    result_list = []
                    result[cell] = result_list
                result_list.append(coords)
        return result

    def keys(self):
        return self.grid.keys()

    def values(self):
        return self.grid.values()

    def get(self, coords: Coords, default_value=None):
        return self.grid.get(coords, default_value)

    def __getitem__(self, coords: Coords):
        return self.get(coords)

    def __setitem__(self, coords: Coords, cell: str):
        self.grid[coords] = cell

    def build_graph(self,
                    directions=COMPASS_DIRECTIONS.values(),
                    node_factory=default_node_factory,
                    is_navigable=default_is_navigable) -> nx.Graph:
        graph = nx.Graph()
        self.add_graph_edges(graph, directions, node_factory, is_navigable)
        return graph

    def build_digraph(self,
                      directions=COMPASS_DIRECTIONS.values(),
                      node_factory=default_node_factory,
                      is_navigable=default_is_navigable) -> nx.DiGraph:
        graph = nx.DiGraph()
        self.add_graph_edges(graph, directions, node_factory, is_navigable)
        return graph

    def add_graph_edges(self, graph: nx.Graph,
                        directions=COMPASS_DIRECTIONS.values(),
                        node_factory=default_node_factory,
                        is_navigable=default_is_navigable):
        for from_coords, from_symbol in self.items():
            from_node = node_factory(from_coords)
            for direction in directions:
                to_coords = direction.move(from_coords)
                to_symbol = self.get(to_coords)
                if to_symbol and is_navigable(self, from_coords, to_coords):
                    to_node = node_factory(to_coords)
                    graph.add_edge(from_node, to_node, distance=1)

    def print(self):
        textgridprinter.TextGridPrinter().print(self)


def parse_grid(content: str) -> Grid:
    grid = {}
    for y, line in enumerate(content.split("\n")):
        for x, cell in enumerate(line.rstrip()):
            grid[(x, y)] = cell
    return Grid(grid)


def load_grid(file: str) -> Grid:
    grid = {}
    with open(file) as f:
        content = f.read()
    return parse_grid(content)
