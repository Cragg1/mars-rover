"""Command pattern implementation for rover operations."""

from typing import Protocol

from mars_rover.models import PlaceArgs
from mars_rover.rover import Rover
from mars_rover.result import CommandResult


class Command(Protocol):
    """Protocol for a rover command execution."""

    def execute(self, rover: Rover) -> CommandResult | str: ...


class PlaceCommand:
    """Command to place rover at a position."""

    def __init__(self, args: PlaceArgs):
        self.args = args

    def execute(self, rover: Rover) -> CommandResult:
        """Execute PLACE command."""
        return rover.place(x=self.args.x, y=self.args.y, direction=self.args.direction)


class MoveCommand:
    """Command to move rover forward."""

    def execute(self, rover: Rover) -> CommandResult:
        """Execute MOVE command."""
        return rover.move()


class LeftCommand:
    """Command to rotate rover left."""

    def execute(self, rover: Rover) -> CommandResult:
        """Execute LEFT command."""
        return rover.left()


class RightCommand:
    """Command to rotate rover right."""

    def execute(self, rover: Rover) -> CommandResult:
        """Execute RIGHT command."""
        return rover.right()


class ReportCommand:
    """Command to report rover position."""

    def execute(self, rover: Rover) -> str:
        """Execute REPORT command."""
        return rover.report()
