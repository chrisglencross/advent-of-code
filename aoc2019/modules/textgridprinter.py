from dataclasses import field, dataclass
from typing import Dict


@dataclass
class TextGridPrinter:
    symbol_map: Dict[object, str] = field(default_factory=dict)
    default_value: str = " "

    def print(self, grid):
        xs = set([c[0] for c in grid.keys()])
        ys = set([c[1] for c in grid.keys()])
        for y in range(min(ys), max(ys) + 1):
            row = []
            for x in range(min(xs), max(xs) + 1):
                value = grid.get((x, y), self.default_value)
                symbol = self.symbol_map.get(value, str(value))
                if len(symbol) == 0:
                    symbol = " "
                else:
                    symbol = symbol[0]
                row.append(symbol)
            line = "".join(row)
            if line.strip():
                print(line)

    def close(self):
        pass
