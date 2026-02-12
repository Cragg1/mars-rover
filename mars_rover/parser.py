from pydantic import ValidationError

from mars_rover.commands import (
    Command,
    MoveCommand,
    LeftCommand,
    RightCommand,
    ReportCommand,
    PlaceCommand,
)
from mars_rover.models import Direction, PlaceArgs


class CommandParser:
    """Parses user input into commands."""

    _COMMANDS = {
        "MOVE": MoveCommand,
        "LEFT": LeftCommand,
        "RIGHT": RightCommand,
        "REPORT": ReportCommand,
    }

    def parse(self, user_input: str) -> Command:
        cmd = user_input.strip().upper()

        if cmd.startswith("PLACE"):
            return self._parse_place(cmd)

        if cmd in self._COMMANDS:
            return self._COMMANDS[cmd]()

        raise ValueError(f"Unknown command: '{user_input}'")

    def _parse_place(self, text: str) -> PlaceCommand:
        raw_args = text[5:].strip()  # removes "PLACE"
        parts = [p.strip() for p in raw_args.split(",")]

        if len(parts) != 3:
            raise ValueError("PLACE requires exactly 3 arguments: PLACE X,Y,F")

        try:
            args = PlaceArgs(
                x=int(parts[0]),
                y=int(parts[1]),
                direction=Direction(parts[2]),
            )
        except (ValueError, ValidationError) as exc:
            raise ValueError(f"Invalid PLACE command: {text}") from exc

        return PlaceCommand(args)
