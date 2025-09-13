from pathlib import Path
from typing import Callable, Any, TextIO, List
from collections import namedtuple
from dataclasses import dataclass
from math import prod
from enum import Enum
from functools import reduce
class Field(Enum):
    TREE = "#"
    EMPTY = "."
@dataclass(frozen = True)
class Slope:
    x: int
    y:int

class AirportMap:
    def __init__(self) -> None:
        self.air_map: List[List[Field]] = []
    @classmethod
    def from_buffer(cls, buffer: TextIO) -> "AirportMap":
        result = cls()
        for line in buffer:
            hor = [Field(x) for x in line.rstrip()]
            result.air_map.append(hor)
        return result
    def num_of_trees_on_slope(self, slope = Slope(3,1)):
        m_x = len(self.air_map[0])
        m_y = len(self.air_map)
        trees= c_x= c_y = 0 #immutables, so this is fine
        while c_y < m_y:
            if self.air_map[c_y % m_y][c_x % m_x] == Field.TREE:
                trees += 1
            c_x = c_x + slope.x
            c_y = c_y + slope.y
        return trees


if __name__ == "__main__":
    with Path("inputs/day3.txt").open("r") as file:
        a_map = AirportMap().from_buffer(file)
    print(f"Answer to the first part of the puzzle: {a_map.num_of_trees_on_slope()}")
    available_slopes = [Slope(1,1),Slope(3,1),Slope(5,1),Slope(7,1), Slope(1,2)]
    trees = [a_map.num_of_trees_on_slope(slope) for slope in available_slopes]
    num_trees_multiplied = prod(trees)
    print(f"Answer to the second part of the puzzle: {num_trees_multiplied}")

