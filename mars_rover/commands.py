from dataclasses import dataclass
from typing import Optional, Protocol
from pydantic import BaseModel

from mars_rover.models import Direction
from mars_rover.rover import Rover


class Command(Protocol):
    """Protocol for a rover command execution."""
    def execute(self, rover: Rover) -> Optional[str]:
        ...


class MoveCommand:
    def execute(self, rover: Rover) -> None:
        rover.move_forward()
        return None


class TurnLeftCommand:
    def execute(self, rover: Rover) -> None:
        rover.turn_left()
        return None


class TurnRightCommand:
    def execute(self, rover: Rover) -> None:
        rover.turn_right()
        return None


class ReportCommand:
    def execute(self, rover: Rover) -> str:
        return rover.report()


class PlaceArgs(BaseModel):
    x: int
    y: int
    direction: Direction


@dataclass
class PlaceCommand:
    args: PlaceArgs

    def execute(self, rover: Rover) -> None:
        rover.place(
            x=self.args.x,
            y=self.args.y,
            direction=self.args.direction
        )
        return None
