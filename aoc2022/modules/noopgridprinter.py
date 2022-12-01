from dataclasses import dataclass


@dataclass
class NoOpGridPrinter:
    def print(self, grid):
        pass

    def close(self):
        pass
