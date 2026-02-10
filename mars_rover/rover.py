from dataclasses import dataclass

from mars_rover.models import Direction, Position, TableBounds


@dataclass
class Rover:
    bounds: TableBounds
    position: Position
    direction: Direction

    _MOVEMENT_CHANGES = {
        Direction.NORTH: (0, 1),
        Direction.EAST:  (1, 0),
        Direction.SOUTH: (0, -1),
        Direction.WEST:  (-1, 0),
    }

    def place(self, x: int, y: int, direction: Direction) -> None:
        pos = Position(x, y)
        if not self.bounds.contains(pos):
            raise ValueError(f"Position {pos} is outside table bounds")
        self.position = pos
        self.direction = direction

    def _ensure_rover_is_placed(self) -> None:
        if self.position is None or self.direction is None:
            raise RuntimeError("Rover must be placed on the table first")

    def move_forward(self) -> None:
        self._ensure_rover_is_placed()
        dx, dy = self._MOVEMENT_CHANGES[self.direction]
        new_pos = Position(self.position.x + dx, self.position.y + dy)
        if self.bounds.contains(new_pos):
            self.position = new_pos

    def turn_left(self) -> None:
        self._ensure_rover_is_placed()
        self.direction = self.direction.turn_left()

    def turn_right(self) -> None:
        self._ensure_rover_is_placed()
        self.direction = self.direction.turn_right()

    def report(self) -> str:
        self._ensure_rover_is_placed()
        return f"{self.position.x},{self.position.y},{self.direction.value}"
