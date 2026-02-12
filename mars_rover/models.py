from dataclasses import dataclass
from enum import StrEnum
from pydantic import BaseModel


class Direction(StrEnum):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"

    def left(self) -> "Direction":
        """Rotate rover counter-clockwise."""
        rotations = {
            Direction.NORTH: Direction.WEST,
            Direction.WEST: Direction.SOUTH,
            Direction.SOUTH: Direction.EAST,
            Direction.EAST: Direction.NORTH,
        }
        return rotations[self]

    def right(self) -> "Direction":
        """Rotate rover clockwise."""
        rotations = {
            Direction.NORTH: Direction.EAST,
            Direction.EAST: Direction.SOUTH,
            Direction.SOUTH: Direction.WEST,
            Direction.WEST: Direction.NORTH,
        }
        return rotations[self]


@dataclass(frozen=True)
class Position:
    x: int
    y: int


@dataclass(frozen=True)
class TableBounds:
    min_x: int = 0
    min_y: int = 0
    max_x: int = 5
    max_y: int = 5

    def contains(self, pos: Position) -> bool:
        return self.min_x <= pos.x <= self.max_x and self.min_y <= pos.y <= self.max_y


class PlaceArgs(BaseModel):
    x: int
    y: int
    direction: Direction
