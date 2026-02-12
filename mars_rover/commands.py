from typing import Optional, Protocol

from mars_rover.models import PlaceArgs
from mars_rover.rover import Rover


class Command(Protocol):
    """Protocol for a rover command execution."""

    def execute(self, rover: Rover) -> Optional[str]: ...


class PlaceCommand:
    def __init__(self, args: PlaceArgs):
        self.args = args

    def execute(self, rover: Rover) -> Optional[str]:
        return rover.place(x=self.args.x, y=self.args.y, direction=self.args.direction)


class MoveCommand:
    def execute(self, rover: Rover) -> Optional[str]:
        return rover.move()


class LeftCommand:
    def execute(self, rover: Rover) -> Optional[str]:
        return rover.left()


class RightCommand:
    def execute(self, rover: Rover) -> Optional[str]:
        return rover.right()


class ReportCommand:
    def execute(self, rover: Rover) -> str:
        return rover.report()
