from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple, Dict


@dataclass
class Direction:
    name: str
    left_name: str
    right_name: str
    reverse_name: str
    delta: Tuple[int, int] = field()
    directions: Dict[str, Direction] = field()

    def move(self, from_location, step=1):
        return from_location[0] + self.delta[0] * step, from_location[1] + self.delta[1] * step

    def turn_left(self, turns=1):
        result = self
        for i in range(0, turns):
            result = result.directions[result.left_name]
        return result

    def turn_right(self, turns=1):
        result = self
        for i in range(0, turns):
            result = result.directions[result.right_name]
        return result

    def reverse(self) -> Direction:
        return self.directions[self.reverse_name]

# Directions with left and right turns
UDLR_DIRECTIONS = {}
UDLR_DIRECTIONS["U"] = Direction(name="U", delta=(0, -1), left_name="L", right_name="R", reverse_name="D",
                                    directions=UDLR_DIRECTIONS)
UDLR_DIRECTIONS["R"] = Direction(name="R", delta=(1, 0), left_name="U", right_name="D", reverse_name="R",
                                    directions=UDLR_DIRECTIONS)
UDLR_DIRECTIONS["D"] = Direction(name="D", delta=(0, 1), left_name="R", right_name="L", reverse_name="U",
                                    directions=UDLR_DIRECTIONS)
UDLR_DIRECTIONS["L"] = Direction(name="L", delta=(-1, 0), left_name="D", right_name="U", reverse_name="R",
                                    directions=UDLR_DIRECTIONS)

# Directions with left and right turns
COMPASS_DIRECTIONS = {}
COMPASS_DIRECTIONS["N"] = Direction(name="N", delta=(0, -1), left_name="W", right_name="E", reverse_name="S",
                                    directions=COMPASS_DIRECTIONS)
COMPASS_DIRECTIONS["E"] = Direction(name="E", delta=(1, 0), left_name="N", right_name="S", reverse_name="W",
                                    directions=COMPASS_DIRECTIONS)
COMPASS_DIRECTIONS["S"] = Direction(name="S", delta=(0, 1), left_name="E", right_name="W", reverse_name="N",
                                    directions=COMPASS_DIRECTIONS)
COMPASS_DIRECTIONS["W"] = Direction(name="W", delta=(-1, 0), left_name="S", right_name="N", reverse_name="E",
                                    directions=COMPASS_DIRECTIONS)

COMPASS_DIRECTIONS_8 = {}
COMPASS_DIRECTIONS_8["N"] = Direction(name="N", delta=(0, -1), left_name="NW", right_name="NE", reverse_name="S",
                                      directions=COMPASS_DIRECTIONS_8)
COMPASS_DIRECTIONS_8["E"] = Direction(name="E", delta=(1, 0), left_name="NE", right_name="SE", reverse_name="W",
                                      directions=COMPASS_DIRECTIONS_8)
COMPASS_DIRECTIONS_8["S"] = Direction(name="S", delta=(0, 1), left_name="SE", right_name="SW", reverse_name="N",
                                      directions=COMPASS_DIRECTIONS_8)
COMPASS_DIRECTIONS_8["W"] = Direction(name="W", delta=(-1, 0), left_name="SW", right_name="NW", reverse_name="E",
                                      directions=COMPASS_DIRECTIONS_8)
COMPASS_DIRECTIONS_8["NE"] = Direction(name="NE", delta=(1, -1), left_name="N", right_name="E", reverse_name="SW",
                                       directions=COMPASS_DIRECTIONS_8)
COMPASS_DIRECTIONS_8["SE"] = Direction(name="SE", delta=(1, 1), left_name="E", right_name="S", reverse_name="SW",
                                       directions=COMPASS_DIRECTIONS_8)
COMPASS_DIRECTIONS_8["SW"] = Direction(name="SW", delta=(-1, 1), left_name="S", right_name="W", reverse_name="NE",
                                       directions=COMPASS_DIRECTIONS_8)
COMPASS_DIRECTIONS_8["NW"] = Direction(name="NW", delta=(-1, -1), left_name="W", right_name="N", reverse_name="SE",
                                       directions=COMPASS_DIRECTIONS_8)
