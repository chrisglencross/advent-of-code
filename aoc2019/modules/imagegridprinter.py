import hashlib
import os
from dataclasses import field, dataclass
from typing import Dict, Tuple, List

from PIL import Image, ImageDraw


@dataclass
class ImageGridPrinter:
    max_width: int = None
    max_height: int = None
    colour_map: Dict[object, Tuple[int, int, int]] = field(default_factory=dict)
    colour_cache: Dict[object, Tuple[int, int, int]] = field(default_factory=dict)
    grids: List[Dict[Tuple[int, int, int], object]] = field(default_factory=list)
    count: int = 0

    filename: str = None
    sample: int = 1
    duration: int = 100

    def default_rgb(self, value):
        if value in self.colour_cache:
            return self.colour_cache[value]
        if not value or value == " ":
            return 0, 0, 0
        num = 0
        data = hashlib.md5(str(value).encode()).digest()
        for i in range(0, len(data), 4):
            num = num ^ (data[i] << 16) + (data[i + 1] << 8) + data[i + 2]
        rgb = num & 0xff, (num >> 8) & 0xff, (num >> 16) & 0xff
        self.colour_cache[value] = rgb
        return rgb

    def print(self, grid):
        if self.count % self.sample == 0:
            self.grids.append(grid)
        self.count = self.count + 1

    def create_image(self, grid, min_x=None, min_y=None, max_x=None, max_y=None):

        min_x, min_y, max_x, max_y = self.get_grid_dimensions(grid, min_x, min_y, max_x, max_y)
        grid_width = max_x - min_x + 1
        grid_height = max_y - min_y + 1
        image = Image.new("RGB", (grid_width, grid_height), "black")
        pixels = image.load()

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                value = grid.get((x, y))
                colour = self.colour_map.get(value, self.default_rgb(value))
                pixels[x - min_x, y - min_y] = colour

        if self.max_height and self.max_width:
            scale = min(self.max_width // grid_width, self.max_height // grid_height)
            if scale > 1:
                image = image.resize((grid_width * scale, grid_height * scale))
            # Draw grid lines if sufficiently large
            if scale > 4:
                draw = ImageDraw.Draw(image)
                for x in range(0, image.width, scale):
                    draw.line([(x, 0), (x, image.height)], fill="gray")
                for y in range(0, image.height, scale):
                    draw.line([(0, y), (image.width, y)], fill="gray")

        return image

    @staticmethod
    def get_grid_dimensions(grid, min_x=None, min_y=None, max_x=None, max_y=None):
        xs = set([c[0] for c in grid.keys()])
        ys = set([c[1] for c in grid.keys()])
        if min_x is None:
            min_x = min(xs)
        if min_y is None:
            min_y = min(ys)
        if max_x is None:
            max_x = max(xs)
        if max_y is None:
            max_y = max(ys)
        return min_x, min_y, max_x, max_y

    def get_max_grid_dimensions(self):
        min_x, min_y, max_x, max_y = self.get_grid_dimensions(self.grids[0])
        for grid in self.grids:
            new_min_x, new_min_y, new_max_x, new_max_y = self.get_grid_dimensions(grid)
            min_x = min(min_x, new_min_x)
            min_y = min(min_y, new_min_y)
            max_x = max(max_x, new_max_x)
            max_y = max(max_y, new_max_y)
        return min_x, min_y, max_x, max_y

    def close(self):
        if self.filename and self.grids:
            print(f"Writing {len(self.grids)} frames to {self.filename}")
            min_x, min_y, max_x, max_y = self.get_max_grid_dimensions()
            images = list()
            for grid in self.grids:
                images.append(self.create_image(grid, min_x, min_y, max_x, max_y))
            if os.path.exists(self.filename):
                os.remove(self.filename)
            images[0].save(self.filename,
                           save_all=True,
                           append_images=images[1:],
                           duration=self.duration,
                           loop=0)
        self.grids.clear()
        self.count = 0
