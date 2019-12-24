from dataclasses import field, dataclass
from typing import Dict


@dataclass
class TextGridPrinter:
    symbol_map: Dict[object, str] = field(default_factory=dict)
    default_value: str = " "

    def print(self, grid):
        (min_x, min_y), (max_x, max_y) = grid.get_bounds()
        for y in range(min_x, max_y + 1):
            row = []
            for x in range(min_x, max_y + 1):
                value = grid.get((x, y), self.default_value)
                symbol = self.symbol_map.get(value, str(value))
                if len(symbol) == 0:
                    symbol = " "
                else:
                    symbol = symbol[0]
                row.append(symbol)
            line = "".join(row)
            print(line)

    def close(self):
        pass
