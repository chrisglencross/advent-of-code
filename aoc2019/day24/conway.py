#!/usr/bin/python3
# Conway's Game of Life, similar to part 1.

from aoc2019.modules import grid as g, directions, imagegridprinter


def tick(grid):
    new_grid = {}
    (min_x, min_y), (max_x, max_y) = grid.get_bounds()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            neighbours = 0
            for direction in directions.COMPASS_DIRECTIONS_8.values():
                neighbour = grid.get(direction.move((x, y)), ".")
                if neighbour == "#":
                    neighbours += 1
            if grid[(x, y)] == "#":
                new_grid[(x, y)] = "#" if 2 <= neighbours <= 3 else "."
            else:
                new_grid[(x, y)] = "#" if neighbours == 3 else "."
    return g.Grid(new_grid)


printer = imagegridprinter.ImageGridPrinter(max_width=800, max_height=800, duration=500, filename="conway.gif",
                                            colour_map={".": (0, 0, 0), "#": (255, 255, 255)})
grid = g.load_grid("conway.txt")
printer.print(grid)
for i in range(0, 105):
    print(i)
    grid = tick(grid)
    printer.print(grid)

printer.close()
