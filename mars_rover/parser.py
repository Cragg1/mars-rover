from pydantic import ValidationError

from mars_rover.commands import (
    Command,
    MoveCommand,
    TurnLeftCommand,
    TurnRightCommand,
    ReportCommand,
    PlaceArgs,
    PlaceCommand,
)
from mars_rover.models import Direction


class CommandParser:
    """Parses user input into commands."""

    USER_COMMANDS = {
        "MOVE":  MoveCommand,
        "LEFT":  TurnLeftCommand,
        "RIGHT": TurnRightCommand,
        "REPORT": ReportCommand,
    }

    # TODO: Better way to do parsing?
    def parse(self, user_input: str) -> Command:
        cmds = user_input.strip().upper()

        # Place rover
        if cmds.startswith("PLACE"):
            return self._parse_place(cmds)

        # TODO: Doesn't work yet.
        if cmds in self.USER_COMMANDS:
            return self.USER_COMMANDS

        raise ValueError(f"Unknown command: '{user_input}'")

    def _parse_place(self, text: str) -> PlaceCommand:
        # TODO: Should regex here.
        raw_args = text[5:].strip()  # remove 'PLACE'
        parts = raw_args.split(",")

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
