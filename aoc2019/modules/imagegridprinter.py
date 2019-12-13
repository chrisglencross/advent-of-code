import hashlib
from dataclasses import field, dataclass
from typing import Dict, Tuple, List

from PIL import Image, ImageDraw


@dataclass
class ImageGridPrinter:
    max_width: int = None
    max_height: int = None
    colour_map: Dict[object, Tuple[int, int, int]] = field(default_factory=dict)
    colour_cache: Dict[object, Tuple[int, int, int]] = field(default_factory=dict)
    images: List[Image.Image] = field(default_factory=list)
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
            self.images.append(self.create_image(grid))
        self.count = self.count + 1

    def create_image(self, grid):
        xs = set([c[0] for c in grid.keys() if c[0] >= 0])
        ys = set([c[0] for c in grid.keys() if c[0] >= 0])

        min_y = min(ys)
        min_x = min(xs)
        image_height = max(ys) - min(ys) + 1
        image_width = max(xs) - min(xs) + 1
        image = Image.new("RGB", (image_width, image_height), "black")
        pixels = image.load()

        for y in range(min(ys), max(ys) + 1):
            for x in range(min(xs), max(xs) + 1):
                value = grid.get((x, y), 0)
                colour = self.colour_map.get(value, self.default_rgb(value))
                pixels[x - min_x, y - min_y] = colour

        if self.max_height and self.max_width:
            scale = min(self.max_width // image_width, self.max_height // image_height)
            if scale > 1:
                image = image.resize((image_width * scale, image_height * scale))
            # Draw grid lines if sufficiently large
            if scale > 4:
                draw = ImageDraw.Draw(image)
                for x in range(0, image.width, scale):
                    draw.line([(x, 0), (x, image.height)], fill="gray")
                for y in range(0, image.height, scale):
                    draw.line([(0, y), (image.width, y)], fill="gray")

        return image

    def close(self):
        if self.filename and self.images:
            self.images[0].save(self.filename,
                                save_all=True,
                                append_images=self.images[1:],
                                duration=self.duration,
                                loop=0)
        self.images.clear()
        self.count = 0

    def __del__(self):
        self.flush()
