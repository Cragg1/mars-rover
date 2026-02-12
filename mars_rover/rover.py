from typing import Optional

from mars_rover.models import Direction, Position, TableBounds


class Rover:
    """A Mars rover that can be positioned and moved around an empty table."""

    _MOVEMENT_CHANGES = {
        Direction.NORTH: (0, 1),
        Direction.EAST: (1, 0),
        Direction.SOUTH: (0, -1),
        Direction.WEST: (-1, 0),
    }

    def __init__(
        self,
        bounds: TableBounds,
        position: Optional[Position] = None,
        direction: Optional[Direction] = None,
    ):
        self.bounds = bounds
        self.position = position
        self.direction = direction

    def place(self, x: int, y: int, direction: Direction) -> str | None:
        pos = Position(x, y)
        if not self.bounds.contains(pos):
            return f"Invalid PLACE command: position ({x},{y}) is outside table bounds"
        self.position = pos
        self.direction = direction
        return None

    def _ensure_rover_is_placed(self) -> None:
        if self.position is None or self.direction is None:
            raise RuntimeError("Rover must be placed on the table first")

    def move(self) -> str | None:
        self._ensure_rover_is_placed()
        dx, dy = self._MOVEMENT_CHANGES[self.direction]
        new_pos = Position(self.position.x + dx, self.position.y + dy)
        if self.bounds.contains(new_pos):
            self.position = new_pos
            return None
        return f"Invalid MOVE command: would move rover outside table bounds"

    def left(self) -> str | None:
        self._ensure_rover_is_placed()
        self.direction = self.direction.left()
        return None

    def right(self) -> str | None:
        self._ensure_rover_is_placed()
        self.direction = self.direction.right()
        return None

    def report(self) -> str:
        self._ensure_rover_is_placed()
        return f"{self.position.x},{self.position.y},{self.direction.value}"
