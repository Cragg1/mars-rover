"""Mars rover with movement and positioning logic."""

from typing import Optional

from mars_rover.models import Direction, Position, TableBounds
from mars_rover.exceptions import RoverNotPlacedException
from mars_rover.messages import ErrorMessages
from mars_rover.result import CommandResult


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

    def place(self, x: int, y: int, direction: Direction) -> CommandResult:
        """Place rover at specified position and direction.

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            direction (Direction): Facing direction

        Returns:
            CommandResult indicating success or failure
        """
        pos = Position(x, y)
        if not self.bounds.contains(pos):
            return CommandResult.error(
                ErrorMessages.POSITION_OUT_OF_BOUNDS.format(x=x, y=y)
            )
        self.position = pos
        self.direction = direction
        return CommandResult.ok()

    def _ensure_rover_is_placed(self) -> None:
        """Ensure rover has been placed before executing commands.

        Raises:
            RoverNotPlacedException: If rover has not been placed
        """
        if self.position is None or self.direction is None:
            raise RoverNotPlacedException(ErrorMessages.ROVER_NOT_PLACED)

    def move(self) -> CommandResult:
        """Move rover one unit forward in current direction.

        Returns:
            CommandResult indicating success or failure

        Raises:
            RoverNotPlacedException: If rover has not been placed
        """
        self._ensure_rover_is_placed()
        dx, dy = self._MOVEMENT_CHANGES[self.direction]
        new_pos = Position(self.position.x + dx, self.position.y + dy)
        if self.bounds.contains(new_pos):
            self.position = new_pos
            return CommandResult.ok()
        return CommandResult.error(ErrorMessages.MOVE_OUT_OF_BOUNDS)

    def left(self) -> CommandResult:
        """Rotate rover 90° counter-clockwise.

        Returns:
            CommandResult indicating success

        Raises:
            RoverNotPlacedException: If rover has not been placed
        """
        self._ensure_rover_is_placed()
        self.direction = self.direction.left()
        return CommandResult.ok()

    def right(self) -> CommandResult:
        """Rotate rover 90° clockwise.

        Returns:
            CommandResult indicating success

        Raises:
            RoverNotPlacedException: If rover has not been placed
        """
        self._ensure_rover_is_placed()
        self.direction = self.direction.right()
        return CommandResult.ok()

    def report(self) -> str:
        """Report current position and direction.

        Returns:
            String representation of position and direction

        Raises:
            RoverNotPlacedException: If rover has not been placed
        """
        self._ensure_rover_is_placed()
        return f"{self.position.x},{self.position.y},{self.direction.value}"
